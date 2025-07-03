#!/usr/bin/env python3
"""
Advent of Code 2023 Day 1: Migrated Solution
https://adventofcode.com/2023/day/1

Enhanced solution using AdventSolution base class.
Migrated from legacy implementation.
"""

import sys
from pathlib import Path
from typing import Any, List, Dict, Optional, Tuple

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser

class Day1Solution(AdventSolution):
    """Solution for 2023 Day 1: Trebuchet?!"""

    def __init__(self):
        super().__init__(2023, 1, "Trebuchet?!")
        self.digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    def get_first_digit(self, line: str) -> str:
        """Get the first digit from a line."""
        for c in line:
            if c.isdigit():
                return c
        return ''

    def replace_first_word(self, line: str, rev: bool = False) -> str:
        """Replace first word digit with numeric digit."""
        for x in range(len(line)):
            if line[x].isdigit():
                if rev:
                    line = line[::-1]
                return line
            temp = line[x:]
            for i, d in enumerate(self.digits):
                w = d
                if rev:
                    w = d[::-1]
                if temp.startswith(w):
                    line = line.replace(w, str(i+1))
                    if rev:
                        line = line[::-1]
                    return line
        if rev:
            line = line[::-1]
        return line

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Find first and last digit in each line.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Sum of all calibration values
        """
        parser = InputParser(input_data)
        lines = parser.as_lines()
        
        total = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue
            a = self.get_first_digit(line)
            b = self.get_first_digit(line[::-1])
            if a and b:
                total += int(a + b)
        
        return total

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Handle word digits (one, two, etc.).
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Sum of all calibration values including word digits
        """
        parser = InputParser(input_data)
        lines = parser.as_lines()
        
        total = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Process line for first digit (including words)
            processed_line = self.replace_first_word(line)
            a = self.get_first_digit(processed_line)
            
            # Process reversed line for last digit (including words)
            processed_rev = self.replace_first_word(line[::-1], rev=True)
            b = self.get_first_digit(processed_rev[::-1])
            
            if a and b:
                total += int(a + b)
        
        return total


def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """1000
        2000
        3000

        4000

        5000
        6000

        7000
        8000
        9000

        10000"""
        expected_part1 = 24000
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        expected_part2 = 45000
        
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