"""
Combined Python + SQL Data Analysis Exercises
These simulate real interview scenarios combining programming and database skills
Time limit: 15-20 minutes per exercise
"""

from src.database import Database
from typing import List, Dict, Any
import json

# Exercise 1: Customer Analytics (15 minutes)
class CustomerAnalytics:
    def __init__(self, db: Database):
        self.db = db
    
    def get_top_customers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Find top customers by total purchase amount.
        Return list of dicts with: customer_name, total_spent, order_count
        """
        # TODO: Write SQL query and Python processing
        pass
    
    def customer_retention_rate(self, months_back: int = 6) -> float:
        """
        Calculate what percentage of customers who bought something
        months_back ago also bought something in the last month.
        """
        # TODO: Implement retention calculation
        pass
    
    def segment_customers(self) -> Dict[str, List[str]]:
        """
        Segment customers into groups based on purchasing behavior:
        - 'frequent': >5 orders in last 6 months
        - 'big_spender': average order value >$200
        - 'at_risk': no orders in last 3 months but had orders before
        - 'new': first order in last 30 days
        """
        # TODO: Implement customer segmentation
        pass

# Exercise 2: Sales Performance Dashboard (18 minutes)
class SalesAnalytics:
    def __init__(self, db: Database):
        self.db = db
    
    def monthly_trends(self, year: int = 2023) -> List[Dict[str, Any]]:
        """
        Get monthly sales trends showing:
        - month, revenue, order_count, avg_order_value, growth_rate (vs previous month)
        """
        # TODO: Implement monthly trend analysis
        pass
    
    def product_performance(self) -> List[Dict[str, Any]]:
        """
        Analyze product performance:
        - product_name, category, total_revenue, units_sold, avg_rating
        - Include products with 0 sales (show as 0)
        """
        # TODO: Implement product performance analysis
        pass
    
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """
        Find unusual patterns:
        - Days with sales >2 standard deviations from mean
        - Products with sudden sales spikes/drops
        """
        # TODO: Implement anomaly detection
        pass

# Exercise 3: Inventory Optimization (20 minutes)
class InventoryOptimizer:
    def __init__(self, db: Database):
        self.db = db
    
    def reorder_recommendations(self) -> List[Dict[str, Any]]:
        """
        Recommend products to reorder based on:
        - Current stock level
        - Average daily sales (last 30 days)
        - Days until stockout
        Return products that need reordering within 7 days
        """
        # TODO: Implement reorder logic
        pass
    
    def abc_analysis(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Classify products using ABC analysis:
        A: Top 80% of revenue (most important)
        B: Next 15% of revenue  
        C: Bottom 5% of revenue
        """
        # TODO: Implement ABC classification
        pass
    
    def slow_moving_products(self, days: int = 90) -> List[Dict[str, Any]]:
        """
        Find products with no sales in the last N days
        that still have inventory.
        """
        # TODO: Find slow-moving inventory
        pass

# Exercise 4: Data Processing Pipeline (17 minutes)
def process_daily_sales_report(db: Database, date: str) -> Dict[str, Any]:
    """
    Create a comprehensive daily sales report including:
    - Total sales, orders, customers
    - Top 5 products by revenue
    - New vs returning customers
    - Geographic breakdown (by city)
    """
    # TODO: Implement daily report generation
    pass

def data_quality_check(db: Database) -> Dict[str, List[str]]:
    """
    Perform data quality checks and return issues found:
    - missing_data: Records with null required fields
    - duplicates: Potential duplicate records
    - outliers: Unusual values (negative prices, extreme quantities)
    - referential_integrity: Foreign key violations
    """
    # TODO: Implement data quality checks
    pass

# Test framework
if __name__ == "__main__":
    # Example usage - you would run these with actual database
    db = Database()
    
    # Test CustomerAnalytics
    customer_analytics = CustomerAnalytics(db)
    print("Testing customer analytics...")
    
    # Test SalesAnalytics  
    sales_analytics = SalesAnalytics(db)
    print("Testing sales analytics...")
    
    # Test InventoryOptimizer
    inventory_optimizer = InventoryOptimizer(db)
    print("Testing inventory optimization...")
    
    print("All combined exercises ready for testing!")
