"""
Complete Solutions for Data Analysis Exercises
These demonstrate advanced SQL techniques and efficient Python processing
"""

from src.database import Database
from typing import List, Dict, Any
import json
from datetime import datetime, timedelta

# Exercise 1: Customer Analytics (15 minutes)
class CustomerAnalytics:
    def __init__(self, db: Database):
        self.db = db

    def get_top_customers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Find top customers by total purchase amount."""
        query = """
            SELECT
                c.customer_name,
                COALESCE(SUM(o.total_amount), 0) as total_spent,
                COUNT(o.order_id) as order_count
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.customer_name
            ORDER BY total_spent DESC
            LIMIT %s
        """

        rows = self.db.execute_query(query, (limit,))

        if rows:
            return [
                {
                    'customer_name': row[0],
                    'total_spent': float(row[1]),
                    'order_count': row[2]
                }
                for row in rows
            ]
        return []

    def customer_retention_rate(self, months_back: int = 6) -> float:
        """Calculate retention rate using intersection approach."""
        query = """
            WITH customers_months_back AS (
                SELECT DISTINCT customer_id
                FROM orders
                WHERE order_date >= CURRENT_DATE - INTERVAL '%s months' - INTERVAL '1 month'
                    AND order_date < CURRENT_DATE - INTERVAL '%s months'
            ),
            customers_recent AS (
                SELECT DISTINCT customer_id
                FROM orders
                WHERE order_date >= CURRENT_DATE - INTERVAL '1 month'
            ),
            retention_data AS (
                SELECT
                    (SELECT COUNT(*) FROM customers_months_back) as total_past_customers,
                    (SELECT COUNT(*)
                     FROM customers_months_back cmb
                     INNER JOIN customers_recent cr ON cmb.customer_id = cr.customer_id
                    ) AS retained_customers
            )
            SELECT total_past_customers, retained_customers
            FROM retention_data
        """

        result = self.db.execute_query(query, (months_back, months_back))

        if result and result[0][0] > 0:
            total_past, retained = result[0]
            return (retained / total_past) * 100.0
        return 0.0

    def segment_customers(self) -> Dict[str, List[str]]:
        """Advanced customer segmentation using CTEs and UNION ALL."""
        query = """
            WITH frequent_customer AS (
                SELECT customer_name
                FROM customers c
                JOIN orders o ON c.customer_id = o.customer_id
                WHERE o.order_date >= CURRENT_DATE - INTERVAL '6 months'
                GROUP BY c.customer_id, c.customer_name
                HAVING COUNT(o.order_id) > 5
            ),
            big_spender AS (
                SELECT customer_name
                FROM customer_order_summary
                WHERE total_orders > 0
                    AND (total_spent / total_orders) > 200
            ),
            at_risk AS (
                SELECT customer_name
                FROM customer_order_summary
                WHERE total_orders > 0
                    AND last_order_date < CURRENT_DATE - INTERVAL '3 months'
            ),
            new AS (
                SELECT customer_name
                FROM customer_order_summary
                WHERE first_order_date > CURRENT_DATE - INTERVAL '1 month'
            )
            SELECT 'frequent' as segment, customer_name FROM frequent_customer
            UNION ALL
            SELECT 'big_spender' as segment, customer_name FROM big_spender
            UNION ALL
            SELECT 'at_risk' as segment, customer_name FROM at_risk
            UNION ALL
            SELECT 'new' as segment, customer_name FROM new
        """

        customer_segments = {'frequent': [], 'big_spender': [], 'at_risk': [], 'new': []}
        result = self.db.execute_query(query)

        if result:
            for segment, customer_name in result:
                customer_segments[segment].append(customer_name)

        return customer_segments

# Exercise 2: Sales Performance Dashboard (18 minutes)
class SalesAnalytics:
    def __init__(self, db: Database):
        self.db = db

    def monthly_trends(self, year: int = 2023) -> List[Dict[str, Any]]:
        """Advanced: Calculate growth rates using window functions."""
        query = """
            WITH monthly_data AS (
                SELECT
                    EXTRACT(MONTH FROM order_date) as month,
                    SUM(total_amount) as revenue,
                    COUNT(order_id) as order_count,
                    AVG(total_amount) as avg_order_value
                FROM orders
                WHERE EXTRACT(YEAR FROM order_date) = %s
                GROUP BY EXTRACT(MONTH FROM order_date)
                ORDER BY month
            ),
            with_growth AS (
                SELECT
                    month,
                    revenue,
                    order_count,
                    avg_order_value,
                    LAG(revenue) OVER (ORDER BY month) as prev_revenue
                FROM monthly_data
            )
            SELECT
                month,
                revenue,
                order_count,
                avg_order_value,
                CASE
                    WHEN prev_revenue IS NULL OR prev_revenue = 0 THEN 0
                    ELSE ((revenue - prev_revenue) / prev_revenue) * 100
                END as growth_rate
            FROM with_growth
            ORDER BY month
        """

        rows = self.db.execute_query(query, (year,))

        if rows:
            return [
                {
                    'month': int(row[0]),
                    'revenue': float(row[1]),
                    'order_count': row[2],
                    'avg_order_value': float(row[3]),
                    'growth_rate': float(row[4]) if row[4] else 0.0
                }
                for row in rows
            ]
        return []

    def product_performance(self) -> List[Dict[str, Any]]:
        """Use LEFT JOIN to include products with 0 sales."""
        query = """
            SELECT
                p.product_name,
                c.category_name,
                COALESCE(SUM(oi.total_price), 0) as total_revenue,
                COALESCE(SUM(oi.quantity), 0) as units_sold,
                p.average_rating
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN order_items oi ON p.product_id = oi.product_id
            GROUP BY p.product_id, p.product_name, c.category_name, p.average_rating
            ORDER BY total_revenue DESC
        """

        rows = self.db.execute_query(query)

        if rows:
            return [
                {
                    'product_name': row[0],
                    'category': row[1],
                    'total_revenue': float(row[2]),
                    'units_sold': int(row[3]),
                    'avg_rating': float(row[4]) if row[4] else None
                }
                for row in rows
            ]
        return []

    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Statistical anomaly detection using standard deviation."""
        query = """
            WITH daily_sales AS (
                SELECT
                    DATE(order_date) as sale_date,
                    SUM(total_amount) as daily_revenue
                FROM orders
                WHERE order_date >= CURRENT_DATE - INTERVAL '90 days'
                GROUP BY DATE(order_date)
            ),
            stats AS (
                SELECT
                    AVG(daily_revenue) as mean_revenue,
                    STDDEV(daily_revenue) as stddev_revenue
                FROM daily_sales
            )
            SELECT
                ds.sale_date,
                ds.daily_revenue,
                st.mean_revenue,
                ABS(ds.daily_revenue - st.mean_revenue) / st.stddev_revenue as z_score
            FROM daily_sales ds, stats st
            WHERE ABS(ds.daily_revenue - st.mean_revenue) / st.stddev_revenue > 2
            ORDER BY z_score DESC
        """

        rows = self.db.execute_query(query)

        if rows:
            return [
                {
                    'date': row[0].strftime('%Y-%m-%d'),
                    'daily_revenue': float(row[1]),
                    'mean_revenue': float(row[2]),
                    'z_score': float(row[3]),
                    'anomaly_type': 'spike' if row[1] > row[2] else 'drop'
                }
                for row in rows
            ]
        return []

