#!/usr/bin/env python3
"""
Advent of Code 2020 Day 3: Toboggan Trajectory
https://adventofcode.com/2020/day/3

Tree counting on repeating slope patterns with different trajectories.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, List, Tuple, Dict
import math

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class SlopeMap:
    """Represents a toboggan slope with repeating horizontal pattern."""
    
    def __init__(self, grid_lines: List[str]):
        """
        Initialize slope map from grid lines.
        
        Args:
            grid_lines: List of strings representing the slope pattern
        """
        self.grid_lines = [line.strip() for line in grid_lines if line.strip()]
        self.height = len(self.grid_lines)
        self.width = len(self.grid_lines[0]) if self.grid_lines else 0
        
        if not all(len(line) == self.width for line in self.grid_lines):
            raise ValueError("All grid lines must have the same width")
    
    def is_tree(self, x: int, y: int) -> bool:
        """
        Check if there's a tree at the given coordinates.
        
        The horizontal pattern repeats infinitely, so x coordinate wraps around.
        
        Args:
            x: Horizontal position (wraps around)
            y: Vertical position
            
        Returns:
            True if there's a tree at the position
        """
        if y < 0 or y >= self.height:
            return False
        
        # Wrap x coordinate using modulo
        wrapped_x = x % self.width
        return self.grid_lines[y][wrapped_x] == '#'
    
    def count_trees_on_slope(self, right: int, down: int) -> int:
        """
        Count trees encountered following a specific slope trajectory.
        
        Args:
            right: Steps to move right each iteration
            down: Steps to move down each iteration
            
        Returns:
            Number of trees encountered
        """
        trees = 0
        x, y = 0, 0
        
        while y < self.height:
            if self.is_tree(x, y):
                trees += 1
            
            x += right
            y += down
        
        return trees
    
    def get_tree_positions(self, right: int, down: int) -> List[Tuple[int, int]]:
        """
        Get all positions where trees are encountered on a slope.
        
        Args:
            right: Steps to move right each iteration
            down: Steps to move down each iteration
            
        Returns:
            List of (x, y) positions where trees are found
        """
        tree_positions = []
        x, y = 0, 0
        
        while y < self.height:
            if self.is_tree(x, y):
                tree_positions.append((x, y))
            
            x += right
            y += down
        
        return tree_positions
    
    def visualize_path(self, right: int, down: int, max_width: int = 50) -> str:
        """
        Create a visual representation of the path through the slope.
        
        Args:
            right: Steps to move right each iteration
            down: Steps to move down each iteration
            max_width: Maximum width to show before truncating
            
        Returns:
            String representation of the path
        """
        if not self.grid_lines:
            return "Empty grid"
        
        # Create a copy of the grid for visualization
        visual_grid = []
        for line in self.grid_lines:
            # Repeat pattern enough times to show the full path
            repeated_line = line * (max_width // self.width + 2)
            visual_grid.append(list(repeated_line[:max_width]))
        
        # Mark the path
        x, y = 0, 0
        path_positions = []
        
        while y < self.height:
            if x < max_width:
                path_positions.append((x, y))
            x += right
            y += down
        
        # Mark positions on the grid
        for x, y in path_positions:
            if x < max_width and y < len(visual_grid):
                if visual_grid[y][x] == '#':
                    visual_grid[y][x] = 'X'  # Tree hit
                else:
                    visual_grid[y][x] = 'O'  # Open space visited
        
        return '\n'.join(''.join(row) for row in visual_grid)


class Day3Solution(AdventSolution):
    """Solution for 2020 Day 3: Toboggan Trajectory."""

    def __init__(self):
        super().__init__(2020, 3, "Toboggan Trajectory")

    def parse_slope_map(self, input_data: str) -> SlopeMap:
        """
        Parse slope map from input data.
        
        Args:
            input_data: Raw input data containing the slope pattern
            
        Returns:
            SlopeMap object
        """
        lines = input_data.strip().split('\n')
        return SlopeMap(lines)

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Count trees on slope (right 3, down 1).
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of trees encountered on the slope
        """
        slope_map = self.parse_slope_map(input_data)
        return slope_map.count_trees_on_slope(3, 1)

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Multiply tree counts for multiple slopes.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Product of tree counts for all specified slopes
        """
        slope_map = self.parse_slope_map(input_data)
        
        # Test these slopes as specified in the problem
        slopes = [
            (1, 1),  # Right 1, down 1
            (3, 1),  # Right 3, down 1
            (5, 1),  # Right 5, down 1
            (7, 1),  # Right 7, down 1
            (1, 2),  # Right 1, down 2
        ]
        
        product = 1
        for right, down in slopes:
            trees = slope_map.count_trees_on_slope(right, down)
            product *= trees
        
        return product

    def analyze_slopes(self, input_data: str) -> str:
        """
        Analyze tree patterns on different slopes.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis summary as formatted string
        """
        slope_map = self.parse_slope_map(input_data)
        
        analysis = []
        analysis.append("=== Slope Analysis ===")
        analysis.append(f"Map dimensions: {slope_map.width} x {slope_map.height}")
        
        # Count total trees in original pattern
        total_trees = sum(line.count('#') for line in slope_map.grid_lines)
        total_spaces = slope_map.width * slope_map.height - total_trees
        tree_density = total_trees / (slope_map.width * slope_map.height) * 100
        
        analysis.append(f"Tree density: {total_trees}/{slope_map.width * slope_map.height} ({tree_density:.1f}%)")
        
        # Analyze various slopes
        test_slopes = [
            (1, 1), (3, 1), (5, 1), (7, 1), (1, 2),
            (2, 1), (4, 1), (6, 1), (1, 3)
        ]
        
        analysis.append("Trees encountered on different slopes:")
        slope_results = []
        
        for right, down in test_slopes:
            trees = slope_map.count_trees_on_slope(right, down)
            # Calculate steps taken
            steps = (slope_map.height - 1) // down + 1
            slope_results.append((right, down, trees, steps))
            analysis.append(f"  Right {right}, Down {down}: {trees} trees in {steps} steps")
        
        # Find most/least dangerous slopes
        slope_results.sort(key=lambda x: x[2])  # Sort by tree count
        safest = slope_results[0]
        most_dangerous = slope_results[-1]
        
        analysis.append(f"Safest slope: Right {safest[0]}, Down {safest[1]} ({safest[2]} trees)")
        analysis.append(f"Most dangerous: Right {most_dangerous[0]}, Down {most_dangerous[1]} ({most_dangerous[2]} trees)")
        
        return "\n".join(analysis)

    def visualize_slope(self, input_data: str, right: int = 3, down: int = 1) -> str:
        """
        Create a visual representation of a path through the slope.
        
        Args:
            input_data: Raw input data
            right: Steps to move right
            down: Steps to move down
            
        Returns:
            Visual representation as string
        """
        slope_map = self.parse_slope_map(input_data)
        trees = slope_map.count_trees_on_slope(right, down)
        
        result = [f"Path visualization for slope (right {right}, down {down}):"]
        result.append(f"Trees encountered: {trees}")
        result.append("Legend: # = tree, . = open, O = path (open), X = path (tree)")
        result.append("")
        result.append(slope_map.visualize_path(right, down))
        
        return "\n".join(result)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test with example from problem description
        test_input = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""
        
        slope_map = self.parse_slope_map(test_input)
        
        # Test basic map properties
        if slope_map.height != 11:
            print(f"Height test failed: expected 11, got {slope_map.height}")
            return False
        
        if slope_map.width != 11:
            print(f"Width test failed: expected 11, got {slope_map.width}")
            return False
        
        # Test part 1: slope (3, 1) should encounter 7 trees
        part1_result = slope_map.count_trees_on_slope(3, 1)
        if part1_result != 7:
            print(f"Part 1 test failed: expected 7, got {part1_result}")
            return False
        
        # Test individual slopes for part 2
        expected_slopes = [
            ((1, 1), 2),
            ((3, 1), 7),
            ((5, 1), 3),
            ((7, 1), 4),
            ((1, 2), 2),
        ]
        
        for (right, down), expected_trees in expected_slopes:
            trees = slope_map.count_trees_on_slope(right, down)
            if trees != expected_trees:
                print(f"Slope ({right}, {down}) test failed: expected {expected_trees}, got {trees}")
                return False
        
        # Test part 2: product should be 336
        part2_result = self.part2(test_input)
        if part2_result != 336:
            print(f"Part 2 test failed: expected 336, got {part2_result}")
            return False
        
        print("✅ All Day 3 validation tests passed!")
        return True


def main():
    """Main execution function."""
    solution = Day3Solution()
    solution.main()


if __name__ == "__main__":
    main()