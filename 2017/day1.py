#!/usr/bin/env python3
"""
Advent of Code 2017 - Day 1: Inverse Captcha

You need to solve a captcha by finding digits that match specific criteria.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    get_lines, setup_day_args, find_input_file, validate_solution, run_solution
)
from utils.advent_base import AdventSolution
from typing import Any


class Day1Solution(AdventSolution):
    """Day 1: Inverse Captcha"""
    
    def __init__(self):
        super().__init__(2017, 1, "Inverse Captcha")
    
    def part1(self, input_data: str) -> Any:
        """
        Find the sum of all digits that match the next digit in the circular list.
        
        Args:
            input_data: Raw input data containing the digit sequence
            
        Returns:
            Sum of matching digits
        """
        input_str = input_data.strip()
        
        digits = [int(c) for c in input_str]
        total = 0
        
        # Check each digit against the next one (circular)
        for i in range(len(digits)):
            next_index = (i + 1) % len(digits)
            if digits[i] == digits[next_index]:
                total += digits[i]
        
        return total
    
    def part2(self, input_data: str) -> Any:
        """
        Find the sum of all digits that match the digit halfway around the circular list.
        
        Args:
            input_data: Raw input data containing the digit sequence
            
        Returns:
            Sum of matching digits
        """
        input_str = input_data.strip()
        
        digits = [int(c) for c in input_str]
        length = len(digits)
        half_way = length // 2
        total = 0
        
        # Check each digit against the one halfway around
        for i in range(length):
            half_index = (i + half_way) % length
            if digits[i] == digits[half_index]:
                total += digits[i]
        
        return total

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """91212129"""
        expected_part1 = 9

        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        example_input = """12131415"""
        expected_part2 = 4
                
        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False
        
        print("✅ All Day 1 validation tests passed!")
        return True
    
def main():
    """Main execution function."""
    solution = Day1Solution()
    solution.main()


if __name__ == "__main__":
    main()