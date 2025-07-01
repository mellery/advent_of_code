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



def main():
    """Main execution function."""
    solution = Day1Solution()
    solution.main()

if __name__ == "__main__":
    main()