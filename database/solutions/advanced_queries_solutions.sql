-- Solutions to Advanced SQL Queries Exercise
-- These are reference solutions - try solving exercises/sql/advanced_queries.sql first!

-- Exercise 1: Complex Aggregation (12 minutes)
-- Create a report showing monthly metrics with at least 10 orders
SELECT 
    DATE_TRUNC('month', o.order_date) as month_year,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(o.total_amount) as total_revenue,
    ROUND(AVG(o.total_amount), 2) as avg_order_value,
    COUNT(DISTINCT o.customer_id) as unique_customers
FROM orders o
WHERE o.status != 'cancelled'
GROUP BY DATE_TRUNC('month', o.order_date)
HAVING COUNT(DISTINCT o.order_id) >= 10
ORDER BY month_year DESC;

-- Exercise 2: Self JOIN (10 minutes)
-- Find pairs of customers who live in the same city
SELECT 
    c1.customer_name as customer_1,
    c2.customer_name as customer_2,
    c1.city
FROM customers c1
JOIN customers c2 ON c1.city = c2.city 
    AND c1.customer_id < c2.customer_id  -- Avoid duplicates and self-pairs
WHERE c1.city IS NOT NULL
ORDER BY c1.city, c1.customer_name;

-- Exercise 3: Conditional Logic (8 minutes)
-- Categorize customers based on their total spending
SELECT 
    c.customer_name,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    CASE 
        WHEN COALESCE(SUM(o.total_amount), 0) > 1000 THEN 'High Value'
        WHEN COALESCE(SUM(o.total_amount), 0) BETWEEN 500 AND 1000 THEN 'Medium Value'
        ELSE 'Low Value'
    END as customer_category
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC;

-- Exercise 4: Running Totals (15 minutes)
-- Show daily sales with running totals and percentages
WITH daily_sales AS (
    SELECT 
        DATE(order_date) as sale_date,
        SUM(total_amount) as daily_sales
    FROM orders
    WHERE status != 'cancelled'
    GROUP BY DATE(order_date)
),
sales_with_totals AS (
    SELECT 
        sale_date,
        daily_sales,
        SUM(daily_sales) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total,
        SUM(daily_sales) OVER () as total_sales
    FROM daily_sales
)
SELECT 
    sale_date,
    daily_sales,
    running_total,
    ROUND((running_total * 100.0 / total_sales), 2) as pct_of_total
FROM sales_with_totals
ORDER BY sale_date;

-- Exercise 5: Top N per Group (12 minutes)
-- Find the top 2 best-selling products in each category
WITH product_sales AS (
    SELECT 
        c.category_name,
        p.product_name,
        SUM(oi.quantity) as total_quantity_sold,
        ROW_NUMBER() OVER (PARTITION BY c.category_name ORDER BY SUM(oi.quantity) DESC) as rank_in_category
    FROM categories c
    JOIN products p ON c.category_id = p.category_id
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY c.category_name, p.product_name
)
SELECT 
    category_name,
    product_name,
    total_quantity_sold,
    rank_in_category
FROM product_sales
WHERE rank_in_category <= 2
ORDER BY category_name, rank_in_category;

-- Exercise 6: Data Quality Check (8 minutes)
-- Find potential data issues
-- Negative quantities
SELECT 'Negative Quantities' as issue_type, COUNT(*) as issue_count
FROM order_items 
WHERE quantity < 0

UNION ALL

-- Orders with null customer_id
SELECT 'Orders with Null Customer' as issue_type, COUNT(*) as issue_count
FROM orders 
WHERE customer_id IS NULL

UNION ALL

-- Customers with duplicate email addresses
SELECT 'Duplicate Customer Emails' as issue_type, COUNT(*) - COUNT(DISTINCT email) as issue_count
FROM customers

UNION ALL

-- Products with price = 0
SELECT 'Products with Zero Price' as issue_type, COUNT(*) as issue_count
FROM products 
WHERE price = 0

UNION ALL

-- Orders with mismatched totals
SELECT 'Order Total Mismatches' as issue_type, COUNT(*) as issue_count
FROM (
    SELECT 
        o.order_id,
        o.total_amount as order_total,
        COALESCE(SUM(oi.total_price), 0) as calculated_total
    FROM orders o
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id, o.total_amount
    HAVING ABS(o.total_amount - COALESCE(SUM(oi.total_price), 0)) > 0.01
) mismatches;

-- Detailed view of issues for investigation
SELECT 'DETAILED ISSUES BELOW' as separator;

-- Show actual negative quantity records
SELECT 'Negative Quantities:' as issue_detail, order_id, product_id, quantity
FROM order_items 
WHERE quantity < 0;

-- Show products with zero price
SELECT 'Zero Price Products:' as issue_detail, product_id, product_name, price
FROM products 
WHERE price = 0;