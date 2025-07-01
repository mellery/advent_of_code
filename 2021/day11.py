#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 11: Dumbo Octopus

Simulates the flashing behavior of octopuses in a grid.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import Any, Dict, Tuple, List, Set


def simulate_octopus_step(grid: Dict[Tuple[int, int], int], rows: int, cols: int) -> int:
    """Simulate one step of octopus flashing and return flash count."""
    flash_count = 0
    
    # Increment all by 1
    for x in range(rows):
        for y in range(cols):
            grid[(x, y)] += 1
    
    # Track which octopuses have flashed this step
    flashed = set()
    
    while True:
        new_flashes = []
        
        # Find octopuses ready to flash
        for x in range(rows):
            for y in range(cols):
                if grid[(x, y)] > 9 and (x, y) not in flashed:
                    new_flashes.append((x, y))
                    flashed.add((x, y))
                    flash_count += 1
        
        if not new_flashes:
            break
            
        # Process flashes
        for x, y in new_flashes:
            # Increase energy of all adjacent octopuses
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols:
                        grid[(nx, ny)] += 1
    
    # Reset flashed octopuses to 0
    for x, y in flashed:
        grid[(x, y)] = 0
    
    return flash_count


class Day11Solution(AdventSolution):
    """Day 11: Dumbo Octopus"""
    
    def __init__(self):
        super().__init__(2021, 11, "Dumbo Octopus")
    
    def part1(self, input_data: str) -> Any:
        """
        Count total flashes after 100 steps.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Total number of flashes after 100 steps
        """
        lines = input_data.strip().split('\n')
        grid_data = [[int(c) for c in line.strip()] for line in lines if line.strip()]
        grid = {}
        rows = len(grid_data)
        cols = len(grid_data[0])
        
        # Convert to coordinate-based grid
        for x in range(rows):
            for y in range(cols):
                grid[(x, y)] = grid_data[x][y]
        
        total_flashes = 0
        for step in range(100):
            total_flashes += simulate_octopus_step(grid, rows, cols)
        
        return total_flashes
    
    def part2(self, input_data: str) -> Any:
        """
        Find the step when all octopuses flash simultaneously.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            The step number when all octopuses flash together
        """
        lines = input_data.strip().split('\n')
        grid_data = [[int(c) for c in line.strip()] for line in lines if line.strip()]
        grid = {}
        rows = len(grid_data)
        cols = len(grid_data[0])
        total_octopuses = rows * cols
        
        # Convert to coordinate-based grid
        for x in range(rows):
            for y in range(cols):
                grid[(x, y)] = grid_data[x][y]
        
        step = 0
        while True:
            step += 1
            flashes = simulate_octopus_step(grid, rows, cols)
            if flashes == total_octopuses:
                return step


def main():
    """Main execution function."""
    solution = Day11Solution()
    solution.main()


if __name__ == "__main__":
    main()