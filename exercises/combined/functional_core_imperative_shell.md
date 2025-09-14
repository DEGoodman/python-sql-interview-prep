# Functional Core, Imperative Shell Architecture Pattern

## Overview
"Functional Core, Imperative Shell" is an architectural pattern that combines the best of functional and imperative programming. It structures applications to maximize testability, maintainability, and separation of concerns.

## The Core Concept

### Structure
- **Functional Core**: All business logic implemented as pure functions - no side effects, easy to test
- **Imperative Shell**: Thin layer that handles I/O, side effects, and orchestrates the core

### Visual Representation
```
┌─────────────────────────────────────────────────┐
│                IMPERATIVE SHELL                 │
│  ┌─────────────────────────────────────────┐    │
│  │           FUNCTIONAL CORE               │    │
│  │                                         │    │
│  │  • Pure business logic                  │    │
│  │  • No side effects                      │    │
│  │  • Easy to test                         │    │
│  │  • Deterministic                        │    │
│  │                                         │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  • Database calls                               │
│  • API calls                                    │
│  • File I/O                                     │
│  • Orchestration logic                          │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Implementation Example

### Functional Core - Pure Business Logic
```python
class OrderCore:
    @staticmethod
    def calculate_pricing(items, discount_code, user_tier):
        """Pure function - no database calls, no side effects"""
        subtotal = sum(item.price * item.quantity for item in items)
        discount = OrderCore._apply_discount(subtotal, discount_code, user_tier)
        tax = subtotal * 0.08
        return {
            "subtotal": subtotal,
            "discount": discount, 
            "tax": tax,
            "total": subtotal - discount + tax
        }
    
    @staticmethod
    def validate_order(order_data):
        """Pure validation logic"""
        errors = []
        if not order_data.get("items"):
            errors.append("Items required")
        if not order_data.get("shipping_address"):
            errors.append("Shipping address required")
        for item in order_data.get("items", []):
            if item.get("quantity", 0) <= 0:
                errors.append(f"Invalid quantity for item {item.get('id')}")
        return {"valid": len(errors) == 0, "errors": errors}
    
    @staticmethod
    def _apply_discount(subtotal, code, user_tier):
        """Pure discount calculation"""
        base_discount = 0
        
        # Code-based discounts
        if code == "SAVE10":
            base_discount = subtotal * 0.1
        elif code == "SAVE20":
            base_discount = subtotal * 0.2
        
        # Tier-based discounts
        if user_tier == "premium":
            base_discount += subtotal * 0.05
        elif user_tier == "student":
            base_discount = max(base_discount, subtotal * 0.15)
        
        return base_discount

class InventoryCore:
    @staticmethod
    def calculate_reservation_requirements(items):
        """Pure function to determine what needs to be reserved"""
        reservations = {}
        for item in items:
            product_id = item["product_id"]
            quantity = item["quantity"]
            reservations[product_id] = reservations.get(product_id, 0) + quantity
        return reservations
```

### Imperative Shell - Handles All Side Effects
```python
class OrderService:
    def __init__(self, db, payment_gateway, inventory_service, email_service):
        self.db = db
        self.payment_gateway = payment_gateway  
        self.inventory = inventory_service
        self.email = email_service
    
    def process_order(self, order_request):
        """Orchestrates side effects around pure core"""
        # 1. Get data (side effect)
        user = self.db.get_user(order_request.user_id)
        if not user:
            raise UserNotFoundError()
        
        # 2. Pure business logic - no side effects
        validation = OrderCore.validate_order(order_request.dict())
        if not validation["valid"]:
            raise ValidationError(validation["errors"])
        
        pricing = OrderCore.calculate_pricing(
            order_request.items, 
            order_request.discount_code,
            user.tier
        )
        
        reservation_requirements = InventoryCore.calculate_reservation_requirements(
            order_request.items
        )
        
        # 3. More side effects - all orchestrated here
        try:
            # Check and reserve inventory
            self.inventory.check_availability(reservation_requirements)
            reservation_id = self.inventory.reserve_items(reservation_requirements)
            
            # Process payment
            payment_result = self.payment_gateway.charge(
                user.payment_method_id, 
                pricing["total"]
            )
            
            # Save order
            order_id = self.db.save_order({
                "user_id": user.id,
                "items": order_request.items,
                "pricing": pricing,
                "payment_id": payment_result["id"],
                "reservation_id": reservation_id,
                "status": "confirmed"
            })
            
            # Send confirmation email
            self.email.send_order_confirmation(user.email, order_id)
            
            return {"order_id": order_id, "total": pricing["total"]}
            
        except Exception as e:
            # Cleanup on failure
            if 'reservation_id' in locals():
                self.inventory.release_reservation(reservation_id)
            raise
