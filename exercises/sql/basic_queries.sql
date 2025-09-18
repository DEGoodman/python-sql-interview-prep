-- Basic SQL Queries Exercise
-- Time limit: 5-8 minutes per exercise
-- Use the sample e-commerce database schema

-- Exercise 1: Basic SELECT and Filtering (3 minutes)
-- Find all customers from 'New York' who joined after 2023-01-01

select customer_id, city, registration_date
from customers
where city = 'New York'
    and registration_date > '2023-01-01';


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

select 
	date_trunc('month', order_date) as sales_month,
	COUNT(*) as order_count,
	SUM(total_amount) as total_sales
from orders
where extract(year from order_date) = 2023
group by date_trunc('month', order_date)
order by sales_month desc;


-- Exercise 4: Window Functions (8 minutes)
-- Rank customers by their total purchase amount
-- Show customer_name, total_spent, and their rank
select 
    c.customer_name,
    coalesce(SUM(o.total_amount), 0) as total_spent,
    RANK() over (order by coalesce(sum(o.total_amount), 0) desc) as customer_rank
from customers c
left join orders o on c.customer_id = o.customer_id
group by c.customer_id, c.customer_name
order by total_spent desc;


-- Exercise 5: Subqueries (7 minutes)
-- Find customers who have spent more than the average customer

with customer_spending as (
	select 
		c.customer_id,
		c.customer_name,
		coalesce(sum(o.total_amount), 0) as total_spent
	from customers c
	left join orders o on c.customer_id = o.customer_id
	group by c.customer_id, c.customer_name
)
select customer_name, total_spent
from customer_spending
where total_spent > (
	select avg(total_spent)
	from customer_spending 
	where total_spent > 0
)
order by total_spent desc;



-- Exercise 6: Date Functions (4 minutes)
-- Find orders placed in the last 30 days

select
	c.customer_name,
	o.order_id,
	o.order_date
from customers c
left join orders o on c.customer_id = o.customer_id
where o.order_date >= current_date - interval '30 days'
order by o.order_date desc;