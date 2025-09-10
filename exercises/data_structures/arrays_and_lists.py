"""
Array and List Data Structure Exercises
Time limit: 10-15 minutes per exercise
"""

# Exercise 1: Find Missing Number (Easy - 5 minutes)
def find_missing_number(nums):
    """
    Given an array containing n distinct numbers taken from 0, 1, 2, ..., n,
    find the one number that is missing from the array.
    
    Example: [3,0,1] -> 2
    """
    # TODO: Implement this function
    pass

# Exercise 2: Two Sum (Medium - 8 minutes)
def two_sum(nums, target):
    """
    Given an array of integers and a target sum, return indices of two numbers
    that add up to the target.
    
    Example: nums = [2,7,11,15], target = 9 -> [0,1]
    """
    # TODO: Implement this function
    pass

# Exercise 3: Group Anagrams (Medium - 10 minutes)
def group_anagrams(strs):
    """
    Group strings that are anagrams of each other.
    
    Example: ["eat","tea","tan","ate","nat","bat"] 
    -> [["bat"],["nat","tan"],["ate","eat","tea"]]
    """
    # TODO: Implement this function
    pass

# Exercise 4: Remove Duplicates from Sorted Array (Easy - 5 minutes)
def remove_duplicates(nums):
    """
    Remove duplicates from sorted array in-place and return new length.
    
    Example: [1,1,2] -> 2, nums becomes [1,2,_]
    """
    # TODO: Implement this function
    pass

# Test cases
if __name__ == "__main__":
    # Test find_missing_number
    assert find_missing_number([3,0,1]) == 2
    assert find_missing_number([0,1]) == 2
    assert find_missing_number([9,6,4,2,3,5,7,0,1]) == 8
    
    # Test two_sum
    assert two_sum([2,7,11,15], 9) == [0,1]
    assert two_sum([3,2,4], 6) == [1,2]
    
    # Test group_anagrams
    result = group_anagrams(["eat","tea","tan","ate","nat","bat"])
    # Note: Order doesn't matter for this test
    
    # Test remove_duplicates
    nums = [1,1,2]
    length = remove_duplicates(nums)
    assert length == 2
    assert nums[:length] == [1,2]
    
    print("All tests passed!")