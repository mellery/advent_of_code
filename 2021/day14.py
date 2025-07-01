#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 14: Extended Polymerization

Simulating polymer growth using pair insertion rules.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import Any, Dict, Tuple
from collections import defaultdict


def parse_input_from_data(input_data: str) -> Tuple[str, Dict[str, str]]:
    """Parse the polymer template and insertion rules."""
    lines = input_data.strip().split('\n')
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
    
    def part1(self, input_data: str) -> Any:
        """
        Apply polymer insertion rules for 10 steps.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Difference between most and least common elements after 10 steps
        """
        template, rules = parse_input_from_data(input_data)
        return solve_polymerization(template, rules, 10)
    
    def part2(self, input_data: str) -> Any:
        """
        Apply polymer insertion rules for 40 steps.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Difference between most and least common elements after 40 steps
        """
        template, rules = parse_input_from_data(input_data)
        return solve_polymerization(template, rules, 40)


def main():
    """Main execution function."""
    solution = Day14Solution()
    solution.main()


if __name__ == "__main__":
    main()