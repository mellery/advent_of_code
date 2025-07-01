#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 9: Smoke Basin

Finding low points and basin sizes in a heightmap.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    get_lines, setup_day_args, find_input_file, validate_solution, run_solution
)
from utils.advent_base import AdventSolution
from typing import Any, List, Tuple, Set
from collections import deque


def get_grid(filename: str) -> List[List[int]]:
    """Parse grid from file into a 2D list for faster access."""
    lines = get_lines(filename)
    
    grid = []
    for line in lines:
        if line.strip():  # Skip empty lines
            grid.append([int(c) for c in line.strip()])
    
    return grid


def get_low_points(grid: List[List[int]]) -> List[Tuple[int, int]]:
    """Find all low points in the grid."""
    rows, cols = len(grid), len(grid[0])
    low_points = []
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for r in range(rows):
        for c in range(cols):
            height = grid[r][c]
            is_low = True
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if height >= grid[nr][nc]:
                        is_low = False
                        break
            
            if is_low:
                low_points.append((r, c))
    
    return low_points


def find_basin_size(grid: List[List[int]], start_r: int, start_c: int) -> int:
    """Find basin size using BFS flood fill from a low point."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = deque([(start_r, start_c)])
    visited.add((start_r, start_c))
    size = 0
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        r, c = queue.popleft()
        size += 1
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            
            # Skip if already visited
            if (nr, nc) in visited:
                continue
            
            # Skip if height is 9 (basin boundary)
            if grid[nr][nc] == 9:
                continue
            
            # Add to basin if height flows toward current point
            visited.add((nr, nc))
            queue.append((nr, nc))
    
    return size


class Day9Solution(AdventSolution):
    """Day 9: Smoke Basin"""
    
    def __init__(self):
        super().__init__(2021, 9, "Smoke Basin")
    
    def part1(self, filename: str) -> Any:
        """
        Calculate sum of risk levels for all low points.
        
        Args:
            filename: Path to the input file
            
        Returns:
            Sum of risk levels (height + 1) for all low points
        """
        grid = get_grid(filename)
        low_points = get_low_points(grid)
        
        risk_sum = 0
        for r, c in low_points:
            risk_sum += grid[r][c] + 1
        
        return risk_sum
    
    def part2(self, filename: str) -> Any:
        """
        Find product of three largest basin sizes.
        
        Args:
            filename: Path to the input file
            
        Returns:
            Product of the three largest basin sizes
        """
        grid = get_grid(filename)
        low_points = get_low_points(grid)
        
        basin_sizes = []
        for r, c in low_points:
            size = find_basin_size(grid, r, c)
            basin_sizes.append(size)
        
        # Sort and get top 3
        basin_sizes.sort(reverse=True)
        return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


# Legacy functions for backward compatibility
def part1(filename: str) -> Any:
    """Legacy function for part 1."""
    solution = Day9Solution()
    return solution.part1(filename)


def part2(filename: str) -> Any:
    """Legacy function for part 2."""
    solution = Day9Solution()
    return solution.part2(filename)


def main():
    """Main function to run the solution."""
    solution = Day9Solution()
    
    # Check if we're being called by the legacy test runner
    if len(sys.argv) > 1 and '--legacy' in sys.argv:
        # Legacy mode - use the old approach
        day = '9'
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
                            expected_part1=15, expected_part2=1134)
            print("-" * 40)
        
        # Run the actual solution
        run_solution(part1, part2, input_file, args)
    else:
        # Enhanced mode - use AdventSolution
        solution.run()


if __name__ == "__main__":
    main()