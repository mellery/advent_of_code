#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 7: The Treachery of Whales

Optimizing crab submarine fuel consumption for alignment.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from functools import lru_cache
from typing import List, Any


class Day7Solution(AdventSolution):
    """Solution for Advent of Code 2021 Day 7."""
    
    def __init__(self):
        super().__init__(2021, 7, "The Treachery of Whales")
    
    def _parse_input(self, input_data: str) -> List[int]:
        """Parse input data into list of crab positions."""
        return [int(x) for x in input_data.strip().split(',')]
    
    @lru_cache(maxsize=None)
    def _calc_fuel(self, distance: int) -> int:
        """Calculate fuel cost for given distance (triangular number)."""
        return sum(range(distance + 1))
    
    def part1(self, input_data: str) -> int:
        """Find minimum fuel cost with linear fuel consumption."""
        positions = self._parse_input(input_data)
        min_fuel = sys.maxsize
        
        for target_pos in range(min(positions), max(positions) + 1):
            fuel = sum(abs(pos - target_pos) for pos in positions)
            min_fuel = min(min_fuel, fuel)
        
        return min_fuel
    
    def part2(self, input_data: str) -> int:
        """Find minimum fuel cost with increasing fuel consumption."""
        positions = self._parse_input(input_data)
        min_fuel = sys.maxsize
        
        for target_pos in range(min(positions), max(positions) + 1):
            fuel = sum(self._calc_fuel(abs(pos - target_pos)) for pos in positions)
            min_fuel = min(min_fuel, fuel)
        
        return min_fuel


# Legacy functions for backward compatibility with test runner
def parse_input(input_data):
    """Parse input data - could be filename or data content."""
    if isinstance(input_data, str):
        # If it's a string, check if it's a filename or data
        if '\n' in input_data or ',' in input_data:
            # It's data content
            return [int(x) for x in input_data.strip().split(',')]
        else:
            # It's a filename
            try:
                with open(input_data, 'r') as f:
                    return [int(x) for x in f.read().strip().split(',')]
            except FileNotFoundError:
                # If file doesn't exist, assume it's a single number
                return [int(input_data)]
    elif isinstance(input_data, list):
        return input_data
    else:
        return [int(input_data)]

@lru_cache(maxsize=None)
def calc_fuel(upper):
    return sum(range(0, (upper) + 1))

def part1(input_data):
    input_list = parse_input(input_data)
    ans = sys.maxsize
    for pos in range(0, len(input_list)):
        total = 0
        for i in range(0, len(input_list)):
            total += abs(input_list[i] - input_list[pos])
        if total < ans:
            ans = total
    return ans

def part2(input_data):
    input_list = parse_input(input_data)
    ans = sys.maxsize
    for pos in range(0, len(input_list)):
        total = 0
        for i in range(0, len(input_list)):
            total += calc_fuel(abs(input_list[i] - pos))
        if total < ans:
            ans = total
    return ans

def main():
    """Main function - can be called in legacy mode or new mode."""
    # Check if we're being run directly with arguments or imported
    if len(sys.argv) > 1 or '--test' in sys.argv or '--time' in sys.argv:
        # New AdventSolution mode
        solution = Day7Solution()
        solution.main()
    else:
        # Legacy mode for compatibility
        with open("day7_input.txt", 'r') as f:
            data = f.read().strip()
        print(part2(data))

if __name__ == "__main__":
    main()
