#!/usr/bin/env python3
"""
Advent of Code 2019 Day 10: Monitoring Station
https://adventofcode.com/2019/day/10

Enhanced solution using AdventSolution base class.
Migrated from legacy implementation.
"""

import sys
from pathlib import Path
from typing import Any, List, Dict, Optional, Tuple

from utils.algorithms import grid

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser
from collections import defaultdict, deque, Counter
import math

class Day10Solution(AdventSolution):
    """Solution for 2019 Day 10: Monitoring Station."""

    def __init__(self):
        super().__init__(2019, 10, "Monitoring Station")

    def part1(self, input_data: str) -> Any:
        """
        Solve part 1 of the problem.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Solution for part 1
        """
        parser = InputParser(input_data)
        asteroids = []
        for y, row in enumerate(parser.as_grid()):
            for x, cell in enumerate(row):
                if cell == '#':
                    asteroids.append((x, y))

        best_count = 0
        best_pos = None

        for ax, ay in asteroids:
            # Group asteroids by direction vector
            directions = set()
            
            for bx, by in asteroids:
                if (ax, ay) != (bx, by):
                    dx, dy = bx - ax, by - ay
                    direction = self.get_direction_vector(dx, dy)
                    directions.add(direction)
            
            visible_count = len(directions)
            if visible_count > best_count:
                best_count = visible_count
                best_pos = (ax, ay)

        return best_count

    def part2(self, input_data: str) -> Any:
        """
        Solve part 2 of the problem.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Solution for part 2
        """
        parser = InputParser(input_data)
        asteroids = []
        for y, row in enumerate(parser.as_grid()):
            for x, cell in enumerate(row):
                if cell == '#':
                    asteroids.append((x, y))

        best_count = 0
        best_pos = None

        for ax, ay in asteroids:
            # Group asteroids by direction vector
            directions = set()
            
            for bx, by in asteroids:
                if (ax, ay) != (bx, by):
                    dx, dy = bx - ax, by - ay
                    direction = self.get_direction_vector(dx, dy)
                    directions.add(direction)
            
            visible_count = len(directions)
            if visible_count > best_count:
                best_count = visible_count
                best_pos = (ax, ay)

        station_x, station_y = best_pos
    
        # Group asteroids by angle and sort by distance
        angle_groups = defaultdict(list)
        
        for ax, ay in asteroids:
            if (ax, ay) != best_pos:
                dx, dy = ax - station_x, ay - station_y
                angle = self.get_angle(dx, dy)
                distance = dx * dx + dy * dy  # No need for sqrt, just for comparison
                angle_groups[angle].append((distance, ax, ay))
        
        # Sort each angle group by distance (closest first)
        for angle in angle_groups:
            angle_groups[angle].sort()
        
        # Get sorted angles (clockwise from north)
        sorted_angles = sorted(angle_groups.keys())
        
        # Simulate laser rotation
        destroyed = []
        angle_idx = 0
        
        while angle_groups:
            # Get current angle
            if angle_idx >= len(sorted_angles):
                angle_idx = 0
                # Remove empty angles
                sorted_angles = [a for a in sorted_angles if angle_groups[a]]
                if not sorted_angles:
                    break
            
            current_angle = sorted_angles[angle_idx]
            
            if angle_groups[current_angle]:
                # Destroy closest asteroid at this angle
                _, x, y = angle_groups[current_angle].pop(0)
                destroyed.append((x, y))
            
            angle_idx += 1
        
        # Get 200th destroyed asteroid
        if len(destroyed) >= 200:
            x200, y200 = destroyed[199]  # 0-indexed
            part2_answer = x200 * 100 + y200
        else:
            part2_answer = 0

        return part2_answer
        

    def gcd(self, a: int, b: int) -> int:
        """Calculate greatest common divisor."""
        while b:
            a, b = b, a % b
        return a



    def get_direction_vector(self, dx: int, dy: int) -> tuple[int, int]:
        """Get normalized direction vector using GCD."""
        if dx == 0 and dy == 0:
            return (0, 0)
        g = self.gcd(abs(dx), abs(dy))
        return (dx // g, dy // g)



    def get_angle(self, dx: int, dy: int) -> float:
        """Get angle in degrees, with 0° pointing up and increasing clockwise."""
        angle = math.atan2(dx, -dy) * 180 / math.pi
        return (angle + 360) % 360

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
        expected_part1 = 210
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        expected_part2 = 802
        
        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False
        
        print("✅ All Day 10 validation tests passed!")
        return True

def main():
    """Main execution function."""
    solution = Day10Solution()
    solution.main()


if __name__ == "__main__":
    main()