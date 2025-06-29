#!/usr/bin/env python3
"""
Advent of Code 2019 Day 1: The Tyranny of the Rocket Equation
https://adventofcode.com/2019/day/1

Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any
from math import floor

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class Day1Solution(AdventSolution):
    """Solution for 2019 Day 1: The Tyranny of the Rocket Equation."""

    def __init__(self):
        super().__init__(2019, 1, "The Tyranny of the Rocket Equation")

    def fuel_required(self, mass: int) -> int:
        """Calculate fuel required for a given mass."""
        return floor(mass / 3) - 2

    def fuel_required_recursive(self, mass: int) -> int:
        """Calculate fuel required including fuel for the fuel itself."""
        fuel = self.fuel_required(mass)
        if fuel <= 0:
            return 0
        
        total = fuel
        while fuel > 0:
            fuel = self.fuel_required(fuel)
            if fuel > 0:
                total += fuel
        
        return total

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Calculate fuel for all modules.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Total fuel required for all modules
        """
        parser = InputParser(input_data)
        masses = parser.as_integers()
        
        total_fuel = 0
        for mass in masses:
            total_fuel += self.fuel_required(mass)
        
        return total_fuel

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Calculate fuel including fuel for the fuel.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Total fuel including fuel for fuel itself
        """
        parser = InputParser(input_data)
        masses = parser.as_integers()
        
        total_fuel = 0
        for mass in masses:
            total_fuel += self.fuel_required_recursive(mass)
        
        return total_fuel

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test cases from problem description
        test_cases_part1 = [
            (12, 2),     # For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
            (14, 2),     # For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
            (1969, 654), # For a mass of 1969, the fuel required is 654.
            (100756, 33583) # For a mass of 100756, the fuel required is 33583.
        ]
        
        for mass, expected in test_cases_part1:
            result = self.fuel_required(mass)
            if result != expected:
                print(f"Part 1 test failed for mass {mass}: expected {expected}, got {result}")
                return False
        
        # Test cases for part 2
        test_cases_part2 = [
            (14, 2),     # A module of mass 14 requires 2 fuel. This fuel requires no further fuel
            (1969, 966), # A module of mass 1969 requires 654 fuel. That fuel requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel, which requires 21 more fuel, which requires 5 more fuel, which requires no further fuel. So, the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
            (100756, 50346) # The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
        ]
        
        for mass, expected in test_cases_part2:
            result = self.fuel_required_recursive(mass)
            if result != expected:
                print(f"Part 2 test failed for mass {mass}: expected {expected}, got {result}")
                return False
        
        print("✅ All Day 1 validation tests passed!")
        return True


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