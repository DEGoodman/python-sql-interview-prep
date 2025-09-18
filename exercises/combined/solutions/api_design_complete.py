"""
Complete Solutions for API Design Exercises
These demonstrate robust API patterns, validation, and error handling
"""

from src.database import Database
from typing import List, Dict, Any, Optional
import json
from datetime import datetime, date
import psycopg2

# Exercise 1: User Management API (15 minutes)
class UserAPI:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user with comprehensive validation."""
        # Validate required fields
        required_fields = ['customer_name', 'email']
        missing_fields = [field for field in required_fields if not user_data.get(field)]

        if missing_fields:
            return format_api_response(False, error=f"Missing required fields: {', '.join(missing_fields)}")

        # Validate email format (basic check)
        email = user_data['email']
        if '@' not in email or '.' not in email:
            return format_api_response(False, error="Invalid email format")

        # Check email uniqueness
        check_query = "SELECT customer_id FROM customers WHERE email = %s"
        existing = self.db.execute_query(check_query, (email,))

        if existing:
            return format_api_response(False, error="Email already exists")

        # Insert new user
        insert_query = """
            INSERT INTO customers (customer_name, email, phone, city, state, country, preferences)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING customer_id
        """

        try:
            result = self.db.execute_query(insert_query, (
                user_data['customer_name'],
                user_data['email'],
                user_data.get('phone'),
                user_data.get('city'),
                user_data.get('state'),
                user_data.get('country', 'USA'),
                json.dumps(user_data.get('preferences', {}))
            ))

            if result:
                user_id = result[0][0]
                return format_api_response(True, data={
                    'user_id': user_id,
                    'message': 'User created successfully'
                })

        except psycopg2.Error as e:
            return format_api_response(False, error=f"Database error: {str(e)}")

        return format_api_response(False, error="Failed to create user")

    def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user profile with order summary using the view."""
        query = """
            SELECT
                c.customer_id,
                c.customer_name,
                c.email,
                c.phone,
                c.city,
                c.state,
                c.country,
                c.registration_date,
                c.preferences,
                cos.total_orders,
                cos.total_spent,
                cos.last_order_date
            FROM customers c
            LEFT JOIN customer_order_summary cos ON c.customer_id = cos.customer_id
            WHERE c.customer_id = %s
        """

        result = self.db.execute_query(query, (user_id,))

        if result:
            row = result[0]
            return {
                'user_id': row[0],
                'customer_name': row[1],
                'email': row[2],
                'phone': row[3],
                'city': row[4],
                'state': row[5],
                'country': row[6],
                'registration_date': row[7].strftime('%Y-%m-%d') if row[7] else None,
                'preferences': json.loads(row[8]) if row[8] else {},
                'order_summary': {
                    'total_orders': row[9] or 0,
                    'total_spent': float(row[10]) if row[10] else 0.0,
                    'last_order_date': row[11].strftime('%Y-%m-%d') if row[11] else None
                }
            }

        return None

    def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]) -> bool:
        """Update user preferences using JSON operations."""
        # First check if user exists
        check_query = "SELECT customer_id FROM customers WHERE customer_id = %s"
        if not self.db.execute_query(check_query, (user_id,)):
            return False

        # Update preferences
        update_query = """
            UPDATE customers
            SET preferences = %s,
                last_updated = CURRENT_TIMESTAMP
            WHERE customer_id = %s
        """

        try:
            result = self.db.execute_query(update_query, (json.dumps(preferences), user_id))
            return result is not None

        except psycopg2.Error:
            return False

