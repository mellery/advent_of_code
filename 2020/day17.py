#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 17: Conway Cubes

3D and 4D cellular automaton simulation implementing Conway's Game of Life rules:
- Part 1: 3D space simulation
- Part 2: 4D space simulation

Rules:
- Active cube with 2 or 3 active neighbors stays active
- Inactive cube with exactly 3 active neighbors becomes active
- All other cubes become/stay inactive
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import Dict, List, Tuple, Any, Set, Optional
from dataclasses import dataclass
from itertools import product
import copy


@dataclass(frozen=True)
class Coordinate:
    """Represents a coordinate in n-dimensional space."""
    x: int
    y: int
    z: int
    w: int = 0  # 4th dimension, defaults to 0 for 3D mode
    
    def get_neighbors(self, dimensions: int = 3) -> List['Coordinate']:
        """
        Get all neighboring coordinates.
        
        Args:
            dimensions: Number of dimensions (3 or 4)
            
        Returns:
            List of neighboring coordinates
        """
        neighbors = []
        
        if dimensions == 3:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        if dx == 0 and dy == 0 and dz == 0:
                            continue  # Skip self
                        neighbors.append(Coordinate(self.x + dx, self.y + dy, self.z + dz, 0))
        
        elif dimensions == 4:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        for dw in [-1, 0, 1]:
                            if dx == 0 and dy == 0 and dz == 0 and dw == 0:
                                continue  # Skip self
                            neighbors.append(Coordinate(self.x + dx, self.y + dy, self.z + dz, self.w + dw))
        
        else:
            raise ValueError(f"Unsupported dimensions: {dimensions}")
        
        return neighbors
    
    def __str__(self) -> str:
        if self.w == 0:
            return f"({self.x},{self.y},{self.z})"
        return f"({self.x},{self.y},{self.z},{self.w})"


