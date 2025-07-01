#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 6: Lanternfish

Simulating exponential growth of lanternfish population.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from collections import Counter
from typing import List, Any


class Day6Solution(AdventSolution):
    """Solution for Advent of Code 2021 Day 6."""
    
    def __init__(self):
        super().__init__(2021, 6, "Lanternfish")
    
    def _get_list_of_numbers(self, input_data: str) -> List[int]:
        """Parse input data to get initial fish timer values."""
        line = input_data.strip()
        return [int(x) for x in line.split(",")]
    
    def _simulate_fish(self, initial_fish: List[int], days: int) -> int:
        """
        Efficiently simulate lanternfish population using counter approach.
        
        Instead of tracking individual fish, we track how many fish have each timer value.
        This reduces the problem from exponential to linear time complexity.
        """
        # Count fish by their timer values (0-8)
        fish_count = Counter(initial_fish)
        
        for day in range(days):
            # Fish with timer 0 spawn new fish
            spawning_fish = fish_count[0]
            
            # Shift all timer values down by 1
            new_count = Counter()
            for timer in range(1, 9):
                new_count[timer - 1] = fish_count[timer]
            
            # Fish that spawned reset to timer 6
            new_count[6] += spawning_fish
            
            # New fish start with timer 8
            new_count[8] = spawning_fish
            
            fish_count = new_count
        
        return sum(fish_count.values())
    
    def part1(self, input_data: str) -> int:
        """Part 1: Simulate for 80 days."""
        fish = self._get_list_of_numbers(input_data)
        return self._simulate_fish(fish, 80)
    
    def part2(self, input_data: str) -> int:
        """Part 2: Simulate for 256 days."""
        fish = self._get_list_of_numbers(input_data)
        return self._simulate_fish(fish, 256)



def main():
    """Main execution function."""
    solution = Day6Solution()
    solution.main()

if __name__ == "__main__":
    main()