```

### API Layer (Also Part of Imperative Shell)
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
    """HTTP boundary - part of imperative shell"""
    try:
        result = order_service.process_order(request)
        return {"order_id": result["order_id"], "total": result["total"]}
    except ValidationError as e:
        raise HTTPException(400, str(e))
    except UserNotFoundError as e:
        raise HTTPException(404, "User not found")
    except InsufficientInventoryError as e:
        raise HTTPException(409, str(e))
    except PaymentError as e:
        raise HTTPException(402, str(e))
```

## How It Maps to Our Previous Examples

Looking back at our e-commerce example, we actually implemented this pattern:

### Functional Core Components
```python
# Pure business logic - no side effects
- OrderValidator.validate_order()
- OrderCalculator.calculate_totals()  
- PricingEngine.calculate_subscription_price()
- InventoryCore.calculate_reservation_requirements()
```

### Imperative Shell Components
```python
# Orchestration and side effects
- OrderService.process_order()        # Orchestrates I/O and core logic
- API endpoints                       # Handle HTTP requests/responses
- Database repositories               # Handle data persistence
- Email services                      # External communication
- Payment gateways                    # External service calls
```

## Testing Strategy

### Testing the Functional Core
```python
# Easy to test - no mocks needed!
def test_pricing_calculation():
    items = [{"price": 10, "quantity": 2}]
    result = OrderCore.calculate_pricing(items, "SAVE10", "premium")
    
    # Expected: 20 - 2 (SAVE10) - 1 (premium 5%) + 1.36 (tax on discounted amount)
    assert result["subtotal"] == 20
    assert result["discount"] == 3  # 10% + 5% of 20
    assert result["tax"] == 1.36   # 8% of (20 - 3)
    assert result["total"] == 18.36

def test_order_validation():
    invalid_order = {"items": [], "shipping_address": None}
    result = OrderCore.validate_order(invalid_order)
    
    assert not result["valid"]
    assert "Items required" in result["errors"]
    assert "Shipping address required" in result["errors"]

def test_inventory_reservations():
    items = [
        {"product_id": "A", "quantity": 2},
        {"product_id": "B", "quantity": 1},
        {"product_id": "A", "quantity": 1}  # Same product again
    ]
    
    reservations = InventoryCore.calculate_reservation_requirements(items)
    assert reservations == {"A": 3, "B": 1}
```

### Testing the Imperative Shell
```python
# Test the orchestration - mock the boundaries
def test_order_processing_success(mock_db, mock_payment, mock_inventory, mock_email):
    # Arrange
    mock_db.get_user.return_value = {"id": "user_123", "tier": "premium", "email": "test@example.com"}
    mock_inventory.check_availability.return_value = True
    mock_inventory.reserve_items.return_value = "reservation_123"
    mock_payment.charge.return_value = {"id": "payment_123"}
    mock_db.save_order.return_value = "order_123"
    
    service = OrderService(mock_db, mock_payment, mock_inventory, mock_email)
    
    # Act
    order_request = OrderRequest(
        user_id="user_123",
        items=[{"product_id": "A", "price": 10, "quantity": 2}],
        shipping_address={"street": "123 Main St"}
    )
    
    result = service.process_order(order_request)
    
    # Assert
    assert result["order_id"] == "order_123"
    mock_inventory.check_availability.assert_called_once()
    mock_payment.charge.assert_called_once()
    mock_email.send_order_confirmation.assert_called_once()

def test_order_processing_payment_failure(mock_db, mock_payment, mock_inventory):
    # Test that reservations are cleaned up on payment failure
    mock_db.get_user.return_value = {"id": "user_123", "tier": "basic"}
    mock_inventory.reserve_items.return_value = "reservation_123"
    mock_payment.charge.side_effect = PaymentError("Card declined")
    
    service = OrderService(mock_db, mock_payment, mock_inventory, None)
    
    with pytest.raises(PaymentError):
        service.process_order(order_request)
    
    # Verify cleanup happened
    mock_inventory.release_reservation.assert_called_with("reservation_123")
```

