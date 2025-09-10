-- Sample Data for Interview Practice
-- Run this after creating the schema

-- Insert Categories
INSERT INTO categories (category_name, description) VALUES
('Electronics', 'Electronic devices and accessories'),
('Clothing', 'Apparel and fashion items'),
('Books', 'Books and educational materials'),
('Home & Garden', 'Home improvement and gardening supplies'),
('Sports', 'Sports equipment and fitness gear'),
('Beauty', 'Beauty and personal care products');

-- Insert Sample Customers
INSERT INTO customers (customer_name, email, phone, city, state, country, registration_date) VALUES
('John Smith', 'john.smith@email.com', '555-0101', 'New York', 'NY', 'USA', '2023-01-15'),
('Sarah Johnson', 'sarah.j@email.com', '555-0102', 'Los Angeles', 'CA', 'USA', '2023-02-20'),
('Mike Davis', 'mike.davis@email.com', '555-0103', 'Chicago', 'IL', 'USA', '2023-03-10'),
('Emily Brown', 'emily.brown@email.com', '555-0104', 'Houston', 'TX', 'USA', '2023-01-25'),
('David Wilson', 'david.w@email.com', '555-0105', 'Phoenix', 'AZ', 'USA', '2023-04-05'),
('Lisa Garcia', 'lisa.garcia@email.com', '555-0106', 'Philadelphia', 'PA', 'USA', '2023-02-14'),
('Robert Miller', 'robert.m@email.com', '555-0107', 'San Antonio', 'TX', 'USA', '2023-03-22'),
('Jennifer Taylor', 'jennifer.t@email.com', '555-0108', 'San Diego', 'CA', 'USA', '2023-01-08'),
('William Anderson', 'william.a@email.com', '555-0109', 'Dallas', 'TX', 'USA', '2023-04-12'),
('Maria Martinez', 'maria.martinez@email.com', '555-0110', 'San Jose', 'CA', 'USA', '2023-02-28');

-- Insert Sample Products
INSERT INTO products (product_name, category_id, price, cost, stock_quantity, description, average_rating) VALUES
-- Electronics
('Wireless Headphones', 1, 99.99, 45.00, 50, 'High-quality wireless bluetooth headphones', 4.5),
('Smartphone Case', 1, 24.99, 8.50, 100, 'Protective case for smartphones', 4.2),
('Laptop Stand', 1, 49.99, 20.00, 25, 'Adjustable aluminum laptop stand', 4.7),
('USB Cable', 1, 12.99, 3.50, 200, 'High-speed USB charging cable', 4.0),
('Bluetooth Speaker', 1, 79.99, 35.00, 30, 'Portable wireless bluetooth speaker', 4.4),

-- Clothing  
('Cotton T-Shirt', 2, 19.99, 8.00, 75, 'Comfortable 100% cotton t-shirt', 4.1),
('Denim Jeans', 2, 59.99, 25.00, 40, 'Classic fit denim jeans', 4.3),
('Running Shoes', 2, 89.99, 40.00, 35, 'Lightweight running shoes', 4.6),
('Winter Jacket', 2, 129.99, 60.00, 20, 'Waterproof winter jacket', 4.5),
('Baseball Cap', 2, 24.99, 10.00, 60, 'Adjustable baseball cap', 4.0),

-- Books
('Python Programming', 3, 39.99, 15.00, 50, 'Complete guide to Python programming', 4.8),
('Data Science Handbook', 3, 49.99, 20.00, 30, 'Comprehensive data science reference', 4.7),
('Web Development Guide', 3, 34.99, 14.00, 40, 'Modern web development techniques', 4.4),
('Machine Learning Basics', 3, 44.99, 18.00, 25, 'Introduction to machine learning', 4.6),
('SQL for Beginners', 3, 29.99, 12.00, 55, 'Learn SQL database programming', 4.3),

-- Home & Garden
('Garden Tools Set', 4, 89.99, 35.00, 15, 'Complete set of gardening tools', 4.5),
('Kitchen Blender', 4, 69.99, 30.00, 20, 'High-power kitchen blender', 4.2),
('Throw Pillow', 4, 19.99, 7.00, 80, 'Decorative throw pillow', 4.0),
('LED Light Bulbs', 4, 14.99, 5.00, 100, 'Energy efficient LED bulbs', 4.4),
('Storage Bins', 4, 29.99, 12.00, 45, 'Clear plastic storage containers', 4.1),

-- Sports
('Yoga Mat', 5, 34.99, 15.00, 40, 'Non-slip exercise yoga mat', 4.6),
('Water Bottle', 5, 16.99, 6.00, 70, 'Insulated stainless steel water bottle', 4.3),
('Resistance Bands', 5, 24.99, 10.00, 55, 'Set of exercise resistance bands', 4.4),
('Dumbbells', 5, 79.99, 35.00, 18, 'Adjustable weight dumbbells', 4.5),
('Tennis Racket', 5, 119.99, 50.00, 12, 'Professional tennis racket', 4.7),

-- Beauty
('Face Moisturizer', 6, 24.99, 8.00, 65, 'Daily face moisturizing cream', 4.2),
('Shampoo', 6, 18.99, 6.50, 90, 'Organic hair shampoo', 4.1),
('Lipstick', 6, 22.99, 7.50, 85, 'Long-lasting matte lipstick', 4.3),
('Sunscreen', 6, 16.99, 5.50, 75, 'SPF 50 sunscreen lotion', 4.4),
('Hair Dryer', 6, 89.99, 40.00, 15, 'Professional hair dryer', 4.5);

