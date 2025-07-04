#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 3: Binary Diagnostic

Analyzing binary numbers for power consumption and life support ratings.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Any


class Day3Solution(AdventSolution):
    """Solution for Advent of Code 2021 Day 3."""
    
    def __init__(self):
        super().__init__(2021, 3, "Binary Diagnostic")
    
    def _get_binary_numbers(self, input_data: str) -> List[str]:
        """Parse input data into list of binary numbers."""
        return [line.strip() for line in input_data.strip().split('\n') if line.strip()]
    
    def _get_most_common_bit(self, binary_numbers: List[str], index: int) -> int:
        """Get the most common bit at given index position."""
        one_count = 0
        zero_count = 0
        for b in binary_numbers:
            if int(b[index]) == 1:
                one_count += 1
            else:
                zero_count += 1
        if one_count >= zero_count:
            return 1
        else:
            return 0
    
    def part1(self, input_data: str) -> int:
        """Calculate power consumption from gamma and epsilon rates."""
        binary_numbers = self._get_binary_numbers(input_data)
        gamma = []
        epsilon = []
        
        for i in range(len(binary_numbers[0])):
            if self._get_most_common_bit(binary_numbers, i):
                gamma.append('1')
                epsilon.append('0')
            else:
                gamma.append('0')
                epsilon.append('1')
        
        gamma_int = int(''.join(gamma), 2)
        epsilon_int = int(''.join(epsilon), 2)
        return gamma_int * epsilon_int
    
    def part2(self, input_data: str) -> int:
        """Calculate life support rating from oxygen and CO2 scrubber ratings."""
        # Calculate oxygen generator rating
        binary_numbers = self._get_binary_numbers(input_data)
        for i in range(len(binary_numbers[0])):
            if len(binary_numbers) <= 1:
                break
            keep = str(self._get_most_common_bit(binary_numbers, i))
            binary_numbers = [b for b in binary_numbers if b[i] == keep]
        oxygen_int = int(binary_numbers[0], 2)
        
        # Calculate CO2 scrubber rating
        binary_numbers = self._get_binary_numbers(input_data)
        for i in range(len(binary_numbers[0])):
            if len(binary_numbers) <= 1:
                break
            keep = str(self._get_most_common_bit(binary_numbers, i))
            # Use least common bit for CO2 scrubber
            keep = '0' if keep == '1' else '1'
            binary_numbers = [b for b in binary_numbers if b[i] == keep]
        co2_int = int(binary_numbers[0], 2)
        
        return oxygen_int * co2_int

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
        expected_part1 = 198
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        expected_part2 = 230
        
        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False

        print("✅ All Day 3 validation tests passed!")
        return True

def main():
    """Main execution function."""
    solution = Day3Solution()
    solution.main()

if __name__ == "__main__":
    main()