#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 14: Extended Polymerization

Simulating polymer growth using pair insertion rules.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    get_lines, setup_day_args, find_input_file, validate_solution, run_solution
)
from utils.advent_base import AdventSolution
from typing import Any, Dict, Tuple
from collections import defaultdict


def parse_input(filename: str) -> Tuple[str, Dict[str, str]]:
    """Parse the polymer template and insertion rules."""
    lines = get_lines(filename)
    template = lines[0].strip()
    
    rules = {}
    for line in lines[2:]:  # Skip empty line at index 1
        if '->' in line:
            pair, insert = line.strip().split(' -> ')
            rules[pair] = insert
    
    return template, rules


def solve_polymerization(template: str, rules: Dict[str, str], steps: int) -> int:
    """Solve polymerization efficiently using pair counting."""
    # Count initial pairs
    pair_counts = defaultdict(int)
    for i in range(len(template) - 1):
        pair = template[i:i+2]
        pair_counts[pair] += 1
    
    # Apply insertion rules for specified steps
    for step in range(steps):
        new_pair_counts = defaultdict(int)
        
        for pair, count in pair_counts.items():
            if pair in rules:
                insert_char = rules[pair]
                # One pair AB with insertion C becomes AC and CB
                left_pair = pair[0] + insert_char
                right_pair = insert_char + pair[1]
                
                new_pair_counts[left_pair] += count
                new_pair_counts[right_pair] += count
            else:
                # No rule for this pair, keep as is
                new_pair_counts[pair] += count
        
        pair_counts = new_pair_counts
    
    # Count character frequencies
    char_counts = defaultdict(int)
    
    # Count first character of each pair
    for pair, count in pair_counts.items():
        char_counts[pair[0]] += count
    
    # Add the last character of the original template
    # (it never changes as it's always at the end)
    char_counts[template[-1]] += 1
    
    # Calculate difference between most and least common
    max_count = max(char_counts.values())
    min_count = min(char_counts.values())
    
    return max_count - min_count


class Day14Solution(AdventSolution):
    """Day 14: Extended Polymerization"""
    
    def __init__(self):
        super().__init__(2021, 14, "Extended Polymerization")
    
    def part1(self, filename: str) -> Any:
        """
        Apply polymer insertion rules for 10 steps.
        
        Args:
            filename: Path to the input file
            
        Returns:
            Difference between most and least common elements after 10 steps
        """
        template, rules = parse_input(filename)
        return solve_polymerization(template, rules, 10)
    
    def part2(self, filename: str) -> Any:
        """
        Apply polymer insertion rules for 40 steps.
        
        Args:
            filename: Path to the input file
            
        Returns:
            Difference between most and least common elements after 40 steps
        """
        template, rules = parse_input(filename)
        return solve_polymerization(template, rules, 40)


# Legacy functions for backward compatibility
def part1(filename: str) -> Any:
    """Legacy function for part 1."""
    solution = Day14Solution()
    return solution.part1(filename)


def part2(filename: str) -> Any:
    """Legacy function for part 2."""
    solution = Day14Solution()
    return solution.part2(filename)


def main():
    """Main function to run the solution."""
    solution = Day14Solution()
    
    # Check if we're being called by the legacy test runner
    if len(sys.argv) > 1 and '--legacy' in sys.argv:
        # Legacy mode - use the old approach
        day = '14'
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
                            expected_part1=1588, expected_part2=2188189693529)
            print("-" * 40)
        
        # Run the actual solution
        run_solution(part1, part2, input_file, args)
    else:
        # Enhanced mode - use AdventSolution
        solution.run()


if __name__ == "__main__":
    main()