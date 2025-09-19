"""
Alternative Solution Approaches for Study
These show different ways to solve the same problems
"""

from src.database import Database
from typing import List, Dict, Any, Optional

# ALTERNATIVE APPROACHES FOR CUSTOMER RETENTION

class CustomerAnalyticsAlternatives:
    def __init__(self, db: Database):
        self.db = db

    def top_customers_with_cos(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Alternative: simpler query based on customer_order_summary table"""

        query = """
            SELECT
              customer_name,
              total_spent,
              order_count
            FROM customer_order_summary
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

    def retention_rate_with_exists(self, months_back: int = 6) -> float:
        """Alternative: Using EXISTS instead of JOIN for intersection."""
        query = """
            WITH base_customers AS (
                SELECT DISTINCT customer_id
                FROM orders
                WHERE order_date >= CURRENT_DATE - INTERVAL '%s months' - INTERVAL '1 month'
                  AND order_date < CURRENT_DATE - INTERVAL '%s months'
            )
            SELECT
                COUNT(*) as total_past,
                COUNT(CASE
                    WHEN EXISTS (
                        SELECT 1 FROM orders recent
                        WHERE recent.customer_id = base_customers.customer_id
                          AND recent.order_date >= CURRENT_DATE - INTERVAL '1 month'
                    ) THEN 1
                END) as retained
            FROM base_customers
        """

        result = self.db.execute_query(query, (months_back, months_back))
        if result and result[0][0] > 0:
            total, retained = result[0]
            return (retained / total) * 100.0
        return 0.0

    def retention_rate_single_query(self, months_back: int = 6) -> float:
        """Alternative: Single query with conditional aggregation."""
        query = """
            SELECT
                COUNT(DISTINCT CASE
                    WHEN order_date >= CURRENT_DATE - INTERVAL '%s months' - INTERVAL '1 month'
                     AND order_date < CURRENT_DATE - INTERVAL '%s months'
                    THEN customer_id
                END) as past_customers,
                COUNT(DISTINCT CASE
                    WHEN order_date >= CURRENT_DATE - INTERVAL '%s months' - INTERVAL '1 month'
                     AND order_date < CURRENT_DATE - INTERVAL '%s months'
                     AND customer_id IN (
                         SELECT DISTINCT customer_id FROM orders
                         WHERE order_date >= CURRENT_DATE - INTERVAL '1 month'
                     )
                    THEN customer_id
                END) as retained_customers
            FROM orders
        """

        result = self.db.execute_query(query, (months_back, months_back, months_back, months_back))
        if result and result[0][0] > 0:
            past, retained = result[0]
            return (retained / past) * 100.0
        return 0.0

    def customer_segments_separate_queries(self) -> Dict[str, List[str]]:
        """Alternative: Separate queries instead of CTEs with UNION."""
        segments = {'frequent': [], 'big_spender': [], 'at_risk': [], 'new': []}

        # Query 1: Frequent customers
        frequent_query = """
            SELECT customer_name
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.order_date >= CURRENT_DATE - INTERVAL '6 months'
            GROUP BY c.customer_id, c.customer_name
            HAVING COUNT(o.order_id) > 5
        """

        # Query 2: Big spenders
        big_spender_query = """
            SELECT customer_name
            FROM customer_order_summary
            WHERE total_orders > 0 AND (total_spent / total_orders) > 200
        """

        # Query 3: At risk
        at_risk_query = """
            SELECT customer_name
            FROM customer_order_summary
            WHERE total_orders > 0
              AND last_order_date < CURRENT_DATE - INTERVAL '3 months'
        """

        # Query 4: New customers
        new_query = """
            SELECT customer_name
            FROM customer_order_summary
            WHERE first_order_date > CURRENT_DATE - INTERVAL '1 month'
        """

        # Execute each query separately
        queries = [
            (frequent_query, 'frequent'),
            (big_spender_query, 'big_spender'),
            (at_risk_query, 'at_risk'),
            (new_query, 'new')
        ]

        for query, segment_name in queries:
            result = self.db.execute_query(query)
            if result:
                segments[segment_name] = [row[0] for row in result]

        return segments

# ALTERNATIVE APPROACHES FOR SALES ANALYTICS

class SalesAnalyticsAlternatives:
    def __init__(self, db: Database):
        self.db = db

    def monthly_trends_self_join(self, year: int = 2023) -> List[Dict[str, Any]]:
        """Alternative: Using self-join instead of window functions."""
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
            )
            SELECT
                current.month,
                current.revenue,
                current.order_count,
                current.avg_order_value,
                CASE
                    WHEN previous.revenue IS NULL OR previous.revenue = 0 THEN 0
                    ELSE ((current.revenue - previous.revenue) / previous.revenue) * 100
                END as growth_rate
            FROM monthly_data current
            LEFT JOIN monthly_data previous ON current.month = previous.month + 1
            ORDER BY current.month
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

    def product_performance_with_ranking(self) -> List[Dict[str, Any]]:
        """Alternative: Add ranking and performance categories."""
        query = """
            SELECT
                p.product_name,
                c.category_name,
                COALESCE(SUM(oi.total_price), 0) as total_revenue,
                COALESCE(SUM(oi.quantity), 0) as units_sold,
                p.average_rating,
                RANK() OVER (ORDER BY COALESCE(SUM(oi.total_price), 0) DESC) as revenue_rank,
                CASE
                    WHEN COALESCE(SUM(oi.total_price), 0) = 0 THEN 'No Sales'
                    WHEN COALESCE(SUM(oi.total_price), 0) < 1000 THEN 'Low Performer'
                    WHEN COALESCE(SUM(oi.total_price), 0) < 5000 THEN 'Medium Performer'
                    ELSE 'High Performer'
                END as performance_category
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
                    'avg_rating': float(row[4]) if row[4] else None,
                    'revenue_rank': row[5],
                    'performance_category': row[6]
                }
                for row in rows
            ]
        return []

# ALTERNATIVE APPROACHES FOR INVENTORY OPTIMIZATION

class InventoryOptimizerAlternatives:
    def __init__(self, db: Database):
        self.db = db

    def reorder_recommendations_safety_stock(self) -> List[Dict[str, Any]]:
        """Alternative: Using safety stock model instead of simple days calculation."""
        query = """
            WITH sales_analysis AS (
                SELECT
                    p.product_id,
                    p.product_name,
                    p.stock_quantity,
                    COALESCE(AVG(oi.quantity), 0) as avg_daily_sales,
                    COALESCE(STDDEV(oi.quantity), 0) as sales_stddev,
                    COUNT(oi.order_item_id) as sales_days
                FROM products p
                LEFT JOIN order_items oi ON p.product_id = oi.product_id
                LEFT JOIN orders o ON oi.order_id = o.order_id
                WHERE o.order_date >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY p.product_id, p.product_name, p.stock_quantity
            ),
            reorder_analysis AS (
                SELECT
                    *,
                    7 as lead_time_days,  -- Assume 7 day lead time
                    (avg_daily_sales * 7) as lead_time_demand,
                    -- Safety stock = Z-score * sqrt(lead_time) * demand_stddev
                    (1.65 * SQRT(7) * sales_stddev) as safety_stock,
                    (avg_daily_sales * 7) + (1.65 * SQRT(7) * sales_stddev) as reorder_point
                FROM sales_analysis
                WHERE avg_daily_sales > 0
            )
            SELECT
                product_id,
                product_name,
                stock_quantity,
                avg_daily_sales,
                reorder_point,
                lead_time_demand,
                safety_stock,
                CASE
                    WHEN stock_quantity <= reorder_point THEN 'URGENT'
                    WHEN stock_quantity <= reorder_point * 1.2 THEN 'SOON'
                    ELSE 'OK'
                END as priority
            FROM reorder_analysis
            WHERE stock_quantity <= reorder_point * 1.5
            ORDER BY
                CASE
                    WHEN stock_quantity <= reorder_point THEN 1
                    WHEN stock_quantity <= reorder_point * 1.2 THEN 2
                    ELSE 3
                END,
                stock_quantity / avg_daily_sales ASC
        """

        rows = self.db.execute_query(query)

        if rows:
            return [
                {
                    'product_id': row[0],
                    'product_name': row[1],
                    'current_stock': row[2],
                    'avg_daily_sales': round(float(row[3]), 2),
                    'reorder_point': round(float(row[4]), 0),
                    'lead_time_demand': round(float(row[5]), 0),
                    'safety_stock': round(float(row[6]), 0),
                    'priority': row[7],
                    'recommended_order_qty': max(50, int(row[3] * 30))  # 30 days or minimum 50
                }
                for row in rows
            ]
        return []

    def abc_analysis_revenue_and_margin(self) -> Dict[str, List[Dict[str, Any]]]:
        """Alternative: ABC analysis considering both revenue and profit margin."""
        query = """
            WITH product_metrics AS (
                SELECT
                    p.product_id,
                    p.product_name,
                    c.category_name,
                    COALESCE(SUM(oi.total_price), 0) as total_revenue,
                    COALESCE(SUM(oi.quantity * (oi.unit_price - p.cost)), 0) as total_profit,
                    CASE
                        WHEN SUM(oi.total_price) > 0
                        THEN (SUM(oi.quantity * (oi.unit_price - p.cost)) / SUM(oi.total_price)) * 100
                        ELSE 0
                    END as profit_margin_percent
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN order_items oi ON p.product_id = oi.product_id
                GROUP BY p.product_id, p.product_name, c.category_name, p.cost
            ),
            revenue_percentiles AS (
                SELECT
                    *,
                    SUM(total_revenue) OVER() as total_all_revenue,
                    SUM(total_revenue) OVER(ORDER BY total_revenue DESC) as running_revenue,
                    SUM(total_profit) OVER() as total_all_profit,
                    SUM(total_profit) OVER(ORDER BY total_profit DESC) as running_profit
                FROM product_metrics
                WHERE total_revenue > 0
            ),
            classified AS (
                SELECT
                    *,
                    (running_revenue / total_all_revenue) * 100 as revenue_cumulative_percent,
                    (running_profit / total_all_profit) * 100 as profit_cumulative_percent,
                    -- Weighted classification considering both revenue and profit
                    CASE
                        WHEN (running_revenue / total_all_revenue) * 100 <= 70
                             AND (running_profit / total_all_profit) * 100 <= 70 THEN 'A'
                        WHEN (running_revenue / total_all_revenue) * 100 <= 90
                             AND (running_profit / total_all_profit) * 100 <= 90 THEN 'B'
                        ELSE 'C'
                    END as abc_class
                FROM revenue_percentiles
            )
            SELECT
                abc_class,
                product_name,
                category_name,
                total_revenue,
                total_profit,
                profit_margin_percent,
                revenue_cumulative_percent,
                profit_cumulative_percent
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
                    'total_profit': float(row[4]),
                    'profit_margin_percent': round(float(row[5]), 2),
                    'revenue_cumulative_percent': round(float(row[6]), 2),
                    'profit_cumulative_percent': round(float(row[7]), 2)
                })

        return result

