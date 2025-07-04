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
    
    def part1(self, input_data: str) -> Any:
        """
        Calculate sum of risk levels for all low points.
        
        Args:
            input_data: Raw input data containing the height map
            
        Returns:
            Sum of risk levels (height + 1) for all low points
        """
        lines = input_data.strip().split('\n')
        grid = [[int(char) for char in line] for line in lines]
        
        low_points = get_low_points(grid)
        
        risk_sum = 0
        for r, c in low_points:
            risk_sum += grid[r][c] + 1
        
        return risk_sum
    
    def part2(self, input_data: str) -> Any:
        """
        Find product of three largest basin sizes.
        
        Args:
            input_data: Raw input data containing the height map
            
        Returns:
            Product of the three largest basin sizes
        """
        lines = input_data.strip().split('\n')
        grid = [[int(char) for char in line] for line in lines]
        
        low_points = get_low_points(grid)
        
        basin_sizes = []
        for r, c in low_points:
            size = find_basin_size(grid, r, c)
            basin_sizes.append(size)
        
        # Sort and get top 3
        basin_sizes.sort(reverse=True)
        return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """2199943210
3987894921
9856789892
8767896789
9899965678"""
        expected_part1 = 15
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        expected_part2 = 1134
        
        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False
        
        print("✅ All Day 1 validation tests passed!")
        return True
    
def main():
    """Main execution function."""
    solution = Day9Solution()
    solution.main()


if __name__ == "__main__":
    main()