# Exercise 2: Order Management API (18 minutes)
class OrderAPI:
    def __init__(self, db: Database):
        self.db = db

    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create order with inventory validation and transaction handling."""
        required_fields = ['customer_id', 'items']
        missing_fields = [field for field in required_fields if not order_data.get(field)]

        if missing_fields:
            return format_api_response(False, error=f"Missing required fields: {', '.join(missing_fields)}")

        customer_id = order_data['customer_id']
        items = order_data['items']  # [{'product_id': 1, 'quantity': 2}, ...]

        if not items:
            return format_api_response(False, error="Order must contain at least one item")

        # Validate customer exists
        customer_check = "SELECT customer_id FROM customers WHERE customer_id = %s"
        if not self.db.execute_query(customer_check, (customer_id,)):
            return format_api_response(False, error="Customer not found")

        # Validate products and check inventory
        product_ids = [item['product_id'] for item in items]
        product_query = """
            SELECT product_id, product_name, price, stock_quantity
            FROM products
            WHERE product_id = ANY(%s)
        """

        products = self.db.execute_query(product_query, (product_ids,))

        if len(products) != len(product_ids):
            return format_api_response(False, error="One or more products not found")

        # Create product lookup and validate inventory
        product_lookup = {p[0]: {'name': p[1], 'price': p[2], 'stock': p[3]} for p in products}

        inventory_errors = []
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']

            if quantity <= 0:
                inventory_errors.append(f"Invalid quantity for product {product_id}")
                continue

            if product_id not in product_lookup:
                inventory_errors.append(f"Product {product_id} not found")
                continue

            if product_lookup[product_id]['stock'] < quantity:
                inventory_errors.append(f"Insufficient stock for product {product_id}")

        if inventory_errors:
            return format_api_response(False, error="; ".join(inventory_errors))

        # Calculate totals
        subtotal = sum(item['quantity'] * product_lookup[item['product_id']]['price'] for item in items)
        tax_rate = 0.08  # 8% tax
        tax_amount = subtotal * tax_rate
        shipping_cost = 10.0 if subtotal < 100 else 0.0
        total_amount = subtotal + tax_amount + shipping_cost

        # Create order (transaction will be handled by the database trigger for stock updates)
        try:
            # Insert order
            order_query = """
                INSERT INTO orders (customer_id, total_amount, tax_amount, shipping_cost, status)
                VALUES (%s, %s, %s, %s, 'confirmed')
                RETURNING order_id
            """

            order_result = self.db.execute_query(order_query, (customer_id, total_amount, tax_amount, shipping_cost))

            if not order_result:
                return format_api_response(False, error="Failed to create order")

            order_id = order_result[0][0]

            # Insert order items
            for item in items:
                product_id = item['product_id']
                quantity = item['quantity']
                unit_price = product_lookup[product_id]['price']
                total_price = quantity * unit_price

                item_query = """
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                """

                self.db.execute_query(item_query, (order_id, product_id, quantity, unit_price, total_price))

            return format_api_response(True, data={
                'order_id': order_id,
                'total_amount': total_amount,
                'tax_amount': tax_amount,
                'shipping_cost': shipping_cost,
                'status': 'confirmed',
                'message': 'Order created successfully'
            })

        except psycopg2.Error as e:
            return format_api_response(False, error=f"Database error: {str(e)}")

    def get_order_status(self, order_id: int) -> Dict[str, Any]:
        """Get comprehensive order details."""
        query = """
            SELECT
                o.order_id,
                o.customer_id,
                c.customer_name,
                o.order_date,
                o.status,
                o.total_amount,
                o.tax_amount,
                o.shipping_cost,
                o.notes
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_id = %s
        """

        order_result = self.db.execute_query(query, (order_id,))

        if not order_result:
            return format_api_response(False, error="Order not found")

        # Get order items
        items_query = """
            SELECT
                oi.product_id,
                p.product_name,
                oi.quantity,
                oi.unit_price,
                oi.total_price
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            WHERE oi.order_id = %s
        """

        items_result = self.db.execute_query(items_query, (order_id,))

        order_row = order_result[0]
        return format_api_response(True, data={
            'order_id': order_row[0],
            'customer_id': order_row[1],
            'customer_name': order_row[2],
            'order_date': order_row[3].strftime('%Y-%m-%d %H:%M:%S'),
            'status': order_row[4],
            'total_amount': float(order_row[5]),
            'tax_amount': float(order_row[6]),
            'shipping_cost': float(order_row[7]),
            'notes': order_row[8],
            'items': [
                {
                    'product_id': item[0],
                    'product_name': item[1],
                    'quantity': item[2],
                    'unit_price': float(item[3]),
                    'total_price': float(item[4])
                }
                for item in items_result
            ] if items_result else []
        })

    def cancel_order(self, order_id: int, reason: str) -> Dict[str, Any]:
        """Cancel order with business rules validation."""
        # Check order exists and current status
        status_query = "SELECT status FROM orders WHERE order_id = %s"
        status_result = self.db.execute_query(status_query, (order_id,))

        if not status_result:
            return format_api_response(False, error="Order not found")

        current_status = status_result[0][0]

        if current_status in ['shipped', 'delivered', 'cancelled']:
            return format_api_response(False, error=f"Cannot cancel order with status: {current_status}")

        # Update order status
        try:
            update_query = """
                UPDATE orders
                SET status = 'cancelled',
                    notes = COALESCE(notes || '; ', '') || 'Cancelled: ' || %s
                WHERE order_id = %s
            """

            result = self.db.execute_query(update_query, (reason, order_id))

            if result is not None:
                # Inventory will be restored by the database trigger when order_items are deleted
                delete_items_query = "DELETE FROM order_items WHERE order_id = %s"
                self.db.execute_query(delete_items_query, (order_id,))

                return format_api_response(True, data={
                    'order_id': order_id,
                    'status': 'cancelled',
                    'message': 'Order cancelled successfully'
                })

        except psycopg2.Error as e:
            return format_api_response(False, error=f"Database error: {str(e)}")

        return format_api_response(False, error="Failed to cancel order")

    def get_orders_by_date_range(self, start_date: str, end_date: str,
                                status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get orders with flexible filtering."""
        base_query = """
            SELECT
                o.order_id,
                o.customer_id,
                c.customer_name,
                o.order_date,
                o.status,
                o.total_amount
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE DATE(o.order_date) BETWEEN %s AND %s
        """

        params = [start_date, end_date]

        if status:
            base_query += " AND o.status = %s"
            params.append(status)

        base_query += " ORDER BY o.order_date DESC"

        result = self.db.execute_query(base_query, params)

        if result:
            return [
                {
                    'order_id': row[0],
                    'customer_id': row[1],
                    'customer_name': row[2],
                    'order_date': row[3].strftime('%Y-%m-%d %H:%M:%S'),
                    'status': row[4],
                    'total_amount': float(row[5])
                }
                for row in result
            ]

        return []

