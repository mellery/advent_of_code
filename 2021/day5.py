#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 5: Hydrothermal Venture

Tracking lines of hydrothermal vents on a grid.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import Any, Dict, List, Tuple
from collections import defaultdict


def parse_lines_from_data(input_data: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Parse input data into list of line segments."""
    lines = input_data.strip().split('\n')
    segments = []
    
    for line in lines:
        if line.strip():
            parts = line.strip().split(' -> ')
            x1, y1 = map(int, parts[0].split(','))
            x2, y2 = map(int, parts[1].split(','))
            segments.append(((x1, y1), (x2, y2)))
    
    return segments


def mark_line_on_grid(grid: Dict[Tuple[int, int], int], start: Tuple[int, int], 
                     end: Tuple[int, int], include_diagonal: bool = False) -> None:
    """Mark a line segment on the grid."""
    x1, y1 = start
    x2, y2 = end
    
    # Horizontal line
    if x1 == x2:
        min_y, max_y = min(y1, y2), max(y1, y2)
        for y in range(min_y, max_y + 1):
            grid[(x1, y)] += 1
    
    # Vertical line
    elif y1 == y2:
        min_x, max_x = min(x1, x2), max(x1, x2)
        for x in range(min_x, max_x + 1):
            grid[(x, y1)] += 1
    
    # Diagonal line (only if include_diagonal is True)
    elif include_diagonal:
        # Calculate direction
        dx = 1 if x2 > x1 else -1
        dy = 1 if y2 > y1 else -1
        
        # Only handle 45-degree diagonals
        if abs(x2 - x1) == abs(y2 - y1):
            x, y = x1, y1
            while True:
                grid[(x, y)] += 1
                if x == x2 and y == y2:
                    break
                x += dx
                y += dy


def solve_hydrothermal_vents_from_data(input_data: str, include_diagonal: bool = False) -> int:
    """Solve the hydrothermal vents problem."""
    segments = parse_lines_from_data(input_data)
    grid = defaultdict(int)
    
    for start, end in segments:
        mark_line_on_grid(grid, start, end, include_diagonal)
    
    # Count points where at least two lines overlap
    return sum(1 for count in grid.values() if count >= 2)


class Day5Solution(AdventSolution):
    """Day 5: Hydrothermal Venture"""
    
    def __init__(self):
        super().__init__(2021, 5, "Hydrothermal Venture")
    
    def part1(self, input_data: str) -> Any:
        """
        Count overlap points considering only horizontal and vertical lines.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Number of points where at least two lines overlap
        """
        return solve_hydrothermal_vents_from_data(input_data, include_diagonal=False)
    
    def part2(self, input_data: str) -> Any:
        """
        Count overlap points considering horizontal, vertical, and diagonal lines.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Number of points where at least two lines overlap (including diagonals)
        """
        return solve_hydrothermal_vents_from_data(input_data, include_diagonal=True)




def main():
    """Main execution function."""
    solution = Day5Solution()
    solution.main()


if __name__ == "__main__":
    main()