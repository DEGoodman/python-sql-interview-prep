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
    
    print("All tests passed!")