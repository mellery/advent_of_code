#!/usr/bin/env python3
"""
Advent of Code 2019 Day 5: Sunny with a Chance of Asteroids
https://adventofcode.com/2019/day/5

Intcode computer with extended instruction set including input/output operations.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser

# Import the Intcode computer
from intcode import Intcode


class Day5Solution(AdventSolution):
    """Solution for 2019 Day 5: Sunny with a Chance of Asteroids."""

    def __init__(self):
        super().__init__(2019, 5, "Sunny with a Chance of Asteroids")

    def run_intcode_with_input(self, program: str, input_value: int) -> int:
        """
        Run the Intcode program with a single input value and return the diagnostic code.
        
        Args:
            program: The Intcode program as a string
            input_value: The input value to provide to the program
            
        Returns:
            The final output (diagnostic code) from the program
        """
        machine = Intcode(program)
        machine.add_input(input_value)
        outputs = machine.run()
        return outputs[-1]

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Run the diagnostic program with system ID 1.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Diagnostic code for air conditioner unit
        """
        program = input_data.strip()
        return self.run_intcode_with_input(program, 1)

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Run the diagnostic program with system ID 5.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Diagnostic code for thermal radiator controller
        """
        program = input_data.strip()
        return self.run_intcode_with_input(program, 5)


def main():
    """Main execution function."""
    solution = Day5Solution()
    solution.main()


if __name__ == "__main__":
    main()