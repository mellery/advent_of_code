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


# Legacy functions for backward compatibility with test runner
def get_list_of_numbers(filename):
    """Legacy function for backward compatibility."""
    with open(filename) as f:
        lines = f.readlines()
        numbers = []
        for l in lines:
            number = int(l)
            numbers.append(number)
    return numbers

def part1(filename):
    """Legacy function for backward compatibility."""
    numbers = get_list_of_numbers(filename)
    last_number = numbers[0]
    increases = 0

    for n in numbers[1:]:
        if n > last_number:
            increases += 1
        last_number = n
    return increases

def part2(filename):
    """Legacy function for backward compatibility."""
    numbers = get_list_of_numbers(filename)
    last_number = numbers[0] + numbers[1] + numbers[2]
    increases = 0

    for i in range(1, len(numbers) - 2):
        nsum = numbers[i] + numbers[i + 1] + numbers[i + 2]
        if nsum > last_number:
            increases += 1
        last_number = nsum
    return increases

def main():
    """Main function - can be called in legacy mode or new mode."""
    # Check if we're being run directly or imported
    if len(sys.argv) > 1 or '--test' in sys.argv or '--time' in sys.argv:
        # New AdventSolution mode
        solution = Day1Solution()
        solution.main()
    else:
        # Legacy mode for compatibility
        print(part1("day1_input.txt"))
        print(part2("day1_input.txt"))

if __name__ == "__main__":
    main()