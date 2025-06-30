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


# Legacy functions for backward compatibility with test runner
def get_instructions(filename):
    """Legacy function for backward compatibility."""
    with open(filename) as f:
        lines = f.readlines()
        numbers = []
        commands = []
        for l in lines:
            commands.append(l.split(' ')[0])
            numbers.append(int(l.split(' ')[1].strip()))
        return commands, numbers

def part1(filename):
    """Legacy function for backward compatibility."""
    horizontal = 0
    depth = 0
    commands, numbers = get_instructions(filename)
    for i in range(0, len(commands)):
        if commands[i] == 'forward':
            horizontal += numbers[i]
        if commands[i] == 'down':
            depth += numbers[i]
        if commands[i] == 'up':
            depth -= numbers[i]
    return horizontal * depth

def part2(filename):
    """Legacy function for backward compatibility."""
    horizontal = 0
    depth = 0
    aim = 0
    commands, numbers = get_instructions(filename)
    for i in range(0, len(commands)):
        if commands[i] == 'forward':
            horizontal += numbers[i]
            depth += numbers[i] * aim
        if commands[i] == 'down':
            aim += numbers[i]
        if commands[i] == 'up':
            aim -= numbers[i]
    return horizontal * depth

def main():
    """Main function - can be called in legacy mode or new mode."""
    # Check if we're being run directly with arguments or imported
    if len(sys.argv) > 1 or '--test' in sys.argv or '--time' in sys.argv:
        # New AdventSolution mode
        solution = Day2Solution()
        solution.main()
    else:
        # Legacy mode for compatibility
        print(part2("day2_input.txt"))

if __name__ == "__main__":
    main()