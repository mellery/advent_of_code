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

# Import the Intcode computer
from intcode import Intcode


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
        
        # Replace positions 1 and 2 as specified
        commands = program.split(',')
        commands[1] = "12"  # noun
        commands[2] = "2"   # verb
        modified_program = ",".join(commands)
        
        machine = Intcode(modified_program)
        machine.start()
        machine.join()  # Wait for completion
        
        return machine.commands[0]

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
        
        for noun in range(100):
            for verb in range(100):
                # Create modified program
                commands = program.split(',')
                commands[1] = str(noun)
                commands[2] = str(verb)
                modified_program = ",".join(commands)
                
                machine = Intcode(modified_program)
                machine.start()
                machine.join()  # Wait for completion
                
                if machine.commands[0] == target:
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
        machine = Intcode(test_program)
        machine.start()
        machine.join()
        
        if machine.commands[0] != 3500:
            print(f"Test failed: expected 3500, got {machine.commands[0]}")
            return False
        
        print("✅ Basic Intcode validation passed!")
        return True


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day2Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day2Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main execution function."""
    solution = Day2Solution()
    solution.main()


if __name__ == "__main__":
    main()