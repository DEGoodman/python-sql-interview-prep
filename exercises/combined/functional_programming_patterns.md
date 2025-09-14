# Functional Programming Patterns for Senior Developer Interviews

## Overview
This guide covers functional programming patterns that demonstrate mature architecture thinking for senior developer interviews, specifically focusing on Python applications with business logic, database operations, and APIs.

## Core Functional Patterns

### 1. Pure Functions vs Side Effects

**❌ Impure - mixes business logic with side effects**
```python
def process_payment(user_id, amount):
    user = db.get_user(user_id)  # Side effect
    if user.balance < amount:
        raise InsufficientFunds()
    
    user.balance -= amount
    db.save_user(user)  # Side effect
    send_email(user.email, "Payment processed")  # Side effect
    return {"status": "success"}
```

**✅ Pure business logic separated**
```python
def calculate_payment(user_balance, amount):
    """Pure function - same input always produces same output"""
    if user_balance < amount:
        return {"valid": False, "error": "insufficient_funds"}
    return {"valid": True, "new_balance": user_balance - amount}

def process_payment(user_id, amount):
    """Orchestrates side effects"""
    user = db.get_user(user_id)  # Side effect
    result = calculate_payment(user.balance, amount)  # Pure
    
    if not result["valid"]:
        raise InsufficientFunds(result["error"])
    
    db.update_balance(user_id, result["new_balance"])  # Side effect
    send_email(user.email, "Payment processed")  # Side effect
    return {"status": "success"}
```

### 2. Command/Query Separation (CQS)

Commands modify state and return nothing meaningful. Queries return data and never modify state.

```python
class OrderService:
    # ✅ Query - pure, no side effects
    def calculate_order_total(self, items: List[Item], discount_code: str = None) -> Decimal:
        subtotal = sum(item.price * item.quantity for item in items)
        discount = self._calculate_discount(subtotal, discount_code)
        tax = subtotal * Decimal('0.08')
        return subtotal - discount + tax
    
    def validate_order(self, order_data: dict) -> dict:
        """Pure validation - returns validation result"""
        errors = []
        if not order_data.get('items'):
            errors.append("Order must contain items")
        if order_data.get('total', 0) <= 0:
            errors.append("Order total must be positive")
        return {"valid": len(errors) == 0, "errors": errors}
    
    # ✅ Command - modifies state, minimal return
    def create_order(self, order_data: dict) -> str:
        validation = self.validate_order(order_data)  # Query
        if not validation["valid"]:
            raise ValidationError(validation["errors"])
        
        total = self.calculate_order_total(order_data["items"])  # Query
        
        # Side effects isolated here
        order_id = db.insert_order({
            **order_data,
            "total": total,
            "created_at": datetime.utcnow()
        })
        
        audit_log.record("order_created", order_id)
        return order_id
```

### 3. Layered Architecture - Business Logic Isolation

**Domain Layer - Pure business logic**
```python
class PricingEngine:
    @staticmethod
    def calculate_subscription_price(plan_type: str, months: int, user_tier: str) -> dict:
        """Pure function - no database calls or external dependencies"""
        base_prices = {"basic": 10, "premium": 25, "enterprise": 100}
        
        if plan_type not in base_prices:
            return {"valid": False, "error": "Invalid plan type"}
        
        monthly_price = base_prices[plan_type]
        
        # Business rules
        if months >= 12:
            monthly_price *= 0.9  # 10% annual discount
        if user_tier == "student":
            monthly_price *= 0.5  # 50% student discount
            
        return {
            "valid": True,
            "monthly_price": monthly_price,
            "total_price": monthly_price * months,
            "discounts_applied": months >= 12 or user_tier == "student"
        }
```

