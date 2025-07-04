#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 2: Dive!

Navigating a submarine with commands.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Tuple, Any


class Day2Solution(AdventSolution):
    """Solution for Advent of Code 2021 Day 2."""
    
    def __init__(self):
        super().__init__(2021, 2, "Dive!")
    
    def _get_instructions(self, input_data: str) -> Tuple[List[str], List[int]]:
        """Parse input data into commands and numbers."""
        lines = input_data.strip().split('\n')
        commands = []
        numbers = []
        for line in lines:
            if line.strip():
                parts = line.strip().split(' ')
                commands.append(parts[0])
                numbers.append(int(parts[1]))
        return commands, numbers
    
    def part1(self, input_data: str) -> int:
        """Calculate final position using simple movement rules."""
        horizontal = 0
        depth = 0
        commands, numbers = self._get_instructions(input_data)
        
        for i in range(len(commands)):
            if commands[i] == 'forward':
                horizontal += numbers[i]
            elif commands[i] == 'down':
                depth += numbers[i]
            elif commands[i] == 'up':
                depth -= numbers[i]
        
        return horizontal * depth
    
    def part2(self, input_data: str) -> int:
        """Calculate final position using aim-based movement rules."""
        horizontal = 0
        depth = 0
        aim = 0
        commands, numbers = self._get_instructions(input_data)
        
        for i in range(len(commands)):
            if commands[i] == 'forward':
                horizontal += numbers[i]
                depth += numbers[i] * aim
            elif commands[i] == 'down':
                aim += numbers[i]
            elif commands[i] == 'up':
                aim -= numbers[i]
        
        return horizontal * depth

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""
        expected_part1 = 150
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        expected_part2 = 900
        
        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False

        print("✅ All Day 2 validation tests passed!")
        return True

def main():
    """Main execution function."""
    solution = Day2Solution()
    solution.main()

if __name__ == "__main__":
    main()