## Benefits of This Architecture

### 1. Testability
- **Functional Core**: No mocks needed, fast unit tests
- **Imperative Shell**: Mock external dependencies, test orchestration

### 2. Maintainability
- **Business logic changes**: Only affect the functional core
- **Integration changes**: Only affect the imperative shell
- **Clear separation of concerns**

### 3. Scalability
- **Pure functions**: Easy to cache, parallelize, distribute
- **Side effects isolated**: Easier to optimize I/O operations

### 4. Debugging
- **Deterministic core**: Same input always produces same output
- **Side effects tracked**: All I/O happens in known places

### 5. Code Reviews
- **Business logic**: Easy to review pure functions
- **Integration logic**: Clear orchestration flow

## Relation to Other Architectural Patterns

### Hexagonal Architecture (Ports & Adapters)
```python
# Hexagonal Architecture mapping:
# - Functional Core = Domain layer (business logic)
# - Imperative Shell = Application layer (orchestration) + Infrastructure layer (I/O)

# The functional core contains your domain entities and business rules
# The imperative shell contains your ports, adapters, and application services
```

### Clean Architecture
```python
# Clean Architecture mapping:  
# - Functional Core = Use Cases + Entities
# - Imperative Shell = Controllers + Gateways + External interfaces

# Dependencies point inward: Shell depends on Core, never the reverse
```

### Domain-Driven Design (DDD)
```python
# DDD mapping:
# - Functional Core = Domain Services + Value Objects + Domain Logic
# - Imperative Shell = Application Services + Infrastructure + Repositories

# The core captures the ubiquitous language and domain concepts
# The shell handles technical concerns and external integration
```

## When to Use This Pattern

### Ideal Scenarios
- **Complex business logic** that needs extensive testing
- **Applications where business rules change frequently**
- **Systems that integrate with multiple external services**
- **Domain-rich applications** with complex calculations or validations
- **Applications requiring high reliability** where bugs in business logic are costly

### When It Might Be Overkill
- **Simple CRUD applications** with minimal business logic
- **Prototypes or small scripts** where quick iteration is more important
- **When the team isn't familiar** with functional programming concepts
- **Very simple applications** where the overhead doesn't justify the benefits

## Best Practices

### 1. Keep the Core Pure
```python
# ✅ Good - Pure function
def calculate_discount(amount, user_tier, promo_code):
    return amount * get_discount_rate(user_tier, promo_code)

# ❌ Bad - Has side effects
def calculate_discount(amount, user_id, promo_code):
    user = database.get_user(user_id)  # Side effect!
    return amount * get_discount_rate(user.tier, promo_code)
```

### 2. Make the Shell Thin
```python
# The shell should mostly orchestrate, not contain business logic
def process_order(order_data):
    # Get data
    user = db.get_user(order_data.user_id)
    
    # Call core logic
    result = OrderCore.process(order_data, user)
    
    # Handle side effects
    if result.success:
        db.save_order(result.order)
        email.send_confirmation(result.order)
    
    return result
```

### 3. Use Dependency Injection
```python
# Makes testing easier and keeps dependencies clear
class OrderService:
    def __init__(self, db: DatabaseInterface, payment: PaymentInterface):
        self.db = db
        self.payment = payment
```

### 4. Handle Errors Functionally in Core
```python
# Return error states rather than throwing exceptions in core
def validate_order(order_data):
    if not order_data.items:
        return ValidationResult(valid=False, errors=["No items"])
    return ValidationResult(valid=True, errors=[])
```

## Common Pitfalls

1. **Leaking side effects into the core** - Keep I/O operations in the shell
2. **Making the shell too thick** - Business logic belongs in the core
3. **Not using dependency injection** - Makes testing harder
4. **Ignoring error handling patterns** - Plan how errors flow between layers
5. **Over-engineering simple applications** - Not every app needs this pattern

## Conclusion

The "Functional Core, Imperative Shell" pattern provides a pragmatic way to get the benefits of functional programming while still handling real-world concerns like databases, APIs, and external services. It's particularly valuable for applications with complex business logic that need to be thoroughly tested and maintained over time.

The pattern aligns well with other established architectural patterns and provides a clear separation of concerns that makes code easier to understand, test, and modify.