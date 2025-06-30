#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 11: Seating System

Simulates a cellular automaton for airplane seating with two different visibility rules:
- Part 1: Adjacent neighbors (8-directional) with 4+ occupancy threshold
- Part 2: Line-of-sight visibility with 5+ occupancy threshold

The system evolves until it reaches a stable configuration.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Tuple, Dict, Any, Optional
from enum import Enum
import copy


class SeatState(Enum):
    """Represents the state of a seat in the seating system."""
    FLOOR = '.'
    EMPTY = 'L' 
    OCCUPIED = '#'


class SeatingSystem:
    """
    Manages the seating system simulation with cellular automaton rules.
    
    Handles both adjacent-based and line-of-sight visibility models.
    """
    
    def __init__(self, grid_data: str):
        """
        Initialize the seating system from input data.
        
        Args:
            grid_data: Raw grid data as string
        """
        self.original_grid = self._parse_grid(grid_data)
        self.grid = copy.deepcopy(self.original_grid)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0
        self.generation = 0
        
    def _parse_grid(self, grid_data: str) -> List[List[SeatState]]:
        """
        Parse the input grid data into a 2D array of SeatState enums.
        
        Args:
            grid_data: Raw grid data
            
        Returns:
            2D list of SeatState enums
        """
        lines = grid_data.strip().split('\n')
        grid = []
        
        for line in lines:
            row = []
            for char in line.strip():
                if char == '.':
                    row.append(SeatState.FLOOR)
                elif char == 'L':
                    row.append(SeatState.EMPTY)
                elif char == '#':
                    row.append(SeatState.OCCUPIED)
                else:
                    raise ValueError(f"Invalid seat character: {char}")
            grid.append(row)
            
        return grid
    
    def reset(self) -> None:
        """Reset the grid to its original state."""
        self.grid = copy.deepcopy(self.original_grid)
        self.generation = 0
    
    def get_occupied_count(self) -> int:
        """
        Count the total number of occupied seats.
        
        Returns:
            Number of occupied seats
        """
        count = 0
        for row in self.grid:
            for seat in row:
                if seat == SeatState.OCCUPIED:
                    count += 1
        return count
    
    def get_adjacent_occupied(self, row: int, col: int) -> int:
        """
        Count occupied seats in the 8 adjacent positions.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            Number of adjacent occupied seats
        """
        count = 0
        
        # Check all 8 directions
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the center position
                    
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.rows and 
                    0 <= new_col < self.cols and 
                    self.grid[new_row][new_col] == SeatState.OCCUPIED):
                    count += 1
                    
        return count
    
    def get_visible_occupied(self, row: int, col: int) -> int:
        """
        Count occupied seats visible in line-of-sight (8 directions).
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            Number of visible occupied seats
        """
        count = 0
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), 
                     (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            # Look in this direction until we find a seat or hit boundary
            current_row, current_col = row + dr, col + dc
            
            while (0 <= current_row < self.rows and 
                   0 <= current_col < self.cols):
                
                seat = self.grid[current_row][current_col]
                
                if seat == SeatState.OCCUPIED:
                    count += 1
                    break
                elif seat == SeatState.EMPTY:
                    break  # Empty seat blocks the view
                    
                # Floor doesn't block view, continue looking
                current_row += dr
                current_col += dc
                
        return count
    
    def simulate_step(self, use_visibility: bool = False, 
                     tolerance: int = 4) -> bool:
        """
        Perform one simulation step with the specified rules.
        
        Args:
            use_visibility: If True, use line-of-sight rules; otherwise adjacent
            tolerance: Minimum occupied neighbors to cause seat to empty
            
        Returns:
            True if the grid changed, False if stable
        """
        new_grid = copy.deepcopy(self.grid)
        changed = False
        
        for row in range(self.rows):
            for col in range(self.cols):
                current_seat = self.grid[row][col]
                
                if current_seat == SeatState.FLOOR:
                    continue  # Floor never changes
                
                # Count occupied neighbors based on rule type
                if use_visibility:
                    occupied_neighbors = self.get_visible_occupied(row, col)
                else:
                    occupied_neighbors = self.get_adjacent_occupied(row, col)
                
                # Apply transition rules
                if (current_seat == SeatState.EMPTY and 
                    occupied_neighbors == 0):
                    new_grid[row][col] = SeatState.OCCUPIED
                    changed = True
                elif (current_seat == SeatState.OCCUPIED and 
                      occupied_neighbors >= tolerance):
                    new_grid[row][col] = SeatState.EMPTY
                    changed = True
        
        self.grid = new_grid
        self.generation += 1
        return changed
    
    def simulate_until_stable(self, use_visibility: bool = False, 
                             tolerance: int = 4, 
                             max_generations: int = 1000) -> int:
        """
        Run simulation until the system reaches a stable state.
        
        Args:
            use_visibility: If True, use line-of-sight rules; otherwise adjacent
            tolerance: Minimum occupied neighbors to cause seat to empty
            max_generations: Maximum generations to prevent infinite loops
            
        Returns:
            Final number of occupied seats
        """
        self.reset()
        
        for gen in range(max_generations):
            if not self.simulate_step(use_visibility, tolerance):
                # System has stabilized
                break
        else:
            raise RuntimeError(f"System did not stabilize within {max_generations} generations")
        
        return self.get_occupied_count()
    
    def print_grid(self) -> None:
        """Print the current grid state for debugging."""
        print(f"=== Generation {self.generation} ===")
        for row in self.grid:
            print(''.join(seat.value for seat in row))
        print(f"Occupied seats: {self.get_occupied_count()}")
        print()
    
    def get_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis of the seating system.
        
        Returns:
            Dictionary with system metrics and statistics
        """
        total_seats = sum(1 for row in self.original_grid 
                         for seat in row if seat != SeatState.FLOOR)
        occupied_seats = self.get_occupied_count()
        empty_seats = sum(1 for row in self.grid 
                         for seat in row if seat == SeatState.EMPTY)
        floor_spaces = sum(1 for row in self.grid 
                          for seat in row if seat == SeatState.FLOOR)
        
        return {
            'grid_dimensions': (self.rows, self.cols),
            'total_positions': self.rows * self.cols,
            'total_seats': total_seats,
            'floor_spaces': floor_spaces,
            'current_occupied': occupied_seats,
            'current_empty': empty_seats,
            'occupancy_rate': occupied_seats / total_seats if total_seats > 0 else 0,
            'generations_to_stable': self.generation
        }


class Day11Solution(AdventSolution):
    """Solution for Advent of Code 2020 Day 11: Seating System."""
    
    def __init__(self):
        super().__init__(year=2020, day=11, title="Seating System")
        
    def part1(self, input_data: str) -> Any:
        """
        Solve part 1: Adjacent neighbor rules with 4+ tolerance.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Number of occupied seats when system stabilizes
        """
        seating_system = SeatingSystem(input_data)
        
        # Part 1: Adjacent neighbors, tolerance of 4
        result = seating_system.simulate_until_stable(
            use_visibility=False, tolerance=4
        )
        
        return result
    
    def part2(self, input_data: str) -> Any:
        """
        Solve part 2: Line-of-sight visibility rules with 5+ tolerance.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Number of occupied seats when system stabilizes
        """
        seating_system = SeatingSystem(input_data)
        
        # Part 2: Line-of-sight visibility, tolerance of 5
        result = seating_system.simulate_until_stable(
            use_visibility=True, tolerance=5
        )
        
        return result
    
    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Provide comprehensive analysis of the seating system.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis results for both parts
        """
        seating_system = SeatingSystem(input_data)
        
        # Analyze part 1
        part1_result = seating_system.simulate_until_stable(
            use_visibility=False, tolerance=4
        )
        part1_analysis = seating_system.get_analysis()
        
        # Analyze part 2
        part2_result = seating_system.simulate_until_stable(
            use_visibility=True, tolerance=5
        )
        part2_analysis = seating_system.get_analysis()
        
        return {
            'part1': {
                'result': part1_result,
                'analysis': part1_analysis,
                'rule_type': 'adjacent_neighbors',
                'tolerance': 4
            },
            'part2': {
                'result': part2_result,
                'analysis': part2_analysis,
                'rule_type': 'line_of_sight',
                'tolerance': 5
            },
            'comparison': {
                'part1_more_crowded': part1_result > part2_result,
                'stability_difference': abs(part1_analysis['generations_to_stable'] - 
                                          part2_analysis['generations_to_stable'])
            }
        }


# Legacy compatibility functions for test runner
def part1(filename: str) -> Any:
    """Legacy function for part 1."""
    with open(filename, 'r') as f:
        input_data = f.read()
    
    solution = Day11Solution()
    return solution.part1(input_data)


def part2(filename: str) -> Any:
    """Legacy function for part 2."""
    with open(filename, 'r') as f:
        input_data = f.read()
    
    solution = Day11Solution()
    return solution.part2(input_data)


if __name__ == "__main__":
    solution = Day11Solution()
    solution.main()