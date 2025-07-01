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
    
    def part1(self, filename: str) -> Any:
        """
        Find the floor Santa ends up on after following the instructions.
        
        Args:
            filename: Path to the input file
            
        Returns:
            The final floor number
        """
        lines = get_lines(filename)
        input_str = lines[0].strip()
        
        floor = 0
        for char in input_str:
            if char == "(":
                floor += 1
            elif char == ")":
                floor -= 1
        
        return floor
    
    def part2(self, filename: str) -> Any:
        """
        Find the position of the first character that causes Santa to enter the basement.
        
        Args:
            filename: Path to the input file
            
        Returns:
            The position (1-indexed) where Santa first enters floor -1
        """
        lines = get_lines(filename)
        input_str = lines[0].strip()
        
        floor = 0
        for pos, char in enumerate(input_str, 1):
            if char == "(":
                floor += 1
            elif char == ")":
                floor -= 1
            
            if floor == -1:
                return pos
        
        return pos


# Legacy functions for backward compatibility
def part1(input_str: str) -> int:
    """Legacy function for part 1."""
    floor = 0
    for char in input_str:
        if char == "(":
            floor += 1
        elif char == ")":
            floor -= 1
    return floor


def part2(input_str: str) -> int:
    """Legacy function for part 2."""
    floor = 0
    for pos, char in enumerate(input_str, 1):
        if char == "(":
            floor += 1
        elif char == ")":
            floor -= 1
        
        if floor == -1:
            return pos
    return pos


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
        
        print(f"Advent of Code 2015 - Day {day}")
        print(f"Using input file: {input_file}")
        print("-" * 40)
        
        # Run validation if test file exists
        test_file = args.test
        if os.path.exists(test_file) and not args.use_test:
            print("Running validation tests...")
            # Test with known examples
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