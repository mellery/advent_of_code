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


# Legacy functions for backward compatibility with test runner
def get_binary_numbers(filename):
    """Legacy function for backward compatibility."""
    with open(filename) as f:
        lines = f.readlines()
        numbers = []
        for l in lines:
            numbers.append(l.strip())
        return numbers

def get_most_common_bit(binary_numbers, index):
    """Legacy function for backward compatibility."""
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

def part1(filename):
    """Legacy function for backward compatibility."""
    binary_numbers = get_binary_numbers(filename)
    gamma = []
    epsilon = []
    for i in range(0, len(binary_numbers[0])):
        if get_most_common_bit(binary_numbers, i):
            gamma.append(str(1))
            epsilon.append(str(0))
        else:
            gamma.append(str(0))
            epsilon.append(str(1))
    
    gamma_int = int("".join(gamma), 2)
    epsilon_int = int("".join(epsilon), 2)
    return gamma_int * epsilon_int

def part2(filename):
    """Legacy function for backward compatibility."""
    binary_numbers = get_binary_numbers(filename)
    for i in range(0, len(binary_numbers[0])):
        keep = str(get_most_common_bit(binary_numbers, i))
        new_list = binary_numbers.copy()
        for b in binary_numbers:
            if b[i] != keep:
                new_list.remove(b)
        binary_numbers = new_list.copy()
    oxygen_int = int(binary_numbers[0], 2)

    binary_numbers = get_binary_numbers(filename)
    for i in range(0, len(binary_numbers[0])):
        keep = str(get_most_common_bit(binary_numbers, i))
        
        if keep == "1":
            keep = "0"
        elif keep == "0":
            keep = "1"
        new_list = binary_numbers.copy()
        if len(new_list) > 1:
            for b in binary_numbers:
                if str(b[i]) != str(keep):
                    new_list.remove(b)
        binary_numbers = new_list.copy()

    co2_int = int(binary_numbers[0], 2)
    return oxygen_int * co2_int

def main():
    """Main function - can be called in legacy mode or new mode."""
    # Check if we're being run directly with arguments or imported
    if len(sys.argv) > 1 or '--test' in sys.argv or '--time' in sys.argv:
        # New AdventSolution mode
        solution = Day3Solution()
        solution.main()
    else:
        # Legacy mode for compatibility
        print(part2("day3_input.txt"))

if __name__ == "__main__":
    main()