"""
API Design + Database Integration Exercises
Common interview scenario: Build REST API endpoints
Time limit: 15-20 minutes per exercise
"""

from src.database import Database
from typing import List, Dict, Any, Optional
import json
from datetime import datetime, date

# Exercise 1: User Management API (15 minutes)
class UserAPI:
    def __init__(self, db: Database):
        self.db = db
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user with validation:
        - Required: name, email
        - Email must be unique
        - Return: user_id, success message or error
        """
        # TODO: Implement user creation with validation
        pass
    
    def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user profile with their order history summary:
        - user info + total_orders, total_spent, last_order_date
        """
        # TODO: Implement user profile retrieval
        pass
    
    def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]) -> bool:
        """
        Update user preferences (stored as JSON):
        - newsletter_opt_in, preferred_categories, etc.
        """
        # TODO: Implement preference updates
        pass

# Exercise 2: Order Management API (18 minutes)
class OrderAPI:
    def __init__(self, db: Database):
        self.db = db
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create order with validation and inventory check:
        - Check product availability
        - Calculate total with tax
        - Update inventory
        - Return order_id and details or error
        """
        # TODO: Implement order creation with business logic
        pass
    
    def get_order_status(self, order_id: int) -> Dict[str, Any]:
        """
        Get order details with current status and tracking info
        """
        # TODO: Implement order status retrieval
        pass
    
    def cancel_order(self, order_id: int, reason: str) -> Dict[str, Any]:
        """
        Cancel order if possible:
        - Check if cancellable (not shipped)
        - Restore inventory
        - Update order status
        """
        # TODO: Implement order cancellation logic
        pass
    
    def get_orders_by_date_range(self, start_date: str, end_date: str, 
                                status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get orders within date range, optionally filtered by status
        """
        # TODO: Implement date range filtering
        pass

# Exercise 3: Product Search API (16 minutes)
class ProductSearchAPI:
    def __init__(self, db: Database):
        self.db = db
    
    def search_products(self, query: str, category: Optional[str] = None,
                       min_price: Optional[float] = None, max_price: Optional[float] = None,
                       sort_by: str = 'relevance', page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """
        Product search with filtering and pagination:
        - Text search in name/description
        - Filter by category, price range
        - Sort by: relevance, price, rating, popularity
        - Return: products, total_count, page_info
        """
        # TODO: Implement comprehensive product search
        pass
    
    def get_product_recommendations(self, product_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get product recommendations based on:
        - Same category
        - Frequently bought together
        - Similar price range
        """
        # TODO: Implement recommendation logic
        pass
    
    def update_product_inventory(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Bulk inventory update:
        updates = [{"product_id": 1, "quantity": 50}, ...]
        Return success/failure status for each update
        """
        # TODO: Implement bulk inventory updates
        pass

# Exercise 4: Analytics API (20 minutes)
class AnalyticsAPI:
    def __init__(self, db: Database):
        self.db = db
    
    def get_dashboard_metrics(self, date_range: str = 'last_30_days') -> Dict[str, Any]:
        """
        Return key business metrics:
        - Total sales, orders, customers
        - Growth rates (vs previous period)
        - Top products, categories
        - Geographic distribution
        """
        # TODO: Implement dashboard metrics
        pass
    
    def get_customer_lifetime_value(self, customer_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Calculate CLV for specific customer or all customers
        Include: total_spent, avg_order_value, order_frequency, predicted_clv
        """
        # TODO: Implement CLV calculation
        pass
    
    def generate_sales_report(self, report_type: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Generate different types of reports:
        - 'summary': High-level metrics
        - 'detailed': Line-item breakdown  
        - 'comparison': vs previous period
        """
        # TODO: Implement flexible reporting
        pass

# Utility Functions for Common Interview Tasks
def validate_input(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """Return list of missing required fields"""
    # TODO: Implement input validation
    pass

def paginate_results(total_count: int, page: int, page_size: int) -> Dict[str, Any]:
    """Return pagination metadata"""
    # TODO: Implement pagination logic
    pass

def format_api_response(success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
    """Standardize API response format"""
    # TODO: Implement response formatting
    pass

# Testing framework
if __name__ == "__main__":
    db = Database()
    
    # Test scenarios
    print("Testing User API...")
    user_api = UserAPI(db)
    
    print("Testing Order API...")  
    order_api = OrderAPI(db)
    
    print("Testing Product Search API...")
    search_api = ProductSearchAPI(db)
    
    print("Testing Analytics API...")
    analytics_api = AnalyticsAPI(db)
    
    print("All API exercises ready for implementation!")