#!/usr/bin/env python3
"""
Advent of Code 2020 Day 24: Lobby Layout
https://adventofcode.com/2020/day/24

Hexagonal tile flipping puzzle using Conway's Game of Life-like rules.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Tuple, List, Set
import copy

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class Day24Solution(AdventSolution):
    """Solution for 2020 Day 24: Lobby Layout."""

    def __init__(self):
        super().__init__(2020, 24, "Lobby Layout")
        self.directions = ['e', 'se', 'sw', 'w', 'nw', 'ne']

    def split_instructions(self, line: str) -> List[str]:
        """
        Split a line of hexagonal directions into individual moves.
        
        Args:
            line: String containing direction instructions
            
        Returns:
            List of direction strings
        """
        instructions = []
        while len(line) > 0:
            for direction in self.directions:
                if line.startswith(direction):
                    instructions.append(direction)
                    line = line.replace(direction, '', 1)
                    break
        return instructions

    def get_tile_position(self, path: List[str]) -> Tuple[float, float]:
        """
        Get the final position of a tile after following a path.
        
        Uses hexagonal coordinate system where:
        - e/w moves change x by ±1
        - ne/sw moves change both x and y by ±0.5/±1
        - nw/se moves change both x and y by ±0.5/±1
        
        Args:
            path: List of direction strings
            
        Returns:
            Tuple of (x, y) coordinates
        """
        cur_x, cur_y = 0.0, 0.0
        
        for direction in path:
            if direction == 'e':
                cur_x += 1
            elif direction == 'se':
                cur_y += 1
                cur_x += 0.5
            elif direction == 'sw':
                cur_y += 1
                cur_x -= 0.5
            elif direction == 'w':
                cur_x -= 1
            elif direction == 'nw':
                cur_y -= 1
                cur_x -= 0.5
            elif direction == 'ne':
                cur_y -= 1
                cur_x += 0.5
                
        return (cur_x, cur_y)

    def get_adjacent_positions(self, pos: Tuple[float, float]) -> List[Tuple[float, float]]:
        """
        Get all adjacent positions to a given hexagonal tile.
        
        Args:
            pos: Current position as (x, y) tuple
            
        Returns:
            List of adjacent positions
        """
        x, y = pos
        return [
            (x + 1, y),      # e
            (x + 0.5, y + 1), # se
            (x - 0.5, y + 1), # sw
            (x - 1, y),      # w
            (x - 0.5, y - 1), # nw
            (x + 0.5, y - 1)  # ne
        ]

    def count_adjacent_black(self, pos: Tuple[float, float], floor_map: Dict[Tuple[float, float], int]) -> int:
        """
        Count the number of adjacent black tiles.
        
        Args:
            pos: Position to check
            floor_map: Current state of the floor (1=black, 0=white)
            
        Returns:
            Number of adjacent black tiles
        """
        count = 0
        for adj_pos in self.get_adjacent_positions(pos):
            if floor_map.get(adj_pos, 0) == 1:
                count += 1
        return count

    def expand_floor(self, floor_map: Dict[Tuple[float, float], int]) -> Dict[Tuple[float, float], int]:
        """
        Expand the floor map to include all adjacent positions of current tiles.
        
        Args:
            floor_map: Current floor state
            
        Returns:
            Expanded floor map with new positions initialized to white (0)
        """
        new_floor = copy.deepcopy(floor_map)
        
        for pos in floor_map.keys():
            for adj_pos in self.get_adjacent_positions(pos):
                if adj_pos not in floor_map:
                    new_floor[adj_pos] = 0
                    
        return new_floor

    def simulate_day(self, floor_map: Dict[Tuple[float, float], int]) -> Dict[Tuple[float, float], int]:
        """
        Simulate one day of tile flipping according to the rules.
        
        Rules:
        - Black tile with 0 or >2 adjacent black tiles becomes white
        - White tile with exactly 2 adjacent black tiles becomes black
        
        Args:
            floor_map: Current floor state
            
        Returns:
            New floor state after one day
        """
        # Expand to include all relevant positions
        expanded_floor = self.expand_floor(floor_map)
        new_floor = copy.deepcopy(expanded_floor)
        
        for pos, tile_color in expanded_floor.items():
            adjacent_black = self.count_adjacent_black(pos, expanded_floor)
            
            if tile_color == 1:  # black tile
                if adjacent_black == 0 or adjacent_black > 2:
                    new_floor[pos] = 0  # flip to white
            else:  # white tile
                if adjacent_black == 2:
                    new_floor[pos] = 1  # flip to black
                    
        return new_floor

    def count_black_tiles(self, floor_map: Dict[Tuple[float, float], int]) -> int:
        """Count the number of black tiles on the floor."""
        return sum(1 for color in floor_map.values() if color == 1)

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Count black tiles after initial flipping.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of black tiles after following all instructions
        """
        lines = input_data.strip().split('\n')
        floor_map = {}
        
        for line in lines:
            path = self.split_instructions(line.strip())
            tile_pos = self.get_tile_position(path)
            
            # Flip the tile (0=white, 1=black)
            if tile_pos not in floor_map:
                floor_map[tile_pos] = 1  # start white, flip to black
            else:
                floor_map[tile_pos] = 1 - floor_map[tile_pos]  # flip current state
                
        return self.count_black_tiles(floor_map)

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Count black tiles after 100 days of daily flipping.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of black tiles after 100 days
        """
        lines = input_data.strip().split('\n')
        floor_map = {}
        
        # Initial setup (same as part 1)
        for line in lines:
            path = self.split_instructions(line.strip())
            tile_pos = self.get_tile_position(path)
            
            if tile_pos not in floor_map:
                floor_map[tile_pos] = 1
            else:
                floor_map[tile_pos] = 1 - floor_map[tile_pos]
        
        # Simulate 100 days
        for day in range(1, 101):
            floor_map = self.simulate_day(floor_map)
            
        return self.count_black_tiles(floor_map)


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day24Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day24Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main function to run the solution."""
    solution = Day24Solution()
    solution.main()


if __name__ == "__main__":
    main()