#!/usr/bin/env python3
"""
Advent of Code 2019 Day 19: Tractor Beam
Enhanced solution with object-oriented design and comprehensive analysis.
"""

import sys
import os
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
import time

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.advent_base import AdventSolution
from intcode import IntcodeOptimized


@dataclass
class Point:
    """Represents a 2D coordinate point."""
    x: int
    y: int
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass
class BeamSample:
    """Represents a beam detection sample at a specific point."""
    point: Point
    affected: bool
    
    def __str__(self) -> str:
        status = "affected" if self.affected else "clear"
        return f"{self.point}: {status}"


class TractorBeam:
    """
    Advanced tractor beam analysis system.
    
    This class provides efficient beam detection, area calculation,
    and optimization algorithms for analyzing the tractor beam pattern.
    """
    
    def __init__(self, program: str):
        """
        Initialize the TractorBeam with an Intcode program.
        
        Args:
            program: Comma-separated Intcode program string
        """
        self.program = program
        self.parsed_instructions = [int(x) for x in program.split(',')]
        self.beam_cache: Dict[Tuple[int, int], int] = {}
        self.sample_history: List[BeamSample] = []
        self.beam_bounds: Dict[int, Tuple[int, int]] = {}  # y -> (min_x, max_x)
    
    def _execute_intcode(self, x: int, y: int) -> int:
        """
        Execute the Intcode program to check if point (x,y) is affected by the beam.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            1 if affected by beam, 0 otherwise
        """
        if x < 0 or y < 0:
            return 0
        
        # Check cache first
        if (x, y) in self.beam_cache:
            return self.beam_cache[(x, y)]
        
        # Use optimized Intcode implementation
        machine = IntcodeOptimized(self.program)
        machine.add_input(x)
        machine.add_input(y)
        
        outputs = machine.run()
        result = outputs[0] if outputs else 0
        
        # Cache the result
        self.beam_cache[(x, y)] = result
        return result
    
    def check_point(self, point: Point) -> bool:
        """
        Check if a point is affected by the tractor beam.
        
        Args:
            point: Point to check
            
        Returns:
            True if point is affected by beam
        """
        result = self._execute_intcode(point.x, point.y) == 1
        sample = BeamSample(point, result)
        self.sample_history.append(sample)
        return result
    
    def scan_area(self, width: int, height: int) -> int:
        """
        Scan a rectangular area and count affected points.
        
        Args:
            width: Width of area to scan
            height: Height of area to scan
            
        Returns:
            Number of points affected by the beam
        """
        count = 0
        affected_points = []
        
        for y in range(height):
            for x in range(width):
                point = Point(x, y)
                if self.check_point(point):
                    count += 1
                    affected_points.append(point)
        
        return count
    
    def find_beam_bounds(self, y: int) -> Tuple[Optional[int], Optional[int]]:
        """
        Find the left and right bounds of the beam at a given y coordinate.
        
        Args:
            y: Y coordinate to check
            
        Returns:
            Tuple of (left_bound, right_bound) or (None, None) if no beam
        """
        if y in self.beam_bounds:
            return self.beam_bounds[y]
        
        # Find left bound
        left_bound = None
        for x in range(y * 2):  # Reasonable search limit
            if self.check_point(Point(x, y)):
                left_bound = x
                break
        
        if left_bound is None:
            self.beam_bounds[y] = (None, None)
            return (None, None)
        
        # Find right bound
        right_bound = left_bound
        x = left_bound + 1
        while x < y * 2 and self.check_point(Point(x, y)):
            right_bound = x
            x += 1
        
        self.beam_bounds[y] = (left_bound, right_bound)
        return (left_bound, right_bound)
    
    def find_beam_left_edge(self, y: int) -> Optional[int]:
        """Find the leftmost x coordinate where the beam starts at given y."""
        # For large y values, use a more conservative search approach
        # The beam expands roughly linearly, so start with a reasonable estimate
        
        # Quick check if there's any beam at all at this y level
        # Start checking from a reasonable position based on y
        search_start = max(0, y - 100)  # Start searching a bit before y
        search_end = y * 2  # Search up to 2*y
        
        # First, do a coarse search to find the general area
        coarse_step = max(1, (search_end - search_start) // 50)
        found_beam = False
        coarse_left = search_start
        
        for x in range(search_start, search_end, coarse_step):
            if self.check_point(Point(x, y)):
                coarse_left = max(search_start, x - coarse_step)
                found_beam = True
                break
        
        if not found_beam:
            return None
        
        # Now do fine-grained search from the coarse position
        for x in range(coarse_left, coarse_left + coarse_step + 10):
            if self.check_point(Point(x, y)):
                return x
        
        return None
    
    def find_square_position(self, square_size: int) -> Optional[Point]:
        """
        Find the top-left corner of the first square that fits in the beam.
        Uses a geometric approach based on beam expansion.
        
        Args:
            square_size: Size of the square to fit
            
        Returns:
            Top-left corner point of the square, or None if not found
        """
        # Different approach: find where bottom-left of square aligns with beam
        # For a square at (x,y), we need:
        # 1. Point (x + size - 1, y) in beam (top-right)
        # 2. Point (x, y + size - 1) in beam (bottom-left)
        
        # Start from reasonable distance  
        y = square_size * 5  # Start at a smaller distance
        
        while y < 2000:  # Expanded search limit
            # Find left edge of beam at y + size - 1 (where bottom-left will be)
            bottom_y = y + square_size - 1
            bottom_left_x = self.find_beam_left_edge(bottom_y)
            
            if bottom_left_x is None:
                y += 1
                continue
            
            # The top-left corner would be at (bottom_left_x, y)
            # Check if the top-right corner (bottom_left_x + size - 1, y) is in beam
            top_right_x = bottom_left_x + square_size - 1
            
            if self.check_point(Point(top_right_x, y)):
                # Found a valid square! The top-left is at (bottom_left_x, y)
                return Point(bottom_left_x, y)
            
            y += 1
        
        return None
    
    def get_beam_statistics(self) -> Dict[str, any]:
        """
        Get comprehensive statistics about beam sampling.
        
        Returns:
            Dictionary containing various beam statistics
        """
        total_samples = len(self.sample_history)
        affected_samples = sum(1 for s in self.sample_history if s.affected)
        
        # Calculate beam density
        beam_density = affected_samples / total_samples if total_samples > 0 else 0
        
        # Find extents
        if self.sample_history:
            min_x = min(s.point.x for s in self.sample_history)
            max_x = max(s.point.x for s in self.sample_history)
            min_y = min(s.point.y for s in self.sample_history)
            max_y = max(s.point.y for s in self.sample_history)
            
            area_sampled = (max_x - min_x + 1) * (max_y - min_y + 1)
        else:
            min_x = max_x = min_y = max_y = 0
            area_sampled = 0
        
        return {
            'total_samples': total_samples,
            'affected_samples': affected_samples,
            'clear_samples': total_samples - affected_samples,
            'beam_density': beam_density,
            'cache_size': len(self.beam_cache),
            'area_sampled': area_sampled,
            'sampling_bounds': {
                'min_x': min_x,
                'max_x': max_x,
                'min_y': min_y,
                'max_y': max_y
            }
        }
    
    def visualize_area(self, width: int, height: int) -> str:
        """
        Create a visual representation of the beam in a given area.
        
        Args:
            width: Width of area to visualize
            height: Height of area to visualize
            
        Returns:
            String representation of the beam pattern
        """
        lines = []
        for y in range(height):
            line = ""
            for x in range(width):
                if self.check_point(Point(x, y)):
                    line += "#"
                else:
                    line += "."
            lines.append(line)
        
        return "\n".join(lines)


class Day19Solution(AdventSolution):
    """Enhanced solution for Advent of Code 2019 Day 19: Tractor Beam."""
    
    def __init__(self):
        super().__init__(year=2019, day=19, title="Tractor Beam")
    
    def part1(self, input_data: str) -> int:
        """
        Count points affected by tractor beam in 50x50 area.
        
        Args:
            input_data: Intcode program
            
        Returns:
            Number of points affected in 50x50 grid
        """
        program = input_data.strip()
        beam = TractorBeam(program)
        return beam.scan_area(50, 50)
    
    def part2(self, input_data: str) -> int:
        """
        Find position for 100x100 square in tractor beam.
        
        Args:
            input_data: Intcode program
            
        Returns:
            Encoded position (x*10000 + y) of top-left corner
        """
        program = input_data.strip()
        beam = TractorBeam(program)
        
        square_position = beam.find_square_position(100)
        if square_position is None:
            return -1
        
        return square_position.x * 10000 + square_position.y
    
    def analyze(self, input_data: str) -> None:
        """
        Provide comprehensive analysis of the tractor beam.
        
        Args:
            input_data: Intcode program
        """
        program = input_data.strip()
        beam = TractorBeam(program)
        
        print("=== Tractor Beam Analysis ===\n")
        
        # Part 1 analysis
        print("Part 1 Analysis (50x50 scan):")
        start_time = time.time()
        affected_count = beam.scan_area(50, 50)
        scan_time = time.time() - start_time
        
        print(f"  Affected points: {affected_count}")
        print(f"  Scan time: {scan_time:.4f} seconds")
        
        # Get statistics after Part 1
        stats = beam.get_beam_statistics()
        print(f"  Beam density: {stats['beam_density']:.2%}")
        print(f"  Cache efficiency: {stats['cache_size']} cached results")
        
        # Part 2 analysis
        print(f"\nPart 2 Analysis (100x100 square):")
        start_time = time.time()
        square_pos = beam.find_square_position(100)
        search_time = time.time() - start_time
        
        if square_pos:
            encoded_pos = square_pos.x * 10000 + square_pos.y
            print(f"  Square position: {square_pos}")
            print(f"  Encoded position: {encoded_pos}")
            print(f"  Search time: {search_time:.4f} seconds")
        else:
            print("  No suitable position found")
        
        # Final statistics
        final_stats = beam.get_beam_statistics()
        print(f"\nFinal Statistics:")
        print(f"  Total samples: {final_stats['total_samples']}")
        print(f"  Affected samples: {final_stats['affected_samples']}")
        print(f"  Overall beam density: {final_stats['beam_density']:.2%}")
        print(f"  Cache size: {final_stats['cache_size']}")
        print(f"  Area sampled: {final_stats['area_sampled']}")
        
        # Small visualization
        print(f"\nBeam Pattern (20x20):")
        visualization = beam.visualize_area(20, 20)
        print(visualization)
        
        print(f"\nResults:")
        print(f"  Part 1: {affected_count}")
        if square_pos:
            print(f"  Part 2: {square_pos.x * 10000 + square_pos.y}")

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        print("ℹ️ No examples provided for Day 19, skipping validation")        
        #print("✅ All Day 19 validation tests passed!")
        return True
    
def main():
    """Main execution function."""
    solution = Day19Solution()
    solution.main()


if __name__ == "__main__":
    main()