# Exercise 3: Inventory Optimization (20 minutes)
class InventoryOptimizer:
    def __init__(self, db: Database):
        self.db = db

    def reorder_recommendations(self) -> List[Dict[str, Any]]:
        """Calculate reorder points using sales velocity."""
        query = """
            WITH sales_velocity AS (
                SELECT
                    p.product_id,
                    p.product_name,
                    p.stock_quantity,
                    COALESCE(AVG(oi.quantity), 0) as avg_daily_sales
                FROM products p
                LEFT JOIN order_items oi ON p.product_id = oi.product_id
                LEFT JOIN orders o ON oi.order_id = o.order_id
                WHERE o.order_date >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY p.product_id, p.product_name, p.stock_quantity
            )
            SELECT
                product_id,
                product_name,
                stock_quantity,
                avg_daily_sales,
                CASE
                    WHEN avg_daily_sales > 0 THEN stock_quantity / avg_daily_sales
                    ELSE 999
                END as days_until_stockout
            FROM sales_velocity
            WHERE
                avg_daily_sales > 0
                AND stock_quantity / avg_daily_sales <= 7
            ORDER BY days_until_stockout ASC
        """

        rows = self.db.execute_query(query)

        if rows:
            return [
                {
                    'product_id': row[0],
                    'product_name': row[1],
                    'current_stock': row[2],
                    'avg_daily_sales': float(row[3]),
                    'days_until_stockout': float(row[4]),
                    'recommended_order_qty': int(row[3] * 30)  # 30 days supply
                }
                for row in rows
            ]
        return []

    def abc_analysis(self) -> Dict[str, List[Dict[str, Any]]]:
        """Pareto analysis with running totals."""
        query = """
            WITH product_revenue AS (
                SELECT
                    p.product_id,
                    p.product_name,
                    c.category_name,
                    COALESCE(SUM(oi.total_price), 0) as total_revenue
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN order_items oi ON p.product_id = oi.product_id
                GROUP BY p.product_id, p.product_name, c.category_name
            ),
            with_percentiles AS (
                SELECT
                    *,
                    SUM(total_revenue) OVER() as total_all_revenue,
                    SUM(total_revenue) OVER(ORDER BY total_revenue DESC) as running_revenue
                FROM product_revenue
                WHERE total_revenue > 0
                ORDER BY total_revenue DESC
            ),
            classified AS (
                SELECT
                    *,
                    (running_revenue / total_all_revenue) * 100 as cumulative_percent,
                    CASE
                        WHEN (running_revenue / total_all_revenue) * 100 <= 80 THEN 'A'
                        WHEN (running_revenue / total_all_revenue) * 100 <= 95 THEN 'B'
                        ELSE 'C'
                    END as abc_class
                FROM with_percentiles
            )
            SELECT abc_class, product_name, category_name, total_revenue, cumulative_percent
            FROM classified
            ORDER BY total_revenue DESC
        """

        rows = self.db.execute_query(query)
        result = {'A': [], 'B': [], 'C': []}

        if rows:
            for row in rows:
                abc_class = row[0]
                result[abc_class].append({
                    'product_name': row[1],
                    'category': row[2],
                    'total_revenue': float(row[3]),
                    'cumulative_percent': float(row[4])
                })

        return result

    def slow_moving_products(self, days: int = 90) -> List[Dict[str, Any]]:
        """Find products with inventory but no recent sales."""
        query = """
            SELECT
                p.product_id,
                p.product_name,
                c.category_name,
                p.stock_quantity,
                p.price,
                p.stock_quantity * p.price as inventory_value,
                MAX(o.order_date) as last_sale_date
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN order_items oi ON p.product_id = oi.product_id
            LEFT JOIN orders o ON oi.order_id = o.order_id
            WHERE p.stock_quantity > 0
            GROUP BY p.product_id, p.product_name, c.category_name, p.stock_quantity, p.price
            HAVING
                MAX(o.order_date) IS NULL
                OR MAX(o.order_date) < CURRENT_DATE - INTERVAL '%s days'
            ORDER BY inventory_value DESC
        """

        rows = self.db.execute_query(query, (days,))

        if rows:
            return [
                {
                    'product_id': row[0],
                    'product_name': row[1],
                    'category': row[2],
                    'stock_quantity': row[3],
                    'unit_price': float(row[4]),
                    'inventory_value': float(row[5]),
                    'last_sale_date': row[6].strftime('%Y-%m-%d') if row[6] else None,
                    'days_since_sale': (datetime.now().date() - row[6]).days if row[6] else None
                }
                for row in rows
            ]
        return []