**Service Layer - Orchestrates business logic + side effects**
```python
class SubscriptionService:
    def __init__(self, db, payment_gateway, email_service):
        self.db = db
        self.payment_gateway = payment_gateway
        self.email_service = email_service
    
    def create_subscription(self, user_id: str, plan_data: dict) -> dict:
        # Get data (side effect)
        user = self.db.get_user(user_id)
        
        # Pure business logic
        pricing = PricingEngine.calculate_subscription_price(
            plan_data["plan_type"], 
            plan_data["months"], 
            user["tier"]
        )
        
        if not pricing["valid"]:
            raise ValidationError(pricing["error"])
        
        # Side effects
        payment_result = self.payment_gateway.charge(
            user["payment_method"], 
            pricing["total_price"]
        )
        
        subscription_id = self.db.create_subscription({
            "user_id": user_id,
            "plan_type": plan_data["plan_type"],
            "months": plan_data["months"],
            "price_paid": pricing["total_price"],
            "payment_id": payment_result["id"]
        })
        
        self.email_service.send_confirmation(user["email"], subscription_id)
        
        return {"subscription_id": subscription_id, "amount_charged": pricing["total_price"]}
```

### 4. Functional Error Handling

**Result/Either pattern for functional error handling**
```python
from typing import Union, Optional
from dataclasses import dataclass

@dataclass
class Success:
    value: any

@dataclass 
class Failure:
    error: str

Result = Union[Success, Failure]

def safe_divide(a: float, b: float) -> Result:
    """Pure function that can't throw exceptions"""
    if b == 0:
        return Failure("Division by zero")
    return Success(a / b)

# Chain operations safely
def calculate_ratio(numerator: float, denominator: float, multiplier: float) -> Result:
    division_result = safe_divide(numerator, denominator)
    if isinstance(division_result, Failure):
        return division_result
    
    multiply_result = safe_divide(division_result.value * multiplier, 1)
    return multiply_result
```

**Optional/Maybe pattern**
```python
def find_user_by_email(email: str) -> Optional[dict]:
    """Returns None instead of raising exception"""
    user = db.query("SELECT * FROM users WHERE email = ?", email).first()
    return user if user else None

def get_user_subscription_status(email: str) -> dict:
    user = find_user_by_email(email)
    if not user:
        return {"status": "user_not_found"}
    
    subscription = db.query(
        "SELECT * FROM subscriptions WHERE user_id = ? AND active = true", 
        user["id"]
    ).first()
    
    if not subscription:
        return {"status": "no_active_subscription"}
    
    return {"status": "active", "plan": subscription["plan_type"]}
```

## Complete Example: E-commerce Order System

### API Layer (FastAPI/Flask)
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class OrderRequest(BaseModel):
    user_id: str
    items: List[dict]
    shipping_address: dict
    discount_code: Optional[str] = None

@app.post("/orders")
def create_order_endpoint(request: OrderRequest):
    try:
        result = order_service.process_order(request.dict())
        return {"order_id": result["order_id"], "total": result["total"]}
    except ValidationError as e:
        raise HTTPException(400, str(e))
    except InsufficientInventoryError as e:
        raise HTTPException(409, str(e))
```

### Service Layer
```python
class OrderService:
    def __init__(self, db, inventory_service, payment_service):
        self.db = db
        self.inventory = inventory_service
        self.payment = payment_service
    
    def process_order(self, order_data: dict) -> dict:
        # Validation (pure)
        validation = OrderValidator.validate_order(order_data)
        if not validation["valid"]:
            raise ValidationError(validation["errors"])
        
        # Check inventory (side effect)
        inventory_check = self.inventory.check_availability(order_data["items"])
        if not inventory_check["available"]:
            raise InsufficientInventoryError(inventory_check["missing_items"])
        
        # Calculate totals (pure)
        totals = OrderCalculator.calculate_totals(
            order_data["items"], 
            order_data.get("discount_code")
        )
        
        # Process payment (side effect)
        payment_result = self.payment.process_payment(
            order_data["user_id"], 
            totals["final_total"]
        )
        
        # Save order (side effect)
        order_id = self.db.create_order({
            **order_data,
            "total": totals["final_total"],
            "payment_id": payment_result["id"],
            "status": "confirmed"
        })
        
        # Update inventory (side effect)
        self.inventory.reserve_items(order_data["items"])
        
        return {"order_id": order_id, "total": totals["final_total"]}
