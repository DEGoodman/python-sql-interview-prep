"""
Test cases for Hash Maps and Sets exercises
Run with: pytest tests/test_hash_maps_and_sets.py --pdb
"""
import pytest
import sys
import os

# Add the exercises directory to the path so we can import the functions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exercises', 'data_structures'))

from hash_maps_and_sets import (
    first_uniq_char,
    is_anagram,
    top_k_frequent,
    intersection,
    subarray_sum
)


class TestFirstUniqChar:
    def test_leetcode(self):
        result = first_uniq_char("leetcode")
        assert result == 0, f"first_uniq_char('leetcode'): expected 0, got {result}"

    def test_loveleetcode(self):
        result = first_uniq_char("loveleetcode")
        assert result == 2, f"first_uniq_char('loveleetcode'): expected 2, got {result}"

    def test_aabb(self):
        result = first_uniq_char("aabb")
        assert result == -1, f"first_uniq_char('aabb'): expected -1, got {result}"


class TestIsAnagram:
    def test_anagram_nagagram(self):
        result = is_anagram("anagram", "nagaram")
        assert result == True, f"is_anagram('anagram', 'nagaram'): expected True, got {result}"

    def test_rat_car(self):
        result = is_anagram("rat", "car")
        assert result == False, f"is_anagram('rat', 'car'): expected False, got {result}"


class TestTopKFrequent:
    def test_basic_case(self):
        result = top_k_frequent([1,1,1,2,2,3], 2)
        assert set(result) == {1, 2}, f"top_k_frequent([1,1,1,2,2,3], 2): expected {{1, 2}}, got {set(result)}"


class TestIntersection:
    def test_simple_case(self):
        result = intersection([1,2,2,1], [2,2])
        assert set(result) == {2}, f"intersection([1,2,2,1], [2,2]): expected {{2}}, got {set(result)}"

    def test_multiple_elements(self):
        result = intersection([4,9,5], [9,4,9,8,4])
        assert set(result) == {4, 9}, f"intersection([4,9,5], [9,4,9,8,4]): expected {{4, 9}}, got {set(result)}"


class TestSubarraySum:
    def test_ones_case(self):
        result = subarray_sum([1,1,1], 2)
        assert result == 2, f"subarray_sum([1,1,1], 2): expected 2, got {result}"

    def test_mixed_case(self):
        result = subarray_sum([1,2,3], 3)
        assert result == 2, f"subarray_sum([1,2,3], 3): expected 2, got {result}"