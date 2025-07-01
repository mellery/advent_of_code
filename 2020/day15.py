#!/usr/bin/env python3
"""
Advent of Code 2020 Day 15: Rambunctious Recitation (OPTIMIZED)

High-performance Van Eck sequence implementation with major optimizations:
- Minimal memory allocation (no statistics tracking)
- Optimized loop structure (direct iteration)
- Eliminated object overhead (simple variables)
- No unnecessary features or tracking

Performance target: <10 seconds for 30M iterations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Any


def optimized_van_eck_sequence(starting_numbers: List[int], target_turn: int) -> int:
    """
    Optimized Van Eck sequence generator.
    
    Uses minimal memory and optimized loop structure for maximum performance.
    """
    if target_turn <= len(starting_numbers):
        return starting_numbers[target_turn - 1]
    
    # Dictionary to track last occurrence of each number
    # Only store what we need - no extra overhead
    last_spoken = {}
    
    # Initialize with starting numbers (except the last one)
    for i, num in enumerate(starting_numbers[:-1]):
        last_spoken[num] = i + 1  # 1-indexed
    
    # Current state
    current_number = starting_numbers[-1]
    current_turn = len(starting_numbers)
    
    # Direct loop with minimal overhead
    while current_turn < target_turn:
        # Calculate next number
        if current_number in last_spoken:
            next_number = current_turn - last_spoken[current_number]
        else:
            next_number = 0
        
        # Update state efficiently
        last_spoken[current_number] = current_turn
        current_number = next_number
        current_turn += 1
    
    return current_number


class Day15OptimizedSolution(AdventSolution):
    """Optimized solution for Advent of Code 2020 Day 15."""
    
    def __init__(self):
        super().__init__(year=2020, day=15, title="Rambunctious Recitation (Optimized)")
    
    def _parse_starting_numbers(self, input_data: str) -> List[int]:
        """Parse starting numbers efficiently."""
        line = input_data.strip()
        if ',' in line:
            return [int(x.strip()) for x in line.split(',')]
        else:
            return [int(x.strip()) for x in line.split()]
    
    def part1(self, input_data: str) -> Any:
        """Part 1: Find the 2020th number spoken."""
        starting_numbers = self._parse_starting_numbers(input_data)
        return optimized_van_eck_sequence(starting_numbers, 2020)
    
    def part2(self, input_data: str) -> Any:
        """Part 2: Find the 30000000th number spoken."""
        starting_numbers = self._parse_starting_numbers(input_data)
        return optimized_van_eck_sequence(starting_numbers, 30000000)


def main():
    """Main execution function."""
    solution = Day15OptimizedSolution()
    solution.main()


if __name__ == "__main__":
    main()