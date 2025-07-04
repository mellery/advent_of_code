#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 1: Sonar Sweep

Counting depth measurement increases.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Any


class Day1Solution(AdventSolution):
    """Solution for Advent of Code 2021 Day 1."""
    
    def __init__(self):
        super().__init__(2021, 1, "Sonar Sweep")
    
    def _get_list_of_numbers(self, input_data: str) -> List[int]:
        """Parse input data into list of numbers."""
        return [int(line.strip()) for line in input_data.strip().split('\n') if line.strip()]
    
    def part1(self, input_data: str) -> int:
        """Count increases in depth measurements."""
        numbers = self._get_list_of_numbers(input_data)
        last_number = numbers[0]
        increases = 0

        for n in numbers[1:]:
            if n > last_number:
                increases += 1
            last_number = n
        return increases
    
    def part2(self, input_data: str) -> int:
        """Count increases in three-measurement sliding window sums."""
        numbers = self._get_list_of_numbers(input_data)
        last_number = numbers[0] + numbers[1] + numbers[2]
        increases = 0

        for i in range(1, len(numbers) - 2):
            nsum = numbers[i] + numbers[i + 1] + numbers[i + 2]
            if nsum > last_number:
                increases += 1
            last_number = nsum
        return increases

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """199
200
208
210
200
207
240
269
260
263"""
        expected_part1 = 7
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
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