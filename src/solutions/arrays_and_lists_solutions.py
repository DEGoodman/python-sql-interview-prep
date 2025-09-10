"""
Solutions to Array and List Data Structure Exercises
Try solving exercises/data_structures/arrays_and_lists.py first!
"""

def find_missing_number(nums):
    """
    Given an array containing n distinct numbers taken from 0, 1, 2, ..., n,
    find the one number that is missing from the array.
    
    Time: O(n), Space: O(1)
    """
    n = len(nums)
    # Sum of 0 to n is n*(n+1)/2
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum

def two_sum(nums, target):
    """
    Given an array of integers and a target sum, return indices of two numbers
    that add up to the target.
    
    Time: O(n), Space: O(n)
    """
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

def group_anagrams(strs):
    """
    Group strings that are anagrams of each other.
    
    Time: O(n*m*log(m)) where n=len(strs), m=avg string length
    Space: O(n*m)
    """
    from collections import defaultdict
    groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        key = ''.join(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())

def remove_duplicates(nums):
    """
    Remove duplicates from sorted array in-place and return new length.
    
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    
    # Two pointers approach
    write_index = 1
    for read_index in range(1, len(nums)):
        if nums[read_index] != nums[read_index - 1]:
            nums[write_index] = nums[read_index]
            write_index += 1
    
    return write_index

# Test cases
if __name__ == "__main__":
    # Test find_missing_number
    assert find_missing_number([3,0,1]) == 2
    assert find_missing_number([0,1]) == 2
    assert find_missing_number([9,6,4,2,3,5,7,0,1]) == 8
    print("✅ find_missing_number tests passed")
    
    # Test two_sum
    assert two_sum([2,7,11,15], 9) == [0,1]
    assert two_sum([3,2,4], 6) == [1,2]
    print("✅ two_sum tests passed")
    
    # Test group_anagrams (order doesn't matter)
    result = group_anagrams(["eat","tea","tan","ate","nat","bat"])
    result_sets = [set(group) for group in result]
    expected_sets = [{"eat","tea","ate"}, {"tan","nat"}, {"bat"}]
    assert all(expected in result_sets for expected in expected_sets)
    print("✅ group_anagrams tests passed")
    
    # Test remove_duplicates
    nums = [1,1,2]
    length = remove_duplicates(nums)
    assert length == 2
    assert nums[:length] == [1,2]
    
    nums2 = [0,0,1,1,1,2,2,3,3,4]
    length2 = remove_duplicates(nums2)
    assert length2 == 5
    assert nums2[:length2] == [0,1,2,3,4]
    print("✅ remove_duplicates tests passed")
    
    print("All tests passed!")