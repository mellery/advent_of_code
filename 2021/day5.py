#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 5: Hydrothermal Venture

Tracking lines of hydrothermal vents on a grid.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    get_lines, setup_day_args, find_input_file, validate_solution, run_solution
)
from utils.advent_base import AdventSolution
from typing import Any, Dict, List, Tuple
from collections import defaultdict


def parse_lines(filename: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Parse input file into list of line segments."""
    lines = get_lines(filename)
    segments = []
    
    for line in lines:
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


def solve_hydrothermal_vents(filename: str, include_diagonal: bool = False) -> int:
    """Solve the hydrothermal vents problem."""
    segments = parse_lines(filename)
    grid = defaultdict(int)
    
    for start, end in segments:
        mark_line_on_grid(grid, start, end, include_diagonal)
    
    # Count points where at least two lines overlap
    return sum(1 for count in grid.values() if count >= 2)


class Day5Solution(AdventSolution):
    """Day 5: Hydrothermal Venture"""
    
    def __init__(self):
        super().__init__(2021, 5, "Hydrothermal Venture")
    
    def part1(self, filename: str) -> Any:
        """
        Count overlap points considering only horizontal and vertical lines.
        
        Args:
            filename: Path to the input file
            
        Returns:
            Number of points where at least two lines overlap
        """
        return solve_hydrothermal_vents(filename, include_diagonal=False)
    
    def part2(self, filename: str) -> Any:
        """
        Count overlap points considering horizontal, vertical, and diagonal lines.
        
        Args:
            filename: Path to the input file
            
        Returns:
            Number of points where at least two lines overlap (including diagonals)
        """
        return solve_hydrothermal_vents(filename, include_diagonal=True)


# Legacy functions for backward compatibility
def part1(filename: str) -> Any:
    """Legacy function for part 1."""
    solution = Day5Solution()
    return solution.part1(filename)


def part2(filename: str) -> Any:
    """Legacy function for part 2."""
    solution = Day5Solution()
    return solution.part2(filename)


def main():
    """Main function to run the solution."""
    solution = Day5Solution()
    
    # Check if we're being called by the legacy test runner
    if len(sys.argv) > 1 and '--legacy' in sys.argv:
        # Legacy mode - use the old approach
        day = '5'
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
                            expected_part1=5, expected_part2=12)
            print("-" * 40)
        
        # Run the actual solution
        run_solution(part1, part2, input_file, args)
    else:
        # Enhanced mode - use AdventSolution
        solution.run()


if __name__ == "__main__":
    main()