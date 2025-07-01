#!/usr/bin/env python3
"""
Advent of Code 2020 Day 17: Conway Cubes (OPTIMIZED)

High-performance 3D/4D cellular automaton with major optimizations:
- Tuple-based coordinates (no object overhead)
- Precomputed neighbor offsets
- Optimized set operations
- Eliminated unnecessary tracking
- Efficient candidate generation

Performance target: <2 seconds total execution time
"""

import sys
import os
from typing import Set, Tuple, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.advent_base import AdventSolution


# Precomputed neighbor offsets for 3D (26 neighbors)
NEIGHBORS_3D = [
    (dx, dy, dz) for dx in [-1, 0, 1] 
    for dy in [-1, 0, 1] 
    for dz in [-1, 0, 1]
    if not (dx == 0 and dy == 0 and dz == 0)
]

# Precomputed neighbor offsets for 4D (80 neighbors)
NEIGHBORS_4D = [
    (dx, dy, dz, dw) for dx in [-1, 0, 1] 
    for dy in [-1, 0, 1] 
    for dz in [-1, 0, 1]
    for dw in [-1, 0, 1]
    if not (dx == 0 and dy == 0 and dz == 0 and dw == 0)
]


def get_neighbors_3d(coord: Tuple[int, int, int]) -> list:
    """Get all 3D neighbors efficiently using precomputed offsets."""
    x, y, z = coord
    return [(x + dx, y + dy, z + dz) for dx, dy, dz in NEIGHBORS_3D]


def get_neighbors_4d(coord: Tuple[int, int, int, int]) -> list:
    """Get all 4D neighbors efficiently using precomputed offsets."""
    x, y, z, w = coord
    return [(x + dx, y + dy, z + dz, w + dw) for dx, dy, dz, dw in NEIGHBORS_4D]


def count_active_neighbors_3d(coord: Tuple[int, int, int], active_cubes: Set[Tuple[int, int, int]]) -> int:
    """Count active 3D neighbors efficiently."""
    x, y, z = coord
    count = 0
    for dx, dy, dz in NEIGHBORS_3D:
        if (x + dx, y + dy, z + dz) in active_cubes:
            count += 1
    return count


def count_active_neighbors_4d(coord: Tuple[int, int, int, int], active_cubes: Set[Tuple[int, int, int, int]]) -> int:
    """Count active 4D neighbors efficiently."""
    x, y, z, w = coord
    count = 0
    for dx, dy, dz, dw in NEIGHBORS_4D:
        if (x + dx, y + dy, z + dz, w + dw) in active_cubes:
            count += 1
    return count


def simulate_conway_cubes_3d(initial_state: str, cycles: int) -> int:
    """
    Optimized 3D Conway Cubes simulation.
    
    Returns the number of active cubes after the specified cycles.
    """
    # Parse initial state
    active_cubes = set()
    lines = initial_state.strip().split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == '#':
                active_cubes.add((x, y, 0))
    
    # Simulate cycles
    for _ in range(cycles):
        # Find all candidates (active cubes + their neighbors)
        candidates = set(active_cubes)
        for cube in active_cubes:
            x, y, z = cube
            for dx, dy, dz in NEIGHBORS_3D:
                candidates.add((x + dx, y + dy, z + dz))
        
        # Apply rules to all candidates
        new_active_cubes = set()
        for coord in candidates:
            active_neighbors = count_active_neighbors_3d(coord, active_cubes)
            is_active = coord in active_cubes
            
            if is_active:
                # Active cube stays active with 2 or 3 neighbors
                if active_neighbors in [2, 3]:
                    new_active_cubes.add(coord)
            else:
                # Inactive cube becomes active with exactly 3 neighbors
                if active_neighbors == 3:
                    new_active_cubes.add(coord)
        
        active_cubes = new_active_cubes
    
    return len(active_cubes)


def simulate_conway_cubes_4d(initial_state: str, cycles: int) -> int:
    """
    Optimized 4D Conway Cubes simulation.
    
    Returns the number of active cubes after the specified cycles.
    """
    # Parse initial state
    active_cubes = set()
    lines = initial_state.strip().split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == '#':
                active_cubes.add((x, y, 0, 0))
    
    # Simulate cycles
    for _ in range(cycles):
        # Find all candidates (active cubes + their neighbors)
        candidates = set(active_cubes)
        for cube in active_cubes:
            x, y, z, w = cube
            for dx, dy, dz, dw in NEIGHBORS_4D:
                candidates.add((x + dx, y + dy, z + dz, w + dw))
        
        # Apply rules to all candidates
        new_active_cubes = set()
        for coord in candidates:
            active_neighbors = count_active_neighbors_4d(coord, active_cubes)
            is_active = coord in active_cubes
            
            if is_active:
                # Active cube stays active with 2 or 3 neighbors
                if active_neighbors in [2, 3]:
                    new_active_cubes.add(coord)
            else:
                # Inactive cube becomes active with exactly 3 neighbors
                if active_neighbors == 3:
                    new_active_cubes.add(coord)
        
        active_cubes = new_active_cubes
    
    return len(active_cubes)


class Day17OptimizedSolution(AdventSolution):
    """Optimized solution for Advent of Code 2020 Day 17."""
    
    def __init__(self):
        super().__init__(year=2020, day=17, title="Conway Cubes (Optimized)")
    
    def part1(self, input_data: str) -> Any:
        """Part 1: 3D Conway Cubes simulation."""
        return simulate_conway_cubes_3d(input_data, 6)
    
    def part2(self, input_data: str) -> Any:
        """Part 2: 4D Conway Cubes simulation."""
        return simulate_conway_cubes_4d(input_data, 6)


# Legacy compatibility functions for test runner
def part1(input_data) -> int:
    """Legacy function for part 1."""
    if isinstance(input_data, str) and not ('\n' in input_data):
        # This is a filename
        try:
            with open(input_data, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            return -1
    else:
        content = input_data
    
    solution = Day17OptimizedSolution()
    return solution.part1(content)


def part2(input_data) -> int:
    """Legacy function for part 2."""
    if isinstance(input_data, str) and not ('\n' in input_data):
        # This is a filename
        try:
            with open(input_data, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            return -1
    else:
        content = input_data
    
    solution = Day17OptimizedSolution()
    return solution.part2(content)


def main():
    """Main function with dual compatibility."""
    if len(sys.argv) > 1 or '--test' in sys.argv or '--time' in sys.argv:
        # New AdventSolution mode
        solution = Day17OptimizedSolution()
        solution.main()
    else:
        # Legacy mode for compatibility
        print(part1("day17_input.txt"))
        print(part2("day17_input.txt"))


if __name__ == "__main__":
    main()