```

### Domain Logic (Pure Functions)
```python
class OrderValidator:
    @staticmethod
    def validate_order(order_data: dict) -> dict:
        errors = []
        
        if not order_data.get("items"):
            errors.append("Order must contain items")
        
        for item in order_data.get("items", []):
            if item.get("quantity", 0) <= 0:
                errors.append(f"Invalid quantity for item {item.get('id')}")
        
        if not order_data.get("shipping_address"):
            errors.append("Shipping address required")
            
        return {"valid": len(errors) == 0, "errors": errors}

class OrderCalculator:
    @staticmethod
    def calculate_totals(items: List[dict], discount_code: str = None) -> dict:
        subtotal = sum(
            Decimal(item["price"]) * item["quantity"] 
            for item in items
        )
        
        discount = OrderCalculator._calculate_discount(subtotal, discount_code)
        tax = subtotal * Decimal("0.08")
        shipping = OrderCalculator._calculate_shipping(items)
        
        return {
            "subtotal": subtotal,
            "discount": discount,
            "tax": tax,
            "shipping": shipping,
            "final_total": subtotal - discount + tax + shipping
        }
    
    @staticmethod
    def _calculate_discount(subtotal: Decimal, code: str) -> Decimal:
        # Pure business logic for discounts
        discount_rates = {"SAVE10": 0.1, "SAVE20": 0.2}
        if code in discount_rates:
            return subtotal * Decimal(str(discount_rates[code]))
        return Decimal("0")
```

### SQL Queries
```python
class OrderRepository:
    def create_order(self, order_data: dict) -> str:
        return self.db.execute("""
            INSERT INTO orders (user_id, items, shipping_address, total, status, created_at)
            VALUES (%(user_id)s, %(items)s, %(shipping_address)s, %(total)s, %(status)s, NOW())
            RETURNING id
        """, order_data).fetchone()["id"]
    
    def get_order(self, order_id: str) -> dict:
        return self.db.execute("""
            SELECT o.*, u.email as user_email
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE o.id = %(order_id)s
        """, {"order_id": order_id}).fetchone()
```

## Key Interview Talking Points

### Benefits of Functional Patterns
1. **Testability**: Pure functions are easy to unit test - no mocks needed
2. **Maintainability**: Business logic changes don't affect database/API code
3. **Scalability**: Pure functions can be easily cached, parallelized
4. **Debugging**: Easier to trace bugs when functions don't have hidden side effects
5. **Code Reviews**: Clear separation makes code easier to review

### Senior-Level Questions You Might Face
- "How would you handle database transactions in this functional approach?"
- "What are the performance implications of avoiding mutations?"
- "How do you balance functional purity with practical concerns like caching?"
- "How do you test code that has side effects?"
- "When would you choose functional patterns over object-oriented ones?"

### Trade-offs to Discuss
- **Memory usage**: Creating new objects vs mutating existing ones
- **Performance**: Function call overhead vs inline mutations
- **Complexity**: Sometimes imperative code is more readable
- **Team familiarity**: Not all developers are comfortable with functional patterns

## Best Practices

1. **Keep business logic pure** - separate from I/O operations
2. **Push side effects to the edges** - database calls, API calls, file I/O
3. **Use type hints** - makes functional code more self-documenting
4. **Compose small functions** - easier to test and reason about
5. **Handle errors functionally** - return error states rather than throwing exceptions when possible
6. **Document assumptions** - pure functions should document their constraints

The key is showing you understand the trade-offs and can apply functional principles pragmatically in real systems while maintaining clean architecture.