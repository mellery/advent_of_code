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
    
    def part1(self, filename: str) -> Any:
        """
        Find the sum of all digits that match the next digit in the circular list.
        
        Args:
            filename: Path to the input file
            
        Returns:
            Sum of matching digits
        """
        lines = get_lines(filename)
        input_str = lines[0].strip()
        
        digits = [int(c) for c in input_str]
        total = 0
        
        # Check each digit against the next one (circular)
        for i in range(len(digits)):
            next_index = (i + 1) % len(digits)
            if digits[i] == digits[next_index]:
                total += digits[i]
        
        return total
    
    def part2(self, filename: str) -> Any:
        """
        Find the sum of all digits that match the digit halfway around the circular list.
        
        Args:
            filename: Path to the input file
            
        Returns:
            Sum of matching digits
        """
        lines = get_lines(filename)
        input_str = lines[0].strip()
        
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


# Legacy functions for backward compatibility
def part1(number_input) -> int:
    """Legacy function for part 1."""
    nstr = str(number_input)
    digits = [int(c) for c in nstr]
    total = 0
    
    # Check consecutive digits
    for i in range(len(digits) - 1):
        if digits[i] == digits[i + 1]:
            total += digits[i]
    
    # Check last digit against first (circular)
    if digits[-1] == digits[0]:
        total += digits[-1]
    
    return total


def part2(number_input) -> int:
    """Legacy function for part 2."""
    nstr = str(number_input)
    digits = [int(c) for c in nstr]
    length = len(digits)
    half_way = length // 2
    total = 0
    
    # Check each digit against the one halfway around
    for i in range(length):
        half_index = (i + half_way) % length
        if digits[i] == digits[half_index]:
            total += digits[i]
    
    return total


def main():
    """Main function to run the solution."""
    solution = Day1Solution()
    
    # Check if we're being called by the legacy test runner
    if len(sys.argv) > 1 and '--legacy' in sys.argv:
        # Legacy mode - use the old approach
        day = '1'
        args = setup_day_args(day)
        
        # Determine input file
        if args.use_test:
            input_file = args.test
        else:
            input_file = find_input_file(day) or args.input
        
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found")
            return
        
        print(f"Advent of Code 2017 - Day {day}")
        print(f"Using input file: {input_file}")
        print("-" * 40)
        
        # Run validation if test file exists
        test_file = args.test
        if os.path.exists(test_file) and not args.use_test:
            print("Running validation tests...")
            validate_solution(
                lambda f: solution.part1(f), 
                lambda f: solution.part2(f), 
                test_file,
                expected_part1=None, expected_part2=None
            )
            print("-" * 40)
        
        # Run the actual solution
        run_solution(
            lambda f: solution.part1(f), 
            lambda f: solution.part2(f), 
            input_file, args
        )
    else:
        # Enhanced mode - use AdventSolution
        solution.run()


if __name__ == "__main__":
    main()