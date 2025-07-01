#!/usr/bin/env python3
"""
Advent of Code 2020 Day 24: Lobby Layout (OPTIMIZED)

High-performance hexagonal Conway's Game of Life with major optimizations:
- Integer coordinate system (no floating point)
- Efficient neighbor lookup with precomputed offsets
- Set-based tracking (only store black tiles)
- Optimized direction parsing
- Minimal memory allocations

Performance target: <5 seconds total execution time
"""

import sys
import os
from typing import Set, Tuple, List, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.advent_base import AdventSolution


# Hexagonal coordinate system using axial coordinates (q, r)
# This avoids floating point arithmetic and is more efficient
DIRECTIONS = {
    'e':  (1, 0),
    'se': (0, 1), 
    'sw': (-1, 1),
    'w':  (-1, 0),
    'nw': (0, -1),
    'ne': (1, -1)
}

# Precomputed neighbor offsets for fast lookup
NEIGHBOR_OFFSETS = list(DIRECTIONS.values())


def parse_directions_optimized(line: str) -> List[str]:
    """
    Optimized direction parsing using direct character scanning.
    
    Much faster than string matching and replacement.
    """
    directions = []
    i = 0
    while i < len(line):
        if i + 1 < len(line):
            # Check two-character directions first
            two_char = line[i:i+2]
            if two_char in DIRECTIONS:
                directions.append(two_char)
                i += 2
                continue
        
        # Check one-character directions
        one_char = line[i]
        if one_char in DIRECTIONS:
            directions.append(one_char)
            i += 1
        else:
            i += 1  # Skip invalid characters
    
    return directions


def get_tile_position_optimized(directions: List[str]) -> Tuple[int, int]:
    """
    Get final tile position using integer axial coordinates.
    
    Axial coordinates are much more efficient than floating point.
    """
    q, r = 0, 0
    for direction in directions:
        dq, dr = DIRECTIONS[direction]
        q += dq
        r += dr
    return (q, r)


def get_neighbors(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Get all neighbor positions efficiently."""
    q, r = pos
    return [(q + dq, r + dr) for dq, dr in NEIGHBOR_OFFSETS]


def count_black_neighbors(pos: Tuple[int, int], black_tiles: Set[Tuple[int, int]]) -> int:
    """Count black neighbors efficiently using set lookup."""
    count = 0
    q, r = pos
    for dq, dr in NEIGHBOR_OFFSETS:
        if (q + dq, r + dr) in black_tiles:
            count += 1
    return count


def simulate_day_optimized(black_tiles: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """
    Optimized daily simulation using sets and minimal allocations.
    
    Only considers tiles that could possibly change state.
    """
    # Find all tiles that need to be checked (black tiles + their neighbors)
    candidates = set(black_tiles)
    for tile in black_tiles:
        q, r = tile
        for dq, dr in NEIGHBOR_OFFSETS:
            candidates.add((q + dq, r + dr))
    
    new_black_tiles = set()
    
    for tile in candidates:
        black_neighbors = count_black_neighbors(tile, black_tiles)
        is_black = tile in black_tiles
        
        if is_black:
            # Black tile stays black if it has 1 or 2 black neighbors
            if black_neighbors == 1 or black_neighbors == 2:
                new_black_tiles.add(tile)
        else:
            # White tile becomes black if it has exactly 2 black neighbors
            if black_neighbors == 2:
                new_black_tiles.add(tile)
    
    return new_black_tiles


class Day24OptimizedSolution(AdventSolution):
    """Optimized solution for Advent of Code 2020 Day 24."""
    
    def __init__(self):
        super().__init__(year=2020, day=24, title="Lobby Layout (Optimized)")
    
    def part1(self, input_data: str) -> Any:
        """Part 1: Count black tiles after initial flipping."""
        lines = input_data.strip().split('\n')
        black_tiles = set()
        
        for line in lines:
            directions = parse_directions_optimized(line.strip())
            tile_pos = get_tile_position_optimized(directions)
            
            # Flip tile (toggle presence in set)
            if tile_pos in black_tiles:
                black_tiles.remove(tile_pos)
            else:
                black_tiles.add(tile_pos)
        
        return len(black_tiles)
    
    def part2(self, input_data: str) -> Any:
        """Part 2: Count black tiles after 100 days."""
        lines = input_data.strip().split('\n')
        black_tiles = set()
        
        # Initial setup (same as part 1)
        for line in lines:
            directions = parse_directions_optimized(line.strip())
            tile_pos = get_tile_position_optimized(directions)
            
            if tile_pos in black_tiles:
                black_tiles.remove(tile_pos)
            else:
                black_tiles.add(tile_pos)
        
        # Simulate 100 days efficiently
        for _ in range(100):
            black_tiles = simulate_day_optimized(black_tiles)
        
        return len(black_tiles)


def main():
    """Main execution function."""
    solution = Day24OptimizedSolution()
    solution.main()


if __name__ == "__main__":
    main()