#!/usr/bin/env python3
"""
Advent of Code 2019 Day 2: 1202 Program Alarm
https://adventofcode.com/2019/day/2

Enhanced solution using AdventSolution base class.
Migrated from legacy implementation.
"""

import sys
from pathlib import Path
from typing import Any, List, Dict, Optional, Tuple

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser

# Import the Intcode computer - now optimized by default
from intcode import IntcodeOptimized, run_intcode_simple


class Day2Solution(AdventSolution):
    """Solution for 2019 Day 2: 1202 Program Alarm."""

    def __init__(self):
        super().__init__(2019, 2, "1202 Program Alarm")

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Run the program with noun=12, verb=2.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Value at position 0 after program halts
        """
        program = input_data.strip()
        
        # Use optimized function for simple execution
        return run_intcode_simple(program, noun=12, verb=2)

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Find noun and verb that produce output 19690720.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            100 * noun + verb
        """
        program = input_data.strip()
        target = 19690720
        
        # Optimized brute force using non-threaded execution
        for noun in range(100):
            for verb in range(100):
                result = run_intcode_simple(program, noun=noun, verb=verb)
                if result == target:
                    return 100 * noun + verb
        
        return -1  # Not found

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test with simple program that we know the result
        test_program = "1,9,10,3,2,3,11,0,99,30,40,50"
        
        # This program should:
        # - Add 30+40=70, store at position 3
        # - Multiply 70*50=3500, store at position 0
        # - Halt
        machine = IntcodeOptimized(test_program)
        result = machine.execute()
        
        if result != 3500:
            print(f"Test failed: expected 3500, got {result}")
            return False
        
        print("✅ Basic Intcode validation passed!")
        return True


def main():
    """Main execution function."""
    solution = Day2Solution()
    solution.main()


if __name__ == "__main__":
    main()