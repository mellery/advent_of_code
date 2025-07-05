#!/usr/bin/env python3
"""
Advent of Code 2020 Day 1: Migrated Solution
https://adventofcode.com/2020/day/1

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
    """Solution for 2020 Day 1: Migrated Solution."""

    def __init__(self):
        super().__init__(2020, 1, "Migrated Solution")

    def part1(self, input_data: str) -> Any:
        """
        Solve part 1 of the problem.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Solution for part 1
        """
        parser = InputParser(input_data)

        lines = parser.as_lines()
        for l1 in lines:
            for l2 in lines:
                a = int(l1.strip())
                b = int(l2.strip())
                if a+b == 2020 and a != b:
                    return a*b

        return 0

    def part2(self, input_data: str) -> Any:
        """
        Solve part 2 of the problem.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Solution for part 2
        """
        parser = InputParser(input_data)

        lines = parser.as_lines()
        for l1 in lines:
            for l2 in lines:
                for l3 in lines:  
                    a = int(l1.strip())
                    b = int(l2.strip())
                    c = int(l3.strip())
                    if a+b+c == 2020 and a != b != c:
                        return a*b*c
                        #print(f"{a} + {b} + {c} = {a+b+c} {a*b*c}")

        return 0

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """1721
979
366
299
675
1456"""
        expected_part1 = 514579
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        expected_part2 = 241861950
        
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