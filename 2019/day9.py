#!/usr/bin/env python3
"""
Advent of Code 2019 Day 9: Sensor Boost
https://adventofcode.com/2019/day/9

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


class Day9Solution(AdventSolution):
    """Solution for 2019 Day 9: Sensor Boost."""

    def __init__(self):
        super().__init__(2019, 9, "Sensor Boost")

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Run BOOST program in test mode.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            BOOST keycode output
        """
        program = input_data.strip()
        
        machine = Intcode(program)
        machine.add_input(1)  # Test mode
        machine.start()
        machine.join()  # Wait for completion
        
        # Should output only one value (the BOOST keycode)
        if len(machine.outputs) == 1:
            return machine.outputs[0]
        else:
            # If there are multiple outputs, the first ones should be 0 (no malfunctioning opcodes)
            # and the last one should be the keycode
            return machine.outputs[-1]

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Run BOOST program in sensor boost mode.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Coordinates of the distress signal
        """
        program = input_data.strip()
        
        machine = Intcode(program)
        machine.add_input(2)  # Sensor boost mode
        machine.start()
        machine.join()  # Wait for completion
        
        return machine.outputs[0]

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test case 1: Program that outputs a copy of itself
        test1 = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
        machine1 = Intcode(test1)
        machine1.start()
        machine1.join()
        
        # Should output the program itself
        expected_output = [int(x) for x in test1.split(',')]
        if machine1.outputs != expected_output:
            print(f"Test 1 failed: program should output copy of itself")
            return False
        
        # Test case 2: Program that outputs a 16-digit number
        test2 = "1102,34915192,34915192,7,4,7,99,0"
        machine2 = Intcode(test2)
        machine2.start()
        machine2.join()
        
        if len(str(machine2.outputs[0])) != 16:
            print(f"Test 2 failed: should output 16-digit number, got {machine2.outputs[0]}")
            return False
        
        # Test case 3: Program that outputs the large number in the middle
        test3 = "104,1125899906842624,99"
        machine3 = Intcode(test3)
        machine3.start()
        machine3.join()
        
        if machine3.outputs[0] != 1125899906842624:
            print(f"Test 3 failed: expected 1125899906842624, got {machine3.outputs[0]}")
            return False
        
        print("✅ All Day 9 validation tests passed!")
        return True


def main():
    """Main execution function."""
    solution = Day9Solution()
    solution.main()


if __name__ == "__main__":
    main()