#!/usr/bin/env python3
"""
Advent of Code 2019 - Day 3: Crossed Wires

The gravity assist was successful, and you're well on your way to the Venus refuelling station.
During the trip, you need to fix a fuel management system by tracing wire paths and finding
their intersections.

Key Concepts:
- Grid-based path tracing
- Line segment intersection detection
- Manhattan distance calculation
- Path length optimization
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Tuple, Set, Dict, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True)
class Point:
    """Represents a 2D point with x,y coordinates."""
    x: int
    y: int
    
    def manhattan_distance(self, other: 'Point') -> int:
        """Calculate Manhattan distance to another point."""
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def __add__(self, other: 'Point') -> 'Point':
        """Add two points together."""
        return Point(self.x + other.x, self.y + other.y)


@dataclass
class WireSegment:
    """Represents a line segment of a wire."""
    start: Point
    end: Point
    direction: str
    distance: int
    
    def get_all_points(self) -> List[Point]:
        """Get all points along this segment."""
        points = []
        current = self.start
        
        dx = 1 if self.end.x > self.start.x else (-1 if self.end.x < self.start.x else 0)
        dy = 1 if self.end.y > self.start.y else (-1 if self.end.y < self.start.y else 0)
        
        for _ in range(self.distance):
            current = Point(current.x + dx, current.y + dy)
            points.append(current)
        
        return points
    
    def intersects_with(self, other: 'WireSegment') -> Optional[Point]:
        """Check if this segment intersects with another segment."""
        # Check if segments are parallel
        if self._is_horizontal() == other._is_horizontal():
            return None
        
        if self._is_horizontal():
            horizontal, vertical = self, other
        else:
            horizontal, vertical = other, self
        
        # Check if intersection is within both segments
        h_min_x, h_max_x = min(horizontal.start.x, horizontal.end.x), max(horizontal.start.x, horizontal.end.x)
        v_min_y, v_max_y = min(vertical.start.y, vertical.end.y), max(vertical.start.y, vertical.end.y)
        
        intersection_x = vertical.start.x
        intersection_y = horizontal.start.y
        
        if (h_min_x <= intersection_x <= h_max_x and 
            v_min_y <= intersection_y <= v_max_y):
            return Point(intersection_x, intersection_y)
        
        return None
    
    def _is_horizontal(self) -> bool:
        """Check if this segment is horizontal."""
        return self.start.y == self.end.y


class Wire:
    """Represents a complete wire with multiple segments."""
    
    def __init__(self, path_string: str):
        """
        Initialize wire from path string.
        
        Args:
            path_string: Comma-separated directions like "R8,U5,L5,D3"
        """
        self.path_string = path_string
        self.segments: List[WireSegment] = []
        self.points_with_steps: Dict[Point, int] = {}
        self._parse_path()
    
    def _parse_path(self) -> None:
        """Parse the path string into segments and track all points."""
        directions = {
            'R': Point(1, 0),
            'L': Point(-1, 0),
            'U': Point(0, 1),
            'D': Point(0, -1)
        }
        
        current_pos = Point(0, 0)
        total_steps = 0
        
        for instruction in self.path_string.split(','):
            direction = instruction[0]
            distance = int(instruction[1:])
            
            start_pos = current_pos
            delta = directions[direction]
            end_pos = Point(
                current_pos.x + delta.x * distance,
                current_pos.y + delta.y * distance
            )
            
            # Create segment
            segment = WireSegment(start_pos, end_pos, direction, distance)
            self.segments.append(segment)
            
            # Track all points with their step counts
            for i in range(distance):
                total_steps += 1
                current_pos = Point(current_pos.x + delta.x, current_pos.y + delta.y)
                if current_pos not in self.points_with_steps:
                    self.points_with_steps[current_pos] = total_steps
    
    def get_intersections(self, other: 'Wire') -> Set[Point]:
        """Find all intersection points with another wire."""
        intersections = set()
        
        # Use point sets for faster intersection detection
        self_points = set(self.points_with_steps.keys())
        other_points = set(other.points_with_steps.keys())
        
        # Find common points (excluding origin)
        common_points = self_points & other_points
        origin = Point(0, 0)
        if origin in common_points:
            common_points.remove(origin)
        
        return common_points
    
    def steps_to_point(self, point: Point) -> int:
        """Get the number of steps to reach a specific point."""
        return self.points_with_steps.get(point, float('inf'))


class WireIntersectionAnalyzer:
    """Analyzes wire intersections and calculates optimal paths."""
    
    def __init__(self, wire1: Wire, wire2: Wire):
        """Initialize with two wires to analyze."""
        self.wire1 = wire1
        self.wire2 = wire2
        self.intersections = wire1.get_intersections(wire2)
    
    def find_closest_intersection(self) -> Tuple[Point, int]:
        """
        Find the intersection point closest to the origin by Manhattan distance.
        
        Returns:
            Tuple of (closest_point, manhattan_distance)
        """
        if not self.intersections:
            return Point(0, 0), 0
        
        origin = Point(0, 0)
        closest_point = min(self.intersections, key=lambda p: p.manhattan_distance(origin))
        distance = closest_point.manhattan_distance(origin)
        
        return closest_point, distance
    
    def find_shortest_path_intersection(self) -> Tuple[Point, int]:
        """
        Find the intersection point with the shortest combined wire path.
        
        Returns:
            Tuple of (optimal_point, total_steps)
        """
        if not self.intersections:
            return Point(0, 0), 0
        
        min_steps = float('inf')
        optimal_point = Point(0, 0)
        
        for intersection in self.intersections:
            steps1 = self.wire1.steps_to_point(intersection)
            steps2 = self.wire2.steps_to_point(intersection)
            total_steps = steps1 + steps2
            
            if total_steps < min_steps:
                min_steps = total_steps
                optimal_point = intersection
        
        return optimal_point, min_steps
    
    def analyze_all_intersections(self) -> List[Dict]:
        """
        Analyze all intersections with comprehensive data.
        
        Returns:
            List of dictionaries containing intersection analysis
        """
        origin = Point(0, 0)
        analyses = []
        
        for intersection in self.intersections:
            analysis = {
                'point': intersection,
                'manhattan_distance': intersection.manhattan_distance(origin),
                'wire1_steps': self.wire1.steps_to_point(intersection),
                'wire2_steps': self.wire2.steps_to_point(intersection),
                'total_steps': (self.wire1.steps_to_point(intersection) + 
                               self.wire2.steps_to_point(intersection))
            }
            analyses.append(analysis)
        
        return sorted(analyses, key=lambda x: x['manhattan_distance'])


class Day3Solution(AdventSolution):
    """Enhanced solution for Day 3: Crossed Wires."""
    
    def __init__(self):
        super().__init__(year=2019, day=3, title="Crossed Wires")
    
    def part1(self, input_data: str) -> int:
        """
        Find the Manhattan distance to the closest intersection.
        
        Args:
            input_data: Two lines containing wire path specifications
            
        Returns:
            Manhattan distance to the closest intersection
        """
        lines = input_data.strip().split('\n')
        wire1 = Wire(lines[0])
        wire2 = Wire(lines[1])
        
        analyzer = WireIntersectionAnalyzer(wire1, wire2)
        closest_point, distance = analyzer.find_closest_intersection()
        
        return distance
    
    def part2(self, input_data: str) -> int:
        """
        Find the fewest combined steps to reach an intersection.
        
        Args:
            input_data: Two lines containing wire path specifications
            
        Returns:
            Minimum combined steps to reach any intersection
        """
        lines = input_data.strip().split('\n')
        wire1 = Wire(lines[0])
        wire2 = Wire(lines[1])
        
        analyzer = WireIntersectionAnalyzer(wire1, wire2)
        optimal_point, min_steps = analyzer.find_shortest_path_intersection()
        
        return min_steps
    
    def analyze_intersections(self, input_data: str) -> None:
        """
        Provide comprehensive analysis of all wire intersections.
        
        Args:
            input_data: Two lines containing wire path specifications
        """
        lines = input_data.strip().split('\n')
        wire1 = Wire(lines[0])
        wire2 = Wire(lines[1])
        
        analyzer = WireIntersectionAnalyzer(wire1, wire2)
        
        print(f"Wire 1 path: {wire1.path_string[:50]}{'...' if len(wire1.path_string) > 50 else ''}")
        print(f"Wire 2 path: {wire2.path_string[:50]}{'...' if len(wire2.path_string) > 50 else ''}")
        print(f"Total intersections found: {len(analyzer.intersections)}")
        
        if analyzer.intersections:
            analyses = analyzer.analyze_all_intersections()
            
            print("\nTop 5 intersections by Manhattan distance:")
            for i, analysis in enumerate(analyses[:5]):
                print(f"{i+1}. Point({analysis['point'].x}, {analysis['point'].y}): "
                      f"Manhattan={analysis['manhattan_distance']}, "
                      f"Steps={analysis['total_steps']}")
            
            closest_point, closest_distance = analyzer.find_closest_intersection()
            optimal_point, optimal_steps = analyzer.find_shortest_path_intersection()
            
            print(f"\nPart 1 - Closest intersection: {closest_point} (distance: {closest_distance})")
            print(f"Part 2 - Optimal intersection: {optimal_point} (steps: {optimal_steps})")

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""
        expected_part1 = 159
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        expected_part2 = 610
        
        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False
        
        print("✅ All Day 3 validation tests passed!")
        return True

def main():
    """Main execution function."""
    solution = Day3Solution()
    
    # If run with analyze flag, show comprehensive analysis
    if len(sys.argv) > 1 and sys.argv[1] == 'analyze':
        input_data = solution._load_input()
        solution.analyze_intersections(input_data)
    else:
        solution.main()


if __name__ == "__main__":
    main()