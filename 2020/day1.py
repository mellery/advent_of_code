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

# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day1Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day1Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)

def main():
    """Main execution function."""
    solution = Day1Solution()
    solution.main()


if __name__ == "__main__":
    main()