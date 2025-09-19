"""
Hash Maps and Sets Exercises
Time limit: 10-15 minutes per exercise
"""

# Exercise 1: First Unique Character (Easy - 7 minutes)
def first_uniq_char(s):
    """
    Find the first non-repeating character in a string and return its index.
    If it doesn't exist, return -1.
    
    Example: "leetcode" -> 0 (first 'l')
    """
    # TODO: Implement this function
    pass

# Exercise 2: Valid Anagram (Easy - 5 minutes)
def is_anagram(s, t):
    """
    Check if two strings are anagrams of each other.
    
    Example: "anagram", "nagaram" -> True
    """
    # TODO: Implement this function
    pass

# Exercise 3: Top K Frequent Elements (Medium - 12 minutes)
def top_k_frequent(nums, k):
    """
    Return the k most frequent elements from an array.
    
    Example: nums = [1,1,1,2,2,3], k = 2 -> [1,2]
    """
    # TODO: Implement this function
    pass

# Exercise 4: Intersection of Two Arrays (Easy - 6 minutes)
def intersection(nums1, nums2):
    """
    Find the intersection of two arrays (unique elements that appear in both).
    
    Example: [1,2,2,1], [2,2] -> [2]
    """
    # TODO: Implement this function
    pass

# Exercise 5: Subarray Sum Equals K (Medium - 15 minutes)
def subarray_sum(nums, k):
    """
    Count the number of continuous subarrays whose sum equals k.

    Example: nums = [1,1,1], k = 2 -> 2
    """
    # TODO: Implement this function
    pass

# Exercise 6: Sales Report Generator (Medium - 12 minutes)
def generate_sales_report():
    """
    Given two classes of data - Products (id, name, price) and Orders (id, product_id, date),
    create a "sales report" for each product grouped by date.
    Products that have no orders should have 0 as their total revenue.

    Use hardcoded data and return a list of dictionaries with:
    - date: order date
    - product_name: name of the product
    - product_id: id of the product
    - total_revenue: total revenue for that product on that date (0 if no sales)

    Example output:
    [
        {"date": "2024-01-15", "product_name": "Laptop", "product_id": 1, "total_revenue": 999.99},
        {"date": "2024-01-15", "product_name": "Mouse", "product_id": 2, "total_revenue": 25.50},
        {"date": "2024-01-15", "product_name": "Keyboard", "product_id": 3, "total_revenue": 75.00},
        {"date": "2024-01-15", "product_name": "Monitor", "product_id": 4, "total_revenue": 0},
        ...
    ]
    """
    # TODO: Implement this function
    pass

# Test cases
if __name__ == "__main__":
    # Test first_uniq_char
    assert first_uniq_char("leetcode") == 0
    assert first_uniq_char("loveleetcode") == 2
    assert first_uniq_char("aabb") == -1
    
    # Test is_anagram
    assert is_anagram("anagram", "nagaram") == True
    assert is_anagram("rat", "car") == False
    
    # Test top_k_frequent
    result = top_k_frequent([1,1,1,2,2,3], 2)
    assert set(result) == {1, 2}
    
    # Test intersection
    assert set(intersection([1,2,2,1], [2,2])) == {2}
    assert set(intersection([4,9,5], [9,4,9,8,4])) == {4, 9}
    
    # Test subarray_sum
    assert subarray_sum([1,1,1], 2) == 2
    assert subarray_sum([1,2,3], 3) == 2

    # Test generate_sales_report
    sales_report = generate_sales_report()
    assert len(sales_report) > 0
    assert all('date' in item and 'product_name' in item and 'total_revenue' in item for item in sales_report)

    print("All tests passed!")