# Exercise 3: Product Search API (16 minutes)
class ProductSearchAPI:
    def __init__(self, db: Database):
        self.db = db

    def search_products(self, query: str, category: Optional[str] = None,
                       min_price: Optional[float] = None, max_price: Optional[float] = None,
                       sort_by: str = 'relevance', page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Advanced product search with full-text search simulation."""

        # Base query with text search simulation
        base_query = """
            SELECT
                p.product_id,
                p.product_name,
                p.description,
                p.price,
                p.stock_quantity,
                p.average_rating,
                c.category_name,
                -- Simple relevance scoring
                CASE
                    WHEN LOWER(p.product_name) LIKE LOWER(%s) THEN 3
                    WHEN LOWER(p.description) LIKE LOWER(%s) THEN 2
                    ELSE 1
                END as relevance_score
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE (
                LOWER(p.product_name) LIKE LOWER(%s)
                OR LOWER(p.description) LIKE LOWER(%s)
            )
        """

        # Build dynamic WHERE clauses
        where_conditions = []
        params = [f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%']

        if category:
            where_conditions.append("c.category_name = %s")
            params.append(category)

        if min_price is not None:
            where_conditions.append("p.price >= %s")
            params.append(min_price)

        if max_price is not None:
            where_conditions.append("p.price <= %s")
            params.append(max_price)

        if where_conditions:
            base_query += " AND " + " AND ".join(where_conditions)

        # Add sorting
        sort_options = {
            'relevance': 'relevance_score DESC, p.product_name',
            'price_asc': 'p.price ASC',
            'price_desc': 'p.price DESC',
            'rating': 'p.average_rating DESC NULLS LAST',
            'popularity': 'p.product_id ASC'  # Simplified - could use sales data
        }

        order_by = sort_options.get(sort_by, sort_options['relevance'])
        base_query += f" ORDER BY {order_by}"

        # Get total count for pagination
        count_query = f"SELECT COUNT(*) FROM ({base_query}) as search_results"
        count_result = self.db.execute_query(count_query, params)
        total_count = count_result[0][0] if count_result else 0

        # Add pagination
        offset = (page - 1) * page_size
        base_query += " LIMIT %s OFFSET %s"
        params.extend([page_size, offset])

        # Execute search
        result = self.db.execute_query(base_query, params)

        products = []
        if result:
            products = [
                {
                    'product_id': row[0],
                    'product_name': row[1],
                    'description': row[2],
                    'price': float(row[3]),
                    'stock_quantity': row[4],
                    'average_rating': float(row[5]) if row[5] else None,
                    'category': row[6],
                    'relevance_score': row[7]
                }
                for row in result
            ]

        # Generate pagination info
        pagination = paginate_results(total_count, page, page_size)

        return {
            'products': products,
            'total_count': total_count,
            'pagination': pagination,
            'search_query': query,
            'filters': {
                'category': category,
                'min_price': min_price,
                'max_price': max_price,
                'sort_by': sort_by
            }
        }

    def get_product_recommendations(self, product_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Product recommendations using multiple strategies."""
        query = """
            WITH target_product AS (
                SELECT category_id, price
                FROM products
                WHERE product_id = %s
            ),
            category_similar AS (
                SELECT p.product_id, p.product_name, p.price, p.average_rating,
                       1 as recommendation_type, 'Same category' as reason
                FROM products p, target_product tp
                WHERE p.category_id = tp.category_id
                  AND p.product_id != %s
            ),
            price_similar AS (
                SELECT p.product_id, p.product_name, p.price, p.average_rating,
                       2 as recommendation_type, 'Similar price' as reason
                FROM products p, target_product tp
                WHERE ABS(p.price - tp.price) <= tp.price * 0.3
                  AND p.product_id != %s
                  AND p.category_id != tp.category_id
            ),
            frequently_bought AS (
                SELECT p.product_id, p.product_name, p.price, p.average_rating,
                       3 as recommendation_type, 'Frequently bought together' as reason
                FROM products p
                WHERE p.product_id IN (
                    SELECT DISTINCT oi2.product_id
                    FROM order_items oi1
                    JOIN order_items oi2 ON oi1.order_id = oi2.order_id
                    WHERE oi1.product_id = %s AND oi2.product_id != %s
                )
            )
            SELECT DISTINCT product_id, product_name, price, average_rating, reason
            FROM (
                SELECT * FROM category_similar
                UNION ALL
                SELECT * FROM price_similar
                UNION ALL
                SELECT * FROM frequently_bought
            ) recommendations
            ORDER BY recommendation_type, average_rating DESC NULLS LAST
            LIMIT %s
        """

        result = self.db.execute_query(query, (product_id, product_id, product_id, product_id, product_id, limit))

        if result:
            return [
                {
                    'product_id': row[0],
                    'product_name': row[1],
                    'price': float(row[2]),
                    'average_rating': float(row[3]) if row[3] else None,
                    'recommendation_reason': row[4]
                }
                for row in result
            ]

        return []

    def update_product_inventory(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk inventory update with validation."""
        results = []
        successful_updates = 0

        for update in updates:
            product_id = update.get('product_id')
            quantity = update.get('quantity')

            if not product_id or quantity is None:
                results.append({
                    'product_id': product_id,
                    'success': False,
                    'error': 'Missing product_id or quantity'
                })
                continue

            if quantity < 0:
                results.append({
                    'product_id': product_id,
                    'success': False,
                    'error': 'Quantity cannot be negative'
                })
                continue

            try:
                # Check if product exists
                check_query = "SELECT product_id FROM products WHERE product_id = %s"
                if not self.db.execute_query(check_query, (product_id,)):
                    results.append({
                        'product_id': product_id,
                        'success': False,
                        'error': 'Product not found'
                    })
                    continue

                # Update inventory
                update_query = """
                    UPDATE products
                    SET stock_quantity = %s,
                        last_updated = CURRENT_TIMESTAMP
                    WHERE product_id = %s
                """

                result = self.db.execute_query(update_query, (quantity, product_id))

                if result is not None:
                    results.append({
                        'product_id': product_id,
                        'success': True,
                        'new_quantity': quantity
                    })
                    successful_updates += 1
                else:
                    results.append({
                        'product_id': product_id,
                        'success': False,
                        'error': 'Update failed'
                    })

            except psycopg2.Error as e:
                results.append({
                    'product_id': product_id,
                    'success': False,
                    'error': f'Database error: {str(e)}'
                })

        return {
            'total_updates': len(updates),
            'successful_updates': successful_updates,
            'failed_updates': len(updates) - successful_updates,
            'results': results
        }

# Exercise 4: Analytics API (20 minutes)
class AnalyticsAPI:
    def __init__(self, db: Database):
        self.db = db

    def get_dashboard_metrics(self, date_range: str = 'last_30_days') -> Dict[str, Any]:
        """Comprehensive dashboard with growth calculations."""

        # Date range calculation
        date_mappings = {
            'last_7_days': 7,
            'last_30_days': 30,
            'last_90_days': 90,
            'last_365_days': 365
        }

        days = date_mappings.get(date_range, 30)

        query = """
            WITH current_period AS (
                SELECT
                    SUM(total_amount) as current_sales,
                    COUNT(DISTINCT order_id) as current_orders,
                    COUNT(DISTINCT customer_id) as current_customers
                FROM orders
                WHERE order_date >= CURRENT_DATE - INTERVAL '%s days'
            ),
            previous_period AS (
                SELECT
                    SUM(total_amount) as previous_sales,
                    COUNT(DISTINCT order_id) as previous_orders,
                    COUNT(DISTINCT customer_id) as previous_customers
                FROM orders
                WHERE order_date >= CURRENT_DATE - INTERVAL '%s days'
                  AND order_date < CURRENT_DATE - INTERVAL '%s days'
            ),
            top_products AS (
                SELECT
                    p.product_name,
                    SUM(oi.total_price) as revenue
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                JOIN products p ON oi.product_id = p.product_id
                WHERE o.order_date >= CURRENT_DATE - INTERVAL '%s days'
                GROUP BY p.product_id, p.product_name
                ORDER BY revenue DESC
                LIMIT 5
            ),
            top_categories AS (
                SELECT
                    c.category_name,
                    SUM(oi.total_price) as revenue
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                JOIN products p ON oi.product_id = p.product_id
                JOIN categories c ON p.category_id = c.category_id
                WHERE o.order_date >= CURRENT_DATE - INTERVAL '%s days'
                GROUP BY c.category_id, c.category_name
                ORDER BY revenue DESC
                LIMIT 5
            ),
            geographic_data AS (
                SELECT
                    c.city,
                    SUM(o.total_amount) as revenue,
                    COUNT(DISTINCT o.order_id) as orders
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                WHERE o.order_date >= CURRENT_DATE - INTERVAL '%s days'
                  AND c.city IS NOT NULL
                GROUP BY c.city
                ORDER BY revenue DESC
                LIMIT 10
            )
            SELECT
                cp.current_sales,
                cp.current_orders,
                cp.current_customers,
                pp.previous_sales,
                pp.previous_orders,
                pp.previous_customers
            FROM current_period cp, previous_period pp
        """

        # Execute main metrics query
        main_result = self.db.execute_query(query, (days, days * 2, days, days, days, days))

        # Get top products
        top_products_query = """
            SELECT p.product_name, SUM(oi.total_price) as revenue
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.order_date >= CURRENT_DATE - INTERVAL '%s days'
            GROUP BY p.product_id, p.product_name
            ORDER BY revenue DESC
            LIMIT 5
        """

        top_products = self.db.execute_query(top_products_query, (days,))

        # Get geographic distribution
        geo_query = """
            SELECT c.city, SUM(o.total_amount) as revenue, COUNT(DISTINCT o.order_id) as orders
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_date >= CURRENT_DATE - INTERVAL '%s days'
              AND c.city IS NOT NULL
            GROUP BY c.city
            ORDER BY revenue DESC
            LIMIT 10
        """

        geo_data = self.db.execute_query(geo_query, (days,))

        if main_result:
            row = main_result[0]
            current_sales = float(row[0]) if row[0] else 0
            current_orders = row[1] or 0
            current_customers = row[2] or 0
            previous_sales = float(row[3]) if row[3] else 0
            previous_orders = row[4] or 0
            previous_customers = row[5] or 0

            # Calculate growth rates
            sales_growth = ((current_sales - previous_sales) / previous_sales * 100) if previous_sales > 0 else 0
            orders_growth = ((current_orders - previous_orders) / previous_orders * 100) if previous_orders > 0 else 0
            customers_growth = ((current_customers - previous_customers) / previous_customers * 100) if previous_customers > 0 else 0

            return {
                'date_range': date_range,
                'metrics': {
                    'total_sales': current_sales,
                    'total_orders': current_orders,
                    'total_customers': current_customers,
                    'avg_order_value': current_sales / current_orders if current_orders > 0 else 0
                },
                'growth_rates': {
                    'sales_growth': round(sales_growth, 2),
                    'orders_growth': round(orders_growth, 2),
                    'customers_growth': round(customers_growth, 2)
                },
                'top_products': [
                    {'product_name': row[0], 'revenue': float(row[1])}
                    for row in top_products
                ] if top_products else [],
                'geographic_distribution': [
                    {'city': row[0], 'revenue': float(row[1]), 'orders': row[2]}
                    for row in geo_data
                ] if geo_data else []
            }

        return {}

    def get_customer_lifetime_value(self, customer_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Calculate CLV with predictive component."""
        base_query = """
            WITH customer_metrics AS (
                SELECT
                    c.customer_id,
                    c.customer_name,
                    c.registration_date,
                    COALESCE(SUM(o.total_amount), 0) as total_spent,
                    COUNT(o.order_id) as total_orders,
                    COALESCE(AVG(o.total_amount), 0) as avg_order_value,
                    MAX(o.order_date) as last_order_date,
                    MIN(o.order_date) as first_order_date
                FROM customers c
                LEFT JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id, c.customer_name, c.registration_date
            ),
            customer_clv AS (
                SELECT
                    *,
                    CASE
                        WHEN total_orders = 0 THEN 0
                        WHEN first_order_date IS NULL THEN 0
                        ELSE
                            -- Simple CLV prediction: avg_order_value * predicted_orders_per_year * 2 years
                            avg_order_value *
                            (total_orders / GREATEST(EXTRACT(DAYS FROM (COALESCE(last_order_date, CURRENT_DATE) - first_order_date)) / 365.0, 0.1)) *
                            2
                    END as predicted_clv,
                    CASE
                        WHEN total_orders = 0 THEN 0
                        WHEN first_order_date IS NULL THEN 0
                        ELSE total_orders / GREATEST(EXTRACT(DAYS FROM (COALESCE(last_order_date, CURRENT_DATE) - first_order_date)) / 365.0, 0.1)
                    END as order_frequency_per_year
                FROM customer_metrics
            )
            SELECT
                customer_id,
                customer_name,
                total_spent,
                total_orders,
                avg_order_value,
                order_frequency_per_year,
                predicted_clv,
                last_order_date
            FROM customer_clv
        """

        params = []
        if customer_id:
            base_query += " WHERE customer_id = %s"
            params.append(customer_id)

        base_query += " ORDER BY predicted_clv DESC LIMIT 100"

        result = self.db.execute_query(base_query, params)

        if result:
            return [
                {
                    'customer_id': row[0],
                    'customer_name': row[1],
                    'total_spent': float(row[2]),
                    'total_orders': row[3],
                    'avg_order_value': float(row[4]),
                    'order_frequency_per_year': round(float(row[5]), 2),
                    'predicted_clv': round(float(row[6]), 2),
                    'last_order_date': row[7].strftime('%Y-%m-%d') if row[7] else None
                }
                for row in result
            ]

        return []

    def generate_sales_report(self, report_type: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Flexible reporting system."""
        if report_type == 'summary':
            query = """
                SELECT
                    COUNT(DISTINCT order_id) as total_orders,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_order_value,
                    MIN(total_amount) as min_order_value,
                    MAX(total_amount) as max_order_value
                FROM orders
                WHERE DATE(order_date) BETWEEN %s AND %s
            """

            result = self.db.execute_query(query, (start_date, end_date))

            if result:
                row = result[0]
                return {
                    'report_type': 'summary',
                    'period': f"{start_date} to {end_date}",
                    'metrics': {
                        'total_orders': row[0] or 0,
                        'unique_customers': row[1] or 0,
                        'total_revenue': float(row[2]) if row[2] else 0,
                        'avg_order_value': float(row[3]) if row[3] else 0,
                        'min_order_value': float(row[4]) if row[4] else 0,
                        'max_order_value': float(row[5]) if row[5] else 0
                    }
                }

        elif report_type == 'detailed':
            query = """
                SELECT
                    o.order_id,
                    o.order_date,
                    c.customer_name,
                    o.total_amount,
                    o.status,
                    COUNT(oi.order_item_id) as item_count
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                LEFT JOIN order_items oi ON o.order_id = oi.order_id
                WHERE DATE(o.order_date) BETWEEN %s AND %s
                GROUP BY o.order_id, o.order_date, c.customer_name, o.total_amount, o.status
                ORDER BY o.order_date DESC
                LIMIT 1000
            """

            result = self.db.execute_query(query, (start_date, end_date))

            if result:
                return {
                    'report_type': 'detailed',
                    'period': f"{start_date} to {end_date}",
                    'orders': [
                        {
                            'order_id': row[0],
                            'order_date': row[1].strftime('%Y-%m-%d %H:%M:%S'),
                            'customer_name': row[2],
                            'total_amount': float(row[3]),
                            'status': row[4],
                            'item_count': row[5]
                        }
                        for row in result
                    ]
                }

        return {'error': 'Invalid report type or no data found'}

# Utility Functions
def validate_input(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """Return list of missing required fields."""
    return [field for field in required_fields if not data.get(field)]

def paginate_results(total_count: int, page: int, page_size: int) -> Dict[str, Any]:
    """Return pagination metadata."""
    total_pages = (total_count + page_size - 1) // page_size
    has_next = page < total_pages
    has_prev = page > 1

    return {
        'current_page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'total_count': total_count,
        'has_next': has_next,
        'has_prev': has_prev,
        'next_page': page + 1 if has_next else None,
        'prev_page': page - 1 if has_prev else None
    }

def format_api_response(success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
    """Standardize API response format."""
    response = {
        'success': success,
        'timestamp': datetime.now().isoformat()
    }

    if success:
        response['data'] = data
    else:
        response['error'] = error

    return response