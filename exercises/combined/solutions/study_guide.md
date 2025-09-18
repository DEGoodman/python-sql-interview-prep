# Interview Exercise Solutions Study Guide

## 🔥 Most Interesting Techniques & Patterns

### 1. **CTEs with UNION ALL for Segmentation** (`segment_customers`)
```sql
WITH frequent_customer AS (...),
     big_spender AS (...),
     at_risk AS (...)
SELECT 'frequent' as segment, customer_name FROM frequent_customer
UNION ALL
SELECT 'big_spender' as segment, customer_name FROM big_spender
```

**Why it's brilliant:**
- Single query returns all segments labeled
- Python groups results efficiently: `customer_segments[segment].append(customer_name)`
- Much faster than separate queries
- **Interview gold:** Shows advanced SQL + clean Python processing

### 2. **Window Functions for Growth Rates** (`monthly_trends`)
```sql
WITH monthly_data AS (...),
     with_growth AS (
         SELECT *, LAG(revenue) OVER (ORDER BY month) as prev_revenue
         FROM monthly_data
     )
SELECT ..., ((revenue - prev_revenue) / prev_revenue) * 100 as growth_rate
```

**Why it's powerful:**
- Calculates month-over-month growth in SQL
- `LAG()` gets previous row value
- **Alternative:** Could use self-join, but window functions are cleaner

### 3. **Statistical Anomaly Detection** (`detect_anomalies`)
```sql
WITH daily_sales AS (...),
     stats AS (
         SELECT AVG(daily_revenue) as mean_revenue,
                STDDEV(daily_revenue) as stddev_revenue
         FROM daily_sales
     )
SELECT *, ABS(daily_revenue - mean_revenue) / stddev_revenue as z_score
WHERE z_score > 2
```

**Why it's impressive:**
- Real statistical analysis in SQL
- Z-score calculation for outlier detection
- Shows data science knowledge

### 4. **Pareto Analysis (ABC Classification)** (`abc_analysis`)
```sql
WITH product_revenue AS (...),
     with_percentiles AS (
         SELECT *,
                SUM(total_revenue) OVER() as total_all_revenue,
                SUM(total_revenue) OVER(ORDER BY total_revenue DESC) as running_revenue
         FROM product_revenue
     )
SELECT CASE
    WHEN (running_revenue / total_all_revenue) * 100 <= 80 THEN 'A'
    WHEN (running_revenue / total_all_revenue) * 100 <= 95 THEN 'B'
    ELSE 'C'
END as abc_class
```

**Why it's advanced:**
- Running totals with window functions
- Business intelligence classification
- Shows understanding of inventory management

### 5. **Comprehensive API Error Handling** (`create_order`)
```python
# Multi-stage validation
if missing_fields:
    return format_api_response(False, error=f"Missing: {', '.join(missing_fields)}")

# Business logic validation
inventory_errors = []
for item in items:
    if product_lookup[product_id]['stock'] < quantity:
        inventory_errors.append(f"Insufficient stock for product {product_id}")

if inventory_errors:
    return format_api_response(False, error="; ".join(inventory_errors))
```

**Why it's excellent:**
- Validates at multiple levels
- Collects all errors before returning
- Standardized response format
- Real-world API patterns

## 🎯 Alternative Approaches for Study

### Retention Rate Calculation

**Primary Approach (Intersection):**
```sql
-- Using INNER JOIN to find intersection
SELECT COUNT(*) FROM customers_months_back cmb
INNER JOIN customers_recent cr ON cmb.customer_id = cr.customer_id
```

**Alternative 1 (EXISTS):**
```sql
SELECT COUNT(DISTINCT customer_id)
FROM orders o1
WHERE o1.order_date BETWEEN date1 AND date2
  AND EXISTS (
      SELECT 1 FROM orders o2
      WHERE o2.customer_id = o1.customer_id
        AND o2.order_date >= CURRENT_DATE - INTERVAL '1 month'
  )
```

**Alternative 2 (Window Functions):**
```sql
WITH customer_orders AS (
    SELECT customer_id,
           order_date,
           LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_order
    FROM orders
)
-- Complex logic to find retention patterns
```

### Product Search Implementation

**Primary Approach (Dynamic SQL):**
```python
where_conditions = []
if category:
    where_conditions.append("c.category_name = %s")
if where_conditions:
    base_query += " AND " + " AND ".join(where_conditions)
```

**Alternative 1 (ORM-style Query Builder):**
```python
# Would use SQLAlchemy or similar
query = session.query(Product).join(Category)
if category:
    query = query.filter(Category.name == category)
if min_price:
    query = query.filter(Product.price >= min_price)
```

**Alternative 2 (Prepared Statements):**
```sql
-- Fixed query with CASE statements
WHERE (category_filter IS NULL OR c.category_name = category_filter)
  AND (min_price_filter IS NULL OR p.price >= min_price_filter)
```

### Inventory Reorder Logic

**Primary Approach (Sales Velocity):**
```sql
SELECT stock_quantity / avg_daily_sales as days_until_stockout
```

**Alternative 1 (Safety Stock Model):**
```sql
SELECT
    CASE
        WHEN stock_quantity <= (avg_daily_sales * lead_time_days + safety_stock)
        THEN 'reorder_now'
        ELSE 'sufficient'
    END as reorder_status
```

**Alternative 2 (Economic Order Quantity):**
```python
import math
def calculate_eoq(annual_demand, ordering_cost, holding_cost):
    return math.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
```

## 💡 Study Tips for Tonight

### 1. **Memorize Key Patterns**
- CTE + UNION ALL for multi-segment queries
- Window functions: `LAG()`, `SUM() OVER()`, `ROW_NUMBER()`
- Dynamic WHERE clause building
- Standardized API response format

### 2. **Common Interview Traps**
- **GROUP BY requirements** with aggregate functions
- **Tuple syntax** for single parameters: `(limit,)` not `(limit)`
- **LEFT JOIN vs INNER JOIN** for optional relationships
- **Error handling** before database operations

### 3. **SQL Performance Concepts**
- Use existing views when available (`customer_order_summary`)
- Prefer window functions over self-joins
- Add LIMIT to prevent runaway queries
- Use appropriate indexes (already created in schema)

### 4. **Business Logic Validation Order**
1. Input validation (required fields, format)
2. Authorization (user permissions)
3. Business rules (inventory, status checks)
4. Database operations
5. Response formatting

### 5. **Quick Reference Formulas**
```sql
-- Growth rate calculation
((current - previous) / previous) * 100

-- Running total
SUM(amount) OVER (ORDER BY date)

-- Percentile calculation
(running_sum / total_sum) * 100

-- Z-score for anomalies
ABS(value - mean) / stddev > 2
```

## 🚀 Interview Strategy

1. **Start with the simple solution** - get something working first
2. **Explain your approach** - "I'll use CTEs to break this into logical steps"
3. **Handle edge cases** - "Let me add validation for division by zero"
4. **Optimize if time permits** - "We could add an index on order_date for better performance"
5. **Show business understanding** - "This retention rate helps identify customer lifecycle patterns"

Remember: **Working code beats perfect code** in an interview setting. Get the core functionality working, then enhance if time allows.