# Exercise 4: Data Processing Pipeline (17 minutes)
def process_daily_sales_report(db: Database, date: str) -> Dict[str, Any]:
    """Comprehensive daily report with multiple metrics."""

    # Main metrics query
    main_query = """
        WITH daily_summary AS (
            SELECT
                COUNT(DISTINCT o.order_id) as total_orders,
                COUNT(DISTINCT o.customer_id) as total_customers,
                SUM(o.total_amount) as total_sales
            FROM orders o
            WHERE DATE(o.order_date) = %s
        ),
        new_vs_returning AS (
            SELECT
                SUM(CASE
                    WHEN first_order.first_date = %s THEN 1
                    ELSE 0
                END) as new_customers,
                COUNT(*) - SUM(CASE
                    WHEN first_order.first_date = %s THEN 1
                    ELSE 0
                END) as returning_customers
            FROM orders o
            JOIN (
                SELECT customer_id, MIN(DATE(order_date)) as first_date
                FROM orders
                GROUP BY customer_id
            ) first_order ON o.customer_id = first_order.customer_id
            WHERE DATE(o.order_date) = %s
        )
        SELECT
            ds.total_orders,
            ds.total_customers,
            ds.total_sales,
            nvr.new_customers,
            nvr.returning_customers
        FROM daily_summary ds, new_vs_returning nvr
    """

    # Top products query
    top_products_query = """
        SELECT
            p.product_name,
            SUM(oi.total_price) as revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE DATE(o.order_date) = %s
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT 5
    """

    # Geographic breakdown query
    geo_query = """
        SELECT
            c.city,
            COUNT(DISTINCT o.order_id) as orders,
            SUM(o.total_amount) as revenue
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE DATE(o.order_date) = %s AND c.city IS NOT NULL
        GROUP BY c.city
        ORDER BY revenue DESC
    """

    # Execute queries
    main_result = db.execute_query(main_query, (date, date, date, date))
    top_products = db.execute_query(top_products_query, (date,))
    geo_breakdown = db.execute_query(geo_query, (date,))

    report = {
        'date': date,
        'summary': {},
        'top_products': [],
        'geographic_breakdown': []
    }

    if main_result:
        row = main_result[0]
        report['summary'] = {
            'total_orders': row[0] or 0,
            'total_customers': row[1] or 0,
            'total_sales': float(row[2]) if row[2] else 0.0,
            'new_customers': row[3] or 0,
            'returning_customers': row[4] or 0
        }

    if top_products:
        report['top_products'] = [
            {'product_name': row[0], 'revenue': float(row[1])}
            for row in top_products
        ]

    if geo_breakdown:
        report['geographic_breakdown'] = [
            {'city': row[0], 'orders': row[1], 'revenue': float(row[2])}
            for row in geo_breakdown
        ]

    return report

