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

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """16,1,2,0,4,2,7,1,2,14"""
        expected_part1 = 37

        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        expected_part2 = 168

        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False

        print("✅ All Day 7 validation tests passed!")
        return True



def main():
    """Main execution function."""
    solution = Day7Solution()
    solution.main()

if __name__ == "__main__":
    main()
