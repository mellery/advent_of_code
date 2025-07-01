#!/usr/bin/env python3
"""
Advent of Code 2022 Day 1: Calorie Counting
https://adventofcode.com/2022/day/1

Enhanced solution using AdventSolution base class.
The jungle must be too overgrown and difficult to navigate in vehicles or access from the air; 
the Elves' expedition traditionally goes on foot. As your boats approach land, the Elves begin 
taking inventory of their supplies. One important consideration is food - in particular, the 
number of Calories each Elf is carrying (your puzzle input).
"""

import sys
from pathlib import Path
from typing import Any, List, Dict, Optional, Tuple

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser

class Day1Solution(AdventSolution):
    """Solution for 2022 Day 1: Calorie Counting."""

    def __init__(self):
        super().__init__(2022, 1, "Calorie Counting")

    def part1(self, input_data: str) -> Any:
        """
        Solve part 1 of the problem.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Solution for part 1
        """
        parser = InputParser(input_data)

        data = parser.as_lines()
        max_calories = 0
        current_calories = 0
        for c in data:
            if c == "":
                # End of current elf's calories, store the total
                if current_calories > max_calories:
                    max_calories = current_calories
                current_calories = 0
            else:
                current_calories += int(c)
        
        return max_calories

    def part2(self, input_data: str) -> Any:
        """
        Solve part 2 of the problem.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Solution for part 2
        """
        parser = InputParser(input_data)
        data = parser.as_lines()
        elf_calories = []
        current_calories = 0
        
        for c in data:
            if c == "":
                # End of current elf's calories, store the total
                elf_calories.append(current_calories)
                current_calories = 0
            else:
                current_calories += int(c)
        
        # Add last elf's calories if not already added
        if current_calories > 0:
            elf_calories.append(current_calories)

        # Sort and get the top three elves' calories
        elf_calories.sort(reverse=True)
        return sum(elf_calories[:3])



def main():
    """Main execution function."""
    solution = Day1Solution()
    solution.main()


if __name__ == "__main__":
    main()