# ALTERNATIVE APPROACHES FOR API DESIGN

class APIDesignAlternatives:
    def __init__(self, db: Database):
        self.db = db

    def search_products_with_full_text(self, query: str, **filters) -> Dict[str, Any]:
        """Alternative: Using PostgreSQL full-text search instead of LIKE."""
        # Note: This requires setting up text search in PostgreSQL
        search_query = """
            SELECT
                p.product_id,
                p.product_name,
                p.description,
                p.price,
                p.stock_quantity,
                p.average_rating,
                c.category_name,
                -- Full-text search ranking
                ts_rank_cd(
                    to_tsvector('english', p.product_name || ' ' || COALESCE(p.description, '')),
                    plainto_tsquery('english', %s)
                ) as search_rank
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE to_tsvector('english', p.product_name || ' ' || COALESCE(p.description, ''))
                  @@ plainto_tsquery('english', %s)
            ORDER BY search_rank DESC, p.product_name
            LIMIT 20
        """

        result = self.db.execute_query(search_query, (query, query))

        if result:
            return {
                'products': [
                    {
                        'product_id': row[0],
                        'product_name': row[1],
                        'description': row[2],
                        'price': float(row[3]),
                        'stock_quantity': row[4],
                        'average_rating': float(row[5]) if row[5] else None,
                        'category': row[6],
                        'search_rank': float(row[7])
                    }
                    for row in result
                ],
                'search_type': 'full_text_search'
            }

        return {'products': [], 'search_type': 'full_text_search'}

    def bulk_operations_with_upsert(self, products_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Alternative: Using PostgreSQL UPSERT (ON CONFLICT) for bulk operations."""
        upsert_query = """
            INSERT INTO products (product_id, product_name, price, stock_quantity, category_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (product_id)
            DO UPDATE SET
                product_name = EXCLUDED.product_name,
                price = EXCLUDED.price,
                stock_quantity = EXCLUDED.stock_quantity,
                last_updated = CURRENT_TIMESTAMP
            RETURNING product_id, 'upserted' as operation
        """

        results = []
        for product_data in products_data:
            try:
                result = self.db.execute_query(upsert_query, (
                    product_data.get('product_id'),
                    product_data.get('product_name'),
                    product_data.get('price'),
                    product_data.get('stock_quantity'),
                    product_data.get('category_id')
                ))

                if result:
                    results.append({
                        'product_id': result[0][0],
                        'operation': result[0][1],
                        'success': True
                    })

            except Exception as e:
                results.append({
                    'product_id': product_data.get('product_id'),
                    'operation': 'failed',
                    'success': False,
                    'error': str(e)
                })

        return {
            'total_operations': len(products_data),
            'successful_operations': len([r for r in results if r['success']]),
            'results': results
        }

# PERFORMANCE-ORIENTED ALTERNATIVES

def get_customer_metrics_materialized_view(db: Database) -> List[Dict[str, Any]]:
    """Alternative: Using materialized views for expensive calculations."""
    # This would require creating a materialized view first:
    create_view_query = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS customer_metrics_mv AS
    SELECT
        c.customer_id,
        c.customer_name,
        COUNT(o.order_id) as total_orders,
        COALESCE(SUM(o.total_amount), 0) as total_spent,
        COALESCE(AVG(o.total_amount), 0) as avg_order_value,
        MAX(o.order_date) as last_order_date,
        -- Pre-calculated CLV
        CASE
            WHEN COUNT(o.order_id) > 0 THEN
                AVG(o.total_amount) *
                (COUNT(o.order_id) / GREATEST(EXTRACT(DAYS FROM (MAX(o.order_date) - MIN(o.order_date))) / 365.0, 0.1)) *
                2
            ELSE 0
        END as predicted_clv
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name;

    CREATE INDEX IF NOT EXISTS idx_customer_metrics_mv_clv ON customer_metrics_mv(predicted_clv);
    """

    # In production, you'd refresh this periodically:
    # REFRESH MATERIALIZED VIEW customer_metrics_mv;

    query = "SELECT * FROM customer_metrics_mv ORDER BY predicted_clv DESC LIMIT 100"
    result = db.execute_query(query)

    if result:
        return [
            {
                'customer_id': row[0],
                'customer_name': row[1],
                'total_orders': row[2],
                'total_spent': float(row[3]),
                'avg_order_value': float(row[4]),
                'last_order_date': row[5].strftime('%Y-%m-%d') if row[5] else None,
                'predicted_clv': round(float(row[6]), 2)
            }
            for row in result
        ]

    return []

def cached_analytics_with_redis_pattern(db: Database, cache_key: str, ttl: int = 3600):
    """Alternative: Caching pattern for expensive analytics queries."""
    # This is a conceptual example - would need Redis or similar

    # Pseudo-code for caching pattern:
    """
    import redis
    import json
    import hashlib

    def get_cached_analytics(db, query, params, cache_key, ttl=3600):
        r = redis.Redis()

        # Create cache key from query and params
        full_key = f"analytics:{cache_key}:{hashlib.md5(str(params).encode()).hexdigest()}"

        # Try to get from cache first
        cached_result = r.get(full_key)
        if cached_result:
            return json.loads(cached_result)

        # If not in cache, execute query
        result = db.execute_query(query, params)
        processed_result = process_analytics_result(result)

        # Store in cache
        r.setex(full_key, ttl, json.dumps(processed_result))

        return processed_result
    """

    # For this example, just return a placeholder
    return {
        'cache_strategy': 'redis_with_ttl',
        'ttl_seconds': ttl,
        'cache_key': cache_key,
        'note': 'This would use Redis or similar caching system in production'
    }