"""
Test cases for Arrays and Lists exercises
Run with: pytest tests/test_arrays_and_lists.py --pdb
"""
import pytest
import sys
import os

# Add the exercises directory to the path so we can import the functions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exercises', 'data_structures'))

from arrays_and_lists import (
    find_missing_number,
    two_sum,
    group_anagrams,
    remove_duplicates
)


class TestFindMissingNumber:
    def test_missing_2(self):
        result = find_missing_number([3,0,1])
        assert result == 2, f"find_missing_number([3,0,1]): expected 2, got {result}"

    def test_missing_2_from_small_array(self):
        result = find_missing_number([0,1])
        assert result == 2, f"find_missing_number([0,1]): expected 2, got {result}"

    def test_missing_8(self):
        result = find_missing_number([9,6,4,2,3,5,7,0,1])
        assert result == 8, f"find_missing_number([9,6,4,2,3,5,7,0,1]): expected 8, got {result}"


class TestTwoSum:
    def test_basic_case(self):
        result = two_sum([2,7,11,15], 9)
        assert result == [0,1], f"two_sum([2,7,11,15], 9): expected [0,1], got {result}"

    def test_different_indices(self):
        result = two_sum([3,2,4], 6)
        assert result == [1,2], f"two_sum([3,2,4], 6): expected [1,2], got {result}"


class TestGroupAnagrams:
    def test_basic_case(self):
        result = group_anagrams(["eat","tea","tan","ate","nat","bat"])
        # Convert to sets for comparison since order doesn't matter
        result_sets = [set(group) for group in result]
        expected_sets = [{"bat"}, {"nat","tan"}, {"ate","eat","tea"}]

        # Check that we have the right number of groups
        assert len(result_sets) == len(expected_sets), f"Expected {len(expected_sets)} groups, got {len(result_sets)}"

        # Check that each expected group is in the result
        for expected_group in expected_sets:
            assert expected_group in result_sets, f"Expected group {expected_group} not found in result {result_sets}"


class TestRemoveDuplicates:
    def test_basic_case(self):
        nums = [1,1,2]
        length = remove_duplicates(nums)
        assert length == 2, f"remove_duplicates([1,1,2]): expected length 2, got {length}"
        assert nums[:length] == [1,2], f"remove_duplicates([1,1,2]): expected [1,2] for first {length} elements, got {nums[:length]}"