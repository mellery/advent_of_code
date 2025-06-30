#!/usr/bin/env python3
"""
Advent of Code 2020 Day 9: Encoding Error
https://adventofcode.com/2020/day/9

XMAS cypher validation and weakness finding.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, List, Optional

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class Day9Solution(AdventSolution):
    """Solution for 2020 Day 9: Encoding Error."""

    def __init__(self):
        super().__init__(2020, 9, "Encoding Error")

    def is_valid_xmas(self, preamble: List[int], target: int) -> bool:
        """
        Check if target can be formed by summing two different numbers from preamble.
        
        Args:
            preamble: List of previous numbers to check against
            target: Number to validate
            
        Returns:
            True if target is valid (can be formed by sum of two preamble numbers)
        """
        for i, x in enumerate(preamble):
            for j, y in enumerate(preamble):
                if i != j and x + y == target:
                    return True
        return False

    def find_invalid_number(self, numbers: List[int], preamble_size: int = 25) -> Optional[int]:
        """
        Find the first number that doesn't follow the XMAS rule.
        
        Args:
            numbers: List of all numbers in the stream
            preamble_size: Size of the preamble to check against
            
        Returns:
            The first invalid number, or None if all are valid
        """
        for i in range(preamble_size, len(numbers)):
            current_number = numbers[i]
            preamble = numbers[i - preamble_size:i]
            
            if not self.is_valid_xmas(preamble, current_number):
                return current_number
                
        return None

    def find_encryption_weakness(self, numbers: List[int], target: int) -> Optional[int]:
        """
        Find a contiguous range of numbers that sum to target.
        
        Args:
            numbers: List of all numbers in the stream
            target: The target sum to find
            
        Returns:
            Sum of min and max from the contiguous range, or None if not found
        """
        for start in range(len(numbers)):
            current_sum = 0
            end = start
            
            # Keep adding numbers until we reach or exceed the target
            while current_sum < target and end < len(numbers):
                current_sum += numbers[end]
                end += 1
            
            # If we found the exact sum and it's a range of at least 2 numbers
            if current_sum == target and end - start >= 2:
                range_numbers = numbers[start:end]
                return min(range_numbers) + max(range_numbers)
                
        return None

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Find the first invalid number in the XMAS stream.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            The first number that doesn't follow the XMAS rule
        """
        parser = InputParser(input_data)
        numbers = parser.as_integers()
        
        invalid_number = self.find_invalid_number(numbers)
        if invalid_number is None:
            raise ValueError("No invalid number found in the stream")
            
        return invalid_number

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Find the encryption weakness.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Sum of the smallest and largest numbers in the contiguous range
        """
        parser = InputParser(input_data)
        numbers = parser.as_integers()
        
        # First find the invalid number from part 1
        invalid_number = self.find_invalid_number(numbers)
        if invalid_number is None:
            raise ValueError("No invalid number found in the stream")
        
        # Then find the encryption weakness
        weakness = self.find_encryption_weakness(numbers, invalid_number)
        if weakness is None:
            raise ValueError(f"No contiguous range found that sums to {invalid_number}")
            
        return weakness

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test the XMAS validation logic with examples from the problem
        test_preamble = list(range(1, 26))  # 1 to 25
        
        # These should be valid
        if not self.is_valid_xmas(test_preamble, 26):  # 1 + 25
            print("Validation failed: 26 should be valid")
            return False
        if not self.is_valid_xmas(test_preamble, 49):  # 24 + 25
            print("Validation failed: 49 should be valid")
            return False
            
        # This should be invalid
        if self.is_valid_xmas(test_preamble, 100):
            print("Validation failed: 100 should be invalid")
            return False
            
        # This should be invalid (would require 25 + 25)
        if self.is_valid_xmas(test_preamble, 50):
            print("Validation failed: 50 should be invalid")
            return False
            
        print("✅ All Day 9 validation tests passed!")
        return True


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day9Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day9Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main function to run the solution."""
    solution = Day9Solution()
    solution.main()


if __name__ == "__main__":
    main()