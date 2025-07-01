#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 8: Seven Segment Search

Decoding seven-segment displays with scrambled wiring.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    get_lines, setup_day_args, find_input_file, validate_solution, run_solution
)
from utils.advent_base import AdventSolution
from typing import Any, Dict, List, Set


def decode_display(patterns: List[str], outputs: List[str]) -> int:
    """Decode a single display's output value."""
    # Sort patterns by length for easier identification
    patterns_by_len = {}
    for pattern in patterns:
        length = len(pattern)
        if length not in patterns_by_len:
            patterns_by_len[length] = []
        patterns_by_len[length].append(set(pattern))
    
    # Known digit patterns by segment count
    digit_map = {}
    
    # Easy digits with unique segment counts
    digit_map[1] = patterns_by_len[2][0]  # Only digit with 2 segments
    digit_map[4] = patterns_by_len[4][0]  # Only digit with 4 segments  
    digit_map[7] = patterns_by_len[3][0]  # Only digit with 3 segments
    digit_map[8] = patterns_by_len[7][0]  # Only digit with 7 segments
    
    # Digits with 6 segments: 0, 6, 9
    six_segment_patterns = patterns_by_len[6]
    
    # Digit 6 is the only 6-segment digit that doesn't contain all segments of digit 1
    for pattern in six_segment_patterns:
        if not digit_map[1].issubset(pattern):
            digit_map[6] = pattern
            break
    
    # Digit 9 contains all segments of digit 4
    for pattern in six_segment_patterns:
        if pattern != digit_map[6] and digit_map[4].issubset(pattern):
            digit_map[9] = pattern
            break
    
    # Digit 0 is the remaining 6-segment digit
    for pattern in six_segment_patterns:
        if pattern != digit_map[6] and pattern != digit_map[9]:
            digit_map[0] = pattern
            break
    
    # Digits with 5 segments: 2, 3, 5
    five_segment_patterns = patterns_by_len[5]
    
    # Digit 3 contains all segments of digit 1
    for pattern in five_segment_patterns:
        if digit_map[1].issubset(pattern):
            digit_map[3] = pattern
            break
    
    # Digit 5 is contained within digit 6
    for pattern in five_segment_patterns:
        if pattern != digit_map[3] and pattern.issubset(digit_map[6]):
            digit_map[5] = pattern
            break
    
    # Digit 2 is the remaining 5-segment digit
    for pattern in five_segment_patterns:
        if pattern != digit_map[3] and pattern != digit_map[5]:
            digit_map[2] = pattern
            break
    
    # Create reverse mapping for decoding
    pattern_to_digit = {}
    for digit, pattern in digit_map.items():
        pattern_to_digit[frozenset(pattern)] = str(digit)
    
    # Decode output digits
    result = ""
    for output in outputs:
        output_set = frozenset(output)
        result += pattern_to_digit[output_set]
    
    return int(result)


class Day8Solution(AdventSolution):
    """Day 8: Seven Segment Search"""
    
    def __init__(self):
        super().__init__(2021, 8, "Seven Segment Search")
    
    def part1(self, filename: str) -> Any:
        """
        Count how many times digits 1, 4, 7, or 8 appear in the output values.
        
        Args:
            filename: Path to the input file
            
        Returns:
            Count of digits 1, 4, 7, 8 in output values
        """
        lines = get_lines(filename)
        count = 0
        
        for line in lines:
            # Split input and output parts
            output_part = line.split('|')[1].strip()
            output_digits = output_part.split()
            
            # Count digits with unique segment counts
            for digit in output_digits:
                segment_count = len(digit)
                # Check if it's digit 1, 4, 7, or 8 based on segment count
                if segment_count in [2, 4, 3, 7]:  # 1, 4, 7, 8 respectively
                    count += 1
        
        return count
    
    def part2(self, filename: str) -> Any:
        """
        Decode all displays and sum their output values.
        
        Args:
            filename: Path to the input file
            
        Returns:
            Sum of all decoded output values
        """
        lines = get_lines(filename)
        total = 0
        
        for line in lines:
            # Split input and output parts
            parts = line.strip().split('|')
            patterns = parts[0].strip().split()
            outputs = parts[1].strip().split()
            
            # Decode this display and add to total
            value = decode_display(patterns, outputs)
            total += value
        
        return total


# Legacy functions for backward compatibility
def part1(filename: str) -> Any:
    """Legacy function for part 1."""
    solution = Day8Solution()
    return solution.part1(filename)


def part2(filename: str) -> Any:
    """Legacy function for part 2."""
    solution = Day8Solution()
    return solution.part2(filename)


def main():
    """Main function to run the solution."""
    solution = Day8Solution()
    
    # Check if we're being called by the legacy test runner
    if len(sys.argv) > 1 and '--legacy' in sys.argv:
        # Legacy mode - use the old approach
        day = '8'
        args = setup_day_args(day)
        
        # Determine input file
        if args.use_test:
            input_file = args.test
        else:
            input_file = find_input_file(day) or args.input
        
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found")
            return
        
        print(f"Advent of Code 2021 - Day {day}")
        print(f"Using input file: {input_file}")
        print("-" * 40)
        
        # Run validation if test file exists
        test_file = args.test
        if os.path.exists(test_file) and not args.use_test:
            print("Running validation tests...")
            validate_solution(part1, part2, test_file, 
                            expected_part1=26, expected_part2=61229)
            print("-" * 40)
        
        # Run the actual solution
        run_solution(part1, part2, input_file, args)
    else:
        # Enhanced mode - use AdventSolution
        solution.run()


if __name__ == "__main__":
    main()