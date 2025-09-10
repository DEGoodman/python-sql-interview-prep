-- Solutions to Basic SQL Queries Exercise
-- These are reference solutions - try solving exercises/sql/basic_queries.sql first!

-- Exercise 1: Basic SELECT and Filtering (3 minutes)
-- Find all customers from 'New York' who joined after 2023-01-01
SELECT customer_id, customer_name, email, registration_date
FROM customers 
WHERE city = 'New York' 
  AND registration_date > '2023-01-01';

-- Exercise 2: JOIN Operations (5 minutes)
-- Get all orders with customer name, product name, and order total
-- Include customers even if they haven't placed orders
SELECT 
    c.customer_name,
    p.product_name,
    o.total_amount,
    o.order_date,
    oi.quantity
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
ORDER BY c.customer_name, o.order_date DESC;

-- Exercise 3: Aggregation and GROUP BY (6 minutes)
-- Find the total sales amount by month for 2023
-- Order by month descending
SELECT 
    DATE_TRUNC('month', order_date) as sales_month,
    COUNT(*) as order_count,
    SUM(total_amount) as total_sales
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2023
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY sales_month DESC;

-- Exercise 4: Window Functions (8 minutes)
-- Rank customers by their total purchase amount
-- Show customer_name, total_spent, and their rank
SELECT 
    c.customer_name,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    RANK() OVER (ORDER BY COALESCE(SUM(o.total_amount), 0) DESC) as customer_rank
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC;

-- Exercise 5: Subqueries (7 minutes)
-- Find customers who have spent more than the average customer
WITH customer_spending AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        COALESCE(SUM(o.total_amount), 0) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT customer_name, total_spent
FROM customer_spending
WHERE total_spent > (
    SELECT AVG(total_spent) 
    FROM customer_spending
    WHERE total_spent > 0
)
ORDER BY total_spent DESC;

-- Exercise 6: Date Functions (4 minutes)
-- Find orders placed in the last 30 days
SELECT 
    o.order_id,
    c.customer_name,
    o.order_date,
    o.total_amount,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY o.order_date DESC;