def data_quality_check(db: Database) -> Dict[str, List[str]]:
    """Comprehensive data quality validation."""

    issues = {
        'missing_data': [],
        'duplicates': [],
        'outliers': [],
        'referential_integrity': []
    }

    # Check for missing required data
    missing_queries = [
        ("SELECT COUNT(*) FROM customers WHERE customer_name IS NULL OR customer_name = ''", "customers with missing names"),
        ("SELECT COUNT(*) FROM customers WHERE email IS NULL OR email = ''", "customers with missing emails"),
        ("SELECT COUNT(*) FROM products WHERE product_name IS NULL OR price IS NULL", "products with missing critical data"),
        ("SELECT COUNT(*) FROM orders WHERE customer_id IS NULL OR total_amount IS NULL", "orders with missing critical data")
    ]

    for query, description in missing_queries:
        result = db.execute_query(query)
        if result and result[0][0] > 0:
            issues['missing_data'].append(f"{result[0][0]} {description}")

    # Check for duplicates
    duplicate_queries = [
        ("SELECT email, COUNT(*) as cnt FROM customers GROUP BY email HAVING COUNT(*) > 1", "duplicate customer emails"),
        ("SELECT customer_id, order_date, total_amount, COUNT(*) as cnt FROM orders GROUP BY customer_id, order_date, total_amount HAVING COUNT(*) > 1", "potential duplicate orders")
    ]

    for query, description in duplicate_queries:
        result = db.execute_query(query)
        if result:
            issues['duplicates'].append(f"{len(result)} {description}")

    # Check for outliers
    outlier_queries = [
        ("SELECT COUNT(*) FROM products WHERE price < 0 OR price > 10000", "products with extreme prices"),
        ("SELECT COUNT(*) FROM orders WHERE total_amount < 0 OR total_amount > 50000", "orders with extreme amounts"),
        ("SELECT COUNT(*) FROM order_items WHERE quantity <= 0 OR quantity > 1000", "order items with extreme quantities")
    ]

    for query, description in outlier_queries:
        result = db.execute_query(query)
        if result and result[0][0] > 0:
            issues['outliers'].append(f"{result[0][0]} {description}")

    # Check referential integrity
    integrity_queries = [
        ("SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON o.customer_id = c.customer_id WHERE c.customer_id IS NULL", "orders with invalid customer_id"),
        ("SELECT COUNT(*) FROM order_items oi LEFT JOIN orders o ON oi.order_id = o.order_id WHERE o.order_id IS NULL", "order_items with invalid order_id"),
        ("SELECT COUNT(*) FROM order_items oi LEFT JOIN products p ON oi.product_id = p.product_id WHERE p.product_id IS NULL", "order_items with invalid product_id")
    ]

    for query, description in integrity_queries:
        result = db.execute_query(query)
        if result and result[0][0] > 0:
            issues['referential_integrity'].append(f"{result[0][0]} {description}")

    return issues