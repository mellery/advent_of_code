#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 11: Dumbo Octopus

Simulates the flashing behavior of octopuses in a grid.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    get_grid, setup_day_args, find_input_file, validate_solution, run_solution
)
from typing import Any, Dict, Tuple, List


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


def part1(filename: str) -> Any:
    """
    Count total flashes after 100 steps.
    
    Args:
        filename: Path to the input file
        
    Returns:
        Total number of flashes after 100 steps
    """
    grid_data = get_grid(filename, lambda x: int(x))
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


def part2(filename: str) -> Any:
    """
    Find the step when all octopuses flash simultaneously.
    
    Args:
        filename: Path to the input file
        
    Returns:
        The step number when all octopuses flash together
    """
    grid_data = get_grid(filename, lambda x: int(x))
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
    """Main function to run the solution."""
    day = '11'
    args = setup_day_args(day)
    
    # Determine input file
    if args.use_test:
        input_file = args.test
    else:
        input_file = find_input_file(day) or args.input
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        return
    
    print(f"Advent of Code 2021 - Day {day}")
    print(f"Using input file: {input_file}")
    print("-" * 40)
    
    # Run validation if test file exists
    test_file = args.test
    if os.path.exists(test_file) and not args.use_test:
        print("Running validation tests...")
        validate_solution(part1, part2, test_file, 
                        expected_part1=1656, expected_part2=195)
        print("-" * 40)
    
    # Run the actual solution
    run_solution(part1, part2, input_file, args)


if __name__ == "__main__":
    main()