-- Insert Sample Orders (with realistic dates throughout 2023)
INSERT INTO orders (customer_id, order_date, status, total_amount, tax_amount, shipping_cost) VALUES
(1, '2023-01-20 10:30:00', 'delivered', 124.98, 10.00, 9.99),
(2, '2023-01-22 14:15:00', 'delivered', 89.99, 7.20, 5.99),
(1, '2023-02-05 09:45:00', 'delivered', 79.98, 6.40, 5.99),
(3, '2023-02-10 16:20:00', 'delivered', 149.97, 12.00, 9.99),
(4, '2023-02-15 11:30:00', 'delivered', 44.99, 3.60, 5.99),
(5, '2023-03-01 13:45:00', 'delivered', 139.98, 11.20, 9.99),
(2, '2023-03-05 10:15:00', 'delivered', 69.99, 5.60, 5.99),
(6, '2023-03-12 15:30:00', 'delivered', 94.98, 7.60, 5.99),
(7, '2023-03-20 12:00:00', 'delivered', 189.98, 15.20, 12.99),
(8, '2023-04-02 09:30:00', 'delivered', 74.98, 6.00, 5.99),
(3, '2023-04-08 14:45:00', 'delivered', 129.99, 10.40, 9.99),
(9, '2023-04-15 11:15:00', 'delivered', 159.98, 12.80, 9.99),
(10, '2023-04-22 16:30:00', 'delivered', 54.98, 4.40, 5.99),
(1, '2023-05-05 10:00:00', 'shipped', 109.98, 8.80, 7.99),
(4, '2023-05-10 13:20:00', 'confirmed', 89.99, 7.20, 5.99);

-- Insert Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
-- Order 1: John Smith
(1, 1, 1, 99.99, 99.99),   -- Wireless Headphones
(1, 4, 1, 12.99, 12.99),   -- USB Cable
(1, 18, 1, 12.00, 12.00),  -- LED Light Bulbs (discounted)

-- Order 2: Sarah Johnson  
(2, 8, 1, 89.99, 89.99),   -- Running Shoes

-- Order 3: John Smith (repeat customer)
(3, 6, 2, 19.99, 39.98),   -- Cotton T-Shirts x2
(3, 21, 1, 34.99, 34.99),  -- Yoga Mat
(3, 22, 1, 16.99, 16.99),  -- Water Bottle (discounted)

-- Order 4: Mike Davis
(4, 11, 1, 39.99, 39.99),  -- Python Programming
(4, 12, 1, 49.99, 49.99),  -- Data Science Handbook
(4, 15, 1, 29.99, 29.99),  -- SQL for Beginners

-- Order 5: Emily Brown
(5, 14, 1, 44.99, 44.99),  -- Machine Learning Basics

-- Order 6: David Wilson
(6, 9, 1, 129.99, 129.99), -- Winter Jacket
(6, 10, 1, 24.99, 24.99),  -- Baseball Cap (discounted)

-- Order 7: Sarah Johnson (repeat)
(7, 17, 1, 69.99, 69.99),  -- Kitchen Blender

-- Order 8: Lisa Garcia
(8, 2, 2, 24.99, 49.98),   -- Smartphone Cases x2
(8, 3, 1, 49.99, 49.99),   -- Laptop Stand

-- Order 9: Robert Miller
(9, 24, 1, 119.99, 119.99), -- Tennis Racket
(9, 23, 1, 79.99, 79.99),   -- Dumbbells

-- Order 10: Jennifer Taylor
(10, 25, 2, 24.99, 49.98), -- Face Moisturizer x2
(10, 27, 1, 22.99, 22.99), -- Lipstick

-- Order 11: Mike Davis (repeat)
(11, 9, 1, 129.99, 129.99), -- Winter Jacket

-- Order 12: William Anderson
(12, 5, 1, 79.99, 79.99),   -- Bluetooth Speaker
(13, 13, 1, 34.99, 34.99),  -- Web Development Guide
(12, 20, 1, 29.99, 29.99),  -- Storage Bins

-- Order 13: Maria Martinez
(13, 7, 1, 59.99, 59.99),   -- Denim Jeans

-- Order 14: John Smith (3rd order)
(14, 16, 1, 89.99, 89.99),  -- Garden Tools Set
(14, 19, 1, 19.99, 19.99),  -- Throw Pillow

-- Order 15: Emily Brown (repeat)
(15, 5, 1, 79.99, 79.99);   -- Bluetooth Speaker

-- Update some product stock quantities to reflect sales
UPDATE products SET last_updated = CURRENT_TIMESTAMP;

-- Add some customer preferences
UPDATE customers SET preferences = '{"newsletter": true, "categories": ["Electronics", "Books"]}' WHERE customer_id = 1;
UPDATE customers SET preferences = '{"newsletter": false, "categories": ["Clothing", "Beauty"]}' WHERE customer_id = 2;
UPDATE customers SET preferences = '{"newsletter": true, "categories": ["Books", "Sports"]}' WHERE customer_id = 3;

-- Print completion message
SELECT 'Sample data inserted successfully!' as status,
       (SELECT COUNT(*) FROM customers) as customers_count,
       (SELECT COUNT(*) FROM products) as products_count,
       (SELECT COUNT(*) FROM orders) as orders_count,
       (SELECT COUNT(*) FROM order_items) as order_items_count;