class ConwayCube:
    """
    Represents the Conway Cubes cellular automaton simulation.
    
    Supports both 3D and 4D simulations with configurable rules.
    """
    
    def __init__(self, initial_state: str, dimensions: int = 3):
        """
        Initialize the Conway Cubes simulation.
        
        Args:
            initial_state: 2D grid representing the initial state
            dimensions: Number of dimensions (3 or 4)
        """
        self.dimensions = dimensions
        self.active_cubes: Set[Coordinate] = set()
        self.cycle = 0
        self.history: List[int] = []  # Track active cube count per cycle
        
        self._parse_initial_state(initial_state)
    
    def _parse_initial_state(self, state_str: str) -> None:
        """
        Parse the initial 2D state into active cubes.
        
        Args:
            state_str: String representation of initial 2D grid
        """
        lines = state_str.strip().split('\n')
        
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == '#':
                    coord = Coordinate(x, y, 0, 0)
                    self.active_cubes.add(coord)
    
    def count_active_neighbors(self, coord: Coordinate) -> int:
        """
        Count active neighbors of a coordinate.
        
        Args:
            coord: Coordinate to check
            
        Returns:
            Number of active neighbors
        """
        count = 0
        for neighbor in coord.get_neighbors(self.dimensions):
            if neighbor in self.active_cubes:
                count += 1
        return count
    
    def get_candidates_for_next_cycle(self) -> Set[Coordinate]:
        """
        Get all coordinates that might change state in the next cycle.
        
        Returns:
            Set of coordinates to evaluate
        """
        candidates = set()
        
        # All currently active cubes and their neighbors are candidates
        for active_cube in self.active_cubes:
            candidates.add(active_cube)
            candidates.update(active_cube.get_neighbors(self.dimensions))
        
        return candidates
    
    def simulate_cycle(self) -> None:
        """
        Simulate one cycle of the cellular automaton.
        """
        candidates = self.get_candidates_for_next_cycle()
        new_active_cubes = set()
        
        for coord in candidates:
            active_neighbors = self.count_active_neighbors(coord)
            is_currently_active = coord in self.active_cubes
            
            # Apply Conway Cubes rules
            if is_currently_active:
                # Active cube stays active with 2 or 3 neighbors
                if active_neighbors in [2, 3]:
                    new_active_cubes.add(coord)
            else:
                # Inactive cube becomes active with exactly 3 neighbors
                if active_neighbors == 3:
                    new_active_cubes.add(coord)
        
        self.active_cubes = new_active_cubes
        self.cycle += 1
        self.history.append(len(self.active_cubes))
    
    def simulate_cycles(self, num_cycles: int) -> int:
        """
        Simulate multiple cycles.
        
        Args:
            num_cycles: Number of cycles to simulate
            
        Returns:
            Number of active cubes after simulation
        """
        for _ in range(num_cycles):
            self.simulate_cycle()
        
        return len(self.active_cubes)
    
    def get_bounds(self) -> Dict[str, Tuple[int, int]]:
        """
        Get the bounding box of all active cubes.
        
        Returns:
            Dictionary with min/max bounds for each dimension
        """
        if not self.active_cubes:
            return {'x': (0, 0), 'y': (0, 0), 'z': (0, 0), 'w': (0, 0)}
        
        coords = list(self.active_cubes)
        
        bounds = {
            'x': (min(c.x for c in coords), max(c.x for c in coords)),
            'y': (min(c.y for c in coords), max(c.y for c in coords)),
            'z': (min(c.z for c in coords), max(c.z for c in coords)),
            'w': (min(c.w for c in coords), max(c.w for c in coords))
        }
        
        return bounds
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the simulation.
        
        Returns:
            Dictionary with simulation statistics
        """
        bounds = self.get_bounds()
        
        # Calculate volume
        x_range = bounds['x'][1] - bounds['x'][0] + 1
        y_range = bounds['y'][1] - bounds['y'][0] + 1
        z_range = bounds['z'][1] - bounds['z'][0] + 1
        
        if self.dimensions == 4:
            w_range = bounds['w'][1] - bounds['w'][0] + 1
            total_volume = x_range * y_range * z_range * w_range
        else:
            total_volume = x_range * y_range * z_range
        
        return {
            'dimensions': self.dimensions,
            'current_cycle': self.cycle,
            'active_cubes': len(self.active_cubes),
            'bounds': bounds,
            'space_dimensions': {
                'x_range': x_range,
                'y_range': y_range,
                'z_range': z_range,
                'w_range': bounds['w'][1] - bounds['w'][0] + 1 if self.dimensions == 4 else 1
            },
            'total_volume': total_volume,
            'density': len(self.active_cubes) / total_volume if total_volume > 0 else 0,
            'growth_history': self.history,
            'growth_rate': self._calculate_growth_rate()
        }
    
    def _calculate_growth_rate(self) -> Optional[float]:
        """Calculate the average growth rate over the simulation."""
        if len(self.history) < 2:
            return None
        
        initial = self.history[0] if self.history else len(self.active_cubes)
        final = self.history[-1]
        cycles = len(self.history)
        
        if initial == 0:
            return None
        
        return (final / initial) ** (1 / cycles) - 1 if cycles > 0 else 0
    
    def visualize_slice(self, z: int = 0, w: int = 0) -> str:
        """
        Create a visual representation of a 2D slice.
        
        Args:
            z: Z-coordinate of the slice
            w: W-coordinate of the slice (for 4D)
            
        Returns:
            String representation of the slice
        """
        bounds = self.get_bounds()
        
        if not self.active_cubes:
            return "(empty)"
        
        lines = []
        for y in range(bounds['y'][0], bounds['y'][1] + 1):
            line = ""
            for x in range(bounds['x'][0], bounds['x'][1] + 1):
                coord = Coordinate(x, y, z, w)
                if coord in self.active_cubes:
                    line += "#"
                else:
                    line += "."
            lines.append(line)
        
        return "\n".join(lines)
    
    def reset(self, initial_state: str) -> None:
        """
        Reset the simulation to initial state.
        
        Args:
            initial_state: New initial state
        """
        self.active_cubes.clear()
        self.cycle = 0
        self.history.clear()
        self._parse_initial_state(initial_state)


class Day17Solution(AdventSolution):
    """Solution for Advent of Code 2020 Day 17: Conway Cubes."""
    
    def __init__(self):
        super().__init__(year=2020, day=17, title="Conway Cubes")
    
    def part1(self, input_data: str) -> Any:
        """
        Solve part 1: 3D Conway Cubes simulation.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Number of active cubes after 6 cycles in 3D
        """
        simulator = ConwayCube(input_data, dimensions=3)
        return simulator.simulate_cycles(6)
    
    def part2(self, input_data: str) -> Any:
        """
        Solve part 2: 4D Conway Cubes simulation.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Number of active cubes after 6 cycles in 4D
        """
        simulator = ConwayCube(input_data, dimensions=4)
        return simulator.simulate_cycles(6)
    
    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Provide comprehensive analysis of the Conway Cubes problem.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis results for both parts
        """
        # Analyze 3D simulation
        sim_3d = ConwayCube(input_data, dimensions=3)
        part1_result = sim_3d.simulate_cycles(6)
        stats_3d = sim_3d.get_statistics()
        
        # Analyze 4D simulation
        sim_4d = ConwayCube(input_data, dimensions=4)
        part2_result = sim_4d.simulate_cycles(6)
        stats_4d = sim_4d.get_statistics()
        
        # Compare initial state
        initial_sim = ConwayCube(input_data, dimensions=3)
        initial_stats = initial_sim.get_statistics()
        
        return {
            'initial_state': {
                'active_cubes': len(initial_sim.active_cubes),
                'bounds': initial_stats['bounds'],
                'visualization': initial_sim.visualize_slice(0, 0)
            },
            'part1': {
                'result': part1_result,
                'dimensions': 3,
                'statistics': stats_3d,
                'method': '3D_cellular_automaton'
            },
            'part2': {
                'result': part2_result,
                'dimensions': 4,
                'statistics': stats_4d,
                'method': '4D_cellular_automaton'
            },
            'comparison': {
                'growth_3d_vs_4d': part2_result / part1_result if part1_result > 0 else 0,
                'space_expansion_3d': stats_3d['total_volume'],
                'space_expansion_4d': stats_4d['total_volume'],
                'density_3d': stats_3d['density'],
                'density_4d': stats_4d['density']
            },
            'algorithm': {
                'name': 'Conway Cubes (3D/4D Game of Life)',
                'complexity': 'O(cycles * active_cubes * neighbors_per_cube)',
                'neighbors_3d': 26,
                'neighbors_4d': 80,
                'growth_pattern': 'Exponential in early cycles, then stabilizes'
            },
            'visualizations': {
                'final_3d_slice_z0': sim_3d.visualize_slice(0, 0),
                'final_4d_slice_z0_w0': sim_4d.visualize_slice(0, 0)
            }
        }


# Legacy compatibility functions for test runner
def part1(filename: str) -> Any:
    """Legacy function for part 1."""
    with open(filename, 'r') as f:
        input_data = f.read()
    
    solution = Day17Solution()
    return solution.part1(input_data)


def part2(filename: str) -> Any:
    """Legacy function for part 2."""
    with open(filename, 'r') as f:
        input_data = f.read()
    
    solution = Day17Solution()
    return solution.part2(input_data)


if __name__ == "__main__":
    solution = Day17Solution()
    solution.main()

