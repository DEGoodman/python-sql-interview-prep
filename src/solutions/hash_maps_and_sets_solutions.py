"""
Solutions to Hash Maps and Sets Exercises
Try solving exercises/data_structures/hash_maps_and_sets.py first!
"""

def first_uniq_char(s):
    """
    Find the first non-repeating character in a string and return its index.
    
    Time: O(n), Space: O(1) - at most 26 characters in English
    """
    # Count frequency of each character
    char_count = {}
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    # Find first character with count 1
    for i, char in enumerate(s):
        if char_count[char] == 1:
            return i
    
    return -1

def is_anagram(s, t):
    """
    Check if two strings are anagrams of each other.
    
    Time: O(n), Space: O(1) - at most 26 characters
    """
    if len(s) != len(t):
        return False
    
    # Method 1: Sort and compare
    # return sorted(s) == sorted(t)
    
    # Method 2: Count frequencies
    char_count = {}
    
    # Count characters in s
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    # Subtract characters in t
    for char in t:
        if char not in char_count:
            return False
        char_count[char] -= 1
        if char_count[char] == 0:
            del char_count[char]
    
    return len(char_count) == 0

def top_k_frequent(nums, k):
    """
    Return the k most frequent elements from an array.
    
    Time: O(n log k), Space: O(n)
    """
    from collections import Counter
    import heapq
    
    # Count frequencies
    count = Counter(nums)
    
    # Use heap to find top k
    # Python's heapq is min-heap, so we use negative frequencies
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (-freq, num))
    
    # Extract top k elements
    result = []
    for _ in range(k):
        freq, num = heapq.heappop(heap)
        result.append(num)
    
    return result

def intersection(nums1, nums2):
    """
    Find the intersection of two arrays (unique elements that appear in both).
    
    Time: O(m + n), Space: O(min(m, n))
    """
    # Convert to sets and find intersection
    set1 = set(nums1)
    set2 = set(nums2)
    return list(set1 & set2)

def subarray_sum(nums, k):
    """
    Count the number of continuous subarrays whose sum equals k.
    
    Time: O(n), Space: O(n)
    """
    # Use cumulative sum and hash map
    count = 0
    cumsum = 0
    cumsum_count = {0: 1}  # cumsum -> frequency
    
    for num in nums:
        cumsum += num
        
        # If (cumsum - k) exists, we found subarrays ending at current position
        if (cumsum - k) in cumsum_count:
            count += cumsum_count[cumsum - k]
        
        # Add current cumsum to map
        cumsum_count[cumsum] = cumsum_count.get(cumsum, 0) + 1
    
    return count

def generate_sales_report():
    """
    Generate a sales report for products grouped by date.
    Products with no orders show 0 revenue.

    Time: O(p*d + o), Space: O(p*d)
    where p = products, d = dates, o = orders
    """
    # Hardcoded data
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Mouse", "price": 25.50},
        {"id": 3, "name": "Keyboard", "price": 75.00},
        {"id": 4, "name": "Monitor", "price": 299.99},
        {"id": 5, "name": "Webcam", "price": 89.99}
    ]

    orders = [
        {"id": 1, "product_id": 1, "date": "2024-01-15"},
        {"id": 2, "product_id": 1, "date": "2024-01-16"},
        {"id": 3, "product_id": 2, "date": "2024-01-15"},
        {"id": 4, "product_id": 2, "date": "2024-01-16"},
        {"id": 5, "product_id": 2, "date": "2024-01-17"},
        {"id": 6, "product_id": 3, "date": "2024-01-15"},
        {"id": 7, "product_id": 1, "date": "2024-01-17"}
        # Note: No orders for Monitor (id=4) or Webcam (id=5)
    ]

    # Group orders by date and product using hash map
    sales_by_date_product = {}

    for order in orders:
        date = order["date"]
        product_id = order["product_id"]

        if date not in sales_by_date_product:
            sales_by_date_product[date] = {}

        if product_id not in sales_by_date_product[date]:
            sales_by_date_product[date][product_id] = 0

        # Find product price and add to revenue
        product_price = next(p["price"] for p in products if p["id"] == product_id)
        sales_by_date_product[date][product_id] += product_price

    # Generate report ensuring all products appear for each date
    report = []
    all_dates = sorted(set(order["date"] for order in orders))

    for date in all_dates:
        for product in products:
            revenue = sales_by_date_product.get(date, {}).get(product["id"], 0)
            report.append({
                "date": date,
                "product_name": product["name"],
                "product_id": product["id"],
                "total_revenue": revenue
            })

    return sorted(report, key=lambda x: (x["date"], x["product_name"]))

# Test cases
if __name__ == "__main__":
    # Test first_uniq_char
    assert first_uniq_char("leetcode") == 0
    assert first_uniq_char("loveleetcode") == 2
    assert first_uniq_char("aabb") == -1
    print("✅ first_uniq_char tests passed")
    
    # Test is_anagram
    assert is_anagram("anagram", "nagaram") == True
    assert is_anagram("rat", "car") == False
    print("✅ is_anagram tests passed")
    
    # Test top_k_frequent
    result = top_k_frequent([1,1,1,2,2,3], 2)
    assert set(result) == {1, 2}
    
    result2 = top_k_frequent([1], 1)
    assert result2 == [1]
    print("✅ top_k_frequent tests passed")
    
    # Test intersection
    assert set(intersection([1,2,2,1], [2,2])) == {2}
    assert set(intersection([4,9,5], [9,4,9,8,4])) == {4, 9}
    print("✅ intersection tests passed")
    
    # Test subarray_sum
    assert subarray_sum([1,1,1], 2) == 2
    assert subarray_sum([1,2,3], 3) == 2  # [3] and [1,2]
    assert subarray_sum([1], 0) == 0
    assert subarray_sum([1,-1,0], 0) == 3  # [-1,1], [0], [1,-1,0]
    print("✅ subarray_sum tests passed")

    # Test generate_sales_report
    sales_report = generate_sales_report()

    # Verify structure
    assert len(sales_report) > 0
    assert all('date' in item and 'product_name' in item and 'total_revenue' in item for item in sales_report)

    # Verify products with 0 sales are included
    zero_revenue_items = [item for item in sales_report if item['total_revenue'] == 0]
    assert len(zero_revenue_items) > 0  # Monitor and Webcam should have 0 revenue

    # Verify some actual sales
    nonzero_revenue_items = [item for item in sales_report if item['total_revenue'] > 0]
    assert len(nonzero_revenue_items) > 0

    print("✅ generate_sales_report tests passed")

    print("All tests passed!")