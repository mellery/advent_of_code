#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 1: Not Quite Lisp

Santa is trying to deliver presents in a large apartment building, but he can't find the right floor.
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
    """Day 1: Not Quite Lisp"""
    
    def __init__(self):
        super().__init__(2015, 1, "Not Quite Lisp")
    
    def part1(self, input_data: str) -> Any:
        """
        Find the floor Santa ends up on after following the instructions.
        
        Args:
            input_data: Raw input data containing the instructions
            
        Returns:
            The final floor number
        """
        input_str = input_data.strip()
        
        floor = 0
        for char in input_str:
            if char == "(":
                floor += 1
            elif char == ")":
                floor -= 1
        
        return floor
    
    def part2(self, input_data: str) -> Any:
        """
        Find the position of the first character that causes Santa to enter the basement.
        
        Args:
            input_data: Raw input data containing the instructions
            
        Returns:
            The position (1-indexed) where Santa first enters floor -1
        """
        input_str = input_data.strip()
        
        floor = 0
        for pos, char in enumerate(input_str, 1):
            if char == "(":
                floor += 1
            elif char == ")":
                floor -= 1
            
            if floor == -1:
                return pos
        
        return pos

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """)())())"""
        expected_part1 = -3

        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        example_input = """()())"""
        expected_part2 = 5
        
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