-- Sample E-commerce Database Schema
-- Run this to set up your practice database

-- Create database (run this separately first)
-- CREATE DATABASE interview_practice;

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- Customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50) DEFAULT 'USA',
    registration_date DATE DEFAULT CURRENT_DATE,
    preferences JSONB DEFAULT '{}'
);

-- Categories table
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Products table  
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category_id INTEGER REFERENCES categories(category_id),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    cost DECIMAL(10,2) CHECK (cost >= 0),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0),
    description TEXT,
    average_rating DECIMAL(3,2) CHECK (average_rating >= 0 AND average_rating <= 5),
    created_date DATE DEFAULT CURRENT_DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    tax_amount DECIMAL(10,2) DEFAULT 0,
    shipping_cost DECIMAL(8,2) DEFAULT 0,
    notes TEXT
);

-- Order items table (junction table)
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    total_price DECIMAL(10,2) NOT NULL CHECK (total_price >= 0)
);

-- Create indexes for better query performance
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- Create a function to update product stock
CREATE OR REPLACE FUNCTION update_product_stock()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE products 
        SET stock_quantity = stock_quantity - NEW.quantity
        WHERE product_id = NEW.product_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE products 
        SET stock_quantity = stock_quantity + OLD.quantity
        WHERE product_id = OLD.product_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update stock on order creation/cancellation
CREATE TRIGGER trg_update_stock
    AFTER INSERT OR DELETE ON order_items
    FOR EACH ROW
    EXECUTE FUNCTION update_product_stock();

-- Add some constraints and business rules
ALTER TABLE order_items 
ADD CONSTRAINT chk_total_price 
CHECK (total_price = quantity * unit_price);

-- Create views for common queries
CREATE VIEW customer_order_summary AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.email,
    c.city,
    COUNT(DISTINCT o.order_id) as total_orders,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    MAX(o.order_date) as last_order_date,
    MIN(o.order_date) as first_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.email, c.city;

CREATE VIEW product_sales_summary AS
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    p.price,
    p.stock_quantity,
    COALESCE(SUM(oi.quantity), 0) as total_sold,
    COALESCE(SUM(oi.total_price), 0) as total_revenue,
    COUNT(DISTINCT oi.order_id) as order_count
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, c.category_name, p.price, p.stock_quantity;

-- Print success message
SELECT 'Database schema created successfully!' as status;