#!/usr/bin/env python3
"""
Advent of Code 2019 Day 12: The N-Body Problem
Enhanced solution with object-oriented design and comprehensive analysis.
"""

import sys
import os
import re
import itertools
from math import gcd
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
from functools import reduce

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.advent_base import AdventSolution


@dataclass
class Vector3D:
    """Represents a 3D vector for position or velocity."""
    x: int
    y: int
    z: int
    
    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        """Add two vectors."""
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        """Subtract two vectors."""
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def manhattan_magnitude(self) -> int:
        """Calculate the Manhattan distance magnitude."""
        return abs(self.x) + abs(self.y) + abs(self.z)
    
    def __eq__(self, other) -> bool:
        """Check equality of vectors."""
        if not isinstance(other, Vector3D):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self) -> int:
        """Make vector hashable."""
        return hash((self.x, self.y, self.z))
    
    def __str__(self) -> str:
        """String representation."""
        return f"<x={self.x}, y={self.y}, z={self.z}>"


class Moon:
    """
    Represents a moon in the Jupiter system with position and velocity.
    
    Each moon experiences gravitational forces from all other moons,
    affecting its velocity and subsequently its position.
    """
    
    def __init__(self, name: str, position: Vector3D):
        """
        Initialize a moon with a name and starting position.
        
        Args:
            name: Identifier for the moon
            position: Starting 3D position
        """
        self.name = name
        self.position = position
        self.velocity = Vector3D(0, 0, 0)
        self.initial_position = Vector3D(position.x, position.y, position.z)
        self.step_count = 0
    
    def apply_gravity_from(self, other: 'Moon') -> None:
        """
        Apply gravitational force from another moon.
        
        Args:
            other: The moon exerting gravitational force
        """
        # X-axis gravity
        if self.position.x > other.position.x:
            self.velocity.x -= 1
        elif self.position.x < other.position.x:
            self.velocity.x += 1
        
        # Y-axis gravity
        if self.position.y > other.position.y:
            self.velocity.y -= 1
        elif self.position.y < other.position.y:
            self.velocity.y += 1
        
        # Z-axis gravity
        if self.position.z > other.position.z:
            self.velocity.z -= 1
        elif self.position.z < other.position.z:
            self.velocity.z += 1
    
    def apply_velocity(self) -> None:
        """Update position based on current velocity."""
        self.position = self.position + self.velocity
        self.step_count += 1
    
    def potential_energy(self) -> int:
        """Calculate potential energy (sum of absolute coordinate values)."""
        return self.position.manhattan_magnitude()
    
    def kinetic_energy(self) -> int:
        """Calculate kinetic energy (sum of absolute velocity values)."""
        return self.velocity.manhattan_magnitude()
    
    def total_energy(self) -> int:
        """Calculate total energy (potential × kinetic)."""
        return self.potential_energy() * self.kinetic_energy()
    
    def get_axis_state(self, axis: str) -> Tuple[int, int]:
        """
        Get position and velocity for a specific axis.
        
        Args:
            axis: 'x', 'y', or 'z'
            
        Returns:
            Tuple of (position, velocity) for the axis
        """
        if axis == 'x':
            return (self.position.x, self.velocity.x)
        elif axis == 'y':
            return (self.position.y, self.velocity.y)
        elif axis == 'z':
            return (self.position.z, self.velocity.z)
        else:
            raise ValueError(f"Invalid axis: {axis}")
    
    def reset_to_initial(self) -> None:
        """Reset moon to its initial state."""
        self.position = Vector3D(
            self.initial_position.x,
            self.initial_position.y,
            self.initial_position.z
        )
        self.velocity = Vector3D(0, 0, 0)
        self.step_count = 0
    
    def __str__(self) -> str:
        """String representation of the moon."""
        return (f"{self.name}: pos={self.position}, vel={self.velocity}, "
                f"energy={self.total_energy()}")


class JupiterSystem:
    """
    Simulates the gravitational system of Jupiter's moons.
    
    This class manages the orbital mechanics simulation, tracking
    moon positions, velocities, and energy states over time.
    """
    
    def __init__(self, moon_data: List[Tuple[str, Vector3D]]):
        """
        Initialize the Jupiter system with moon data.
        
        Args:
            moon_data: List of (name, position) tuples for each moon
        """
        self.moons = [Moon(name, pos) for name, pos in moon_data]
        self.step_count = 0
        self.initial_state = self._capture_state()
        
        # For cycle detection
        self.axis_periods = {'x': None, 'y': None, 'z': None}
        self.axis_initial_states = {
            'x': self._capture_axis_state('x'),
            'y': self._capture_axis_state('y'),
            'z': self._capture_axis_state('z')
        }
    
    def _capture_state(self) -> List[Tuple[Vector3D, Vector3D]]:
        """Capture the current state of all moons."""
        return [(moon.position, moon.velocity) for moon in self.moons]
    
    def _capture_axis_state(self, axis: str) -> List[Tuple[int, int]]:
        """Capture the current state for a specific axis."""
        return [moon.get_axis_state(axis) for moon in self.moons]
    
    def simulate_step(self) -> None:
        """Simulate one time step of the gravitational system."""
        # Apply gravity between all pairs of moons
        for moon1, moon2 in itertools.combinations(self.moons, 2):
            moon1.apply_gravity_from(moon2)
            moon2.apply_gravity_from(moon1)
        
        # Update positions based on velocities
        for moon in self.moons:
            moon.apply_velocity()
        
        self.step_count += 1
    
    def simulate_steps(self, num_steps: int) -> None:
        """
        Simulate multiple time steps.
        
        Args:
            num_steps: Number of steps to simulate
        """
        for _ in range(num_steps):
            self.simulate_step()
    
    def total_energy(self) -> int:
        """Calculate total energy of the system."""
        return sum(moon.total_energy() for moon in self.moons)
    
    def find_cycle_length(self) -> int:
        """
        Find the number of steps until the system returns to its initial state.
        
        Since the system is deterministic and finite, it must eventually cycle.
        We can optimize by finding cycles for each axis independently.
        
        Returns:
            Number of steps to complete one full cycle
        """
        # Find period for each axis independently
        step = 0
        
        while not all(self.axis_periods.values()):
            self.simulate_step()
            step += 1
            
            # Check each axis that hasn't found its period yet
            for axis in ['x', 'y', 'z']:
                if self.axis_periods[axis] is None:
                    current_state = self._capture_axis_state(axis)
                    if current_state == self.axis_initial_states[axis]:
                        self.axis_periods[axis] = step
                        print(f"Axis {axis} cycle found: {step} steps")
        
        # Calculate LCM of all axis periods
        periods = list(self.axis_periods.values())
        return self._lcm_of_list(periods)
    
    def _lcm_of_list(self, numbers: List[int]) -> int:
        """Calculate LCM of a list of numbers."""
        return reduce(self._lcm, numbers)
    
    def _lcm(self, a: int, b: int) -> int:
        """Calculate LCM of two numbers."""
        return abs(a * b) // gcd(a, b)
    
    def get_analysis(self) -> Dict[str, any]:
        """
        Analyze the current state of the Jupiter system.
        
        Returns:
            Dictionary with comprehensive analysis data
        """
        total_potential = sum(moon.potential_energy() for moon in self.moons)
        total_kinetic = sum(moon.kinetic_energy() for moon in self.moons)
        total_system_energy = self.total_energy()
        
        # Calculate center of mass
        total_mass = len(self.moons)  # Assuming unit mass for each moon
        center_x = sum(moon.position.x for moon in self.moons) / total_mass
        center_y = sum(moon.position.y for moon in self.moons) / total_mass
        center_z = sum(moon.position.z for moon in self.moons) / total_mass
        
        # Calculate velocity of center of mass
        velocity_x = sum(moon.velocity.x for moon in self.moons) / total_mass
        velocity_y = sum(moon.velocity.y for moon in self.moons) / total_mass
        velocity_z = sum(moon.velocity.z for moon in self.moons) / total_mass
        
        return {
            'step_count': self.step_count,
            'total_energy': total_system_energy,
            'total_potential_energy': total_potential,
            'total_kinetic_energy': total_kinetic,
            'center_of_mass': (center_x, center_y, center_z),
            'center_velocity': (velocity_x, velocity_y, velocity_z),
            'moon_count': len(self.moons),
            'axis_periods': dict(self.axis_periods),
            'individual_energies': [(moon.name, moon.total_energy()) for moon in self.moons]
        }
    
    def reset_to_initial(self) -> None:
        """Reset the system to its initial state."""
        for moon in self.moons:
            moon.reset_to_initial()
        self.step_count = 0
        self.axis_periods = {'x': None, 'y': None, 'z': None}
    
    def __str__(self) -> str:
        """String representation of the system."""
        lines = [f"After {self.step_count} steps:"]
        for moon in self.moons:
            lines.append(str(moon))
        lines.append(f"Sum of total energy: {self.total_energy()}")
        return "\n".join(lines)


class Day12Solution(AdventSolution):
    """Enhanced solution for Advent of Code 2019 Day 12: The N-Body Problem."""
    
    def __init__(self):
        super().__init__(year=2019, day=12, title="The N-Body Problem")
    
    def _parse_moon_positions(self, input_data: str) -> List[Tuple[str, Vector3D]]:
        """
        Parse moon positions from input data.
        
        Args:
            input_data: Input string with moon position data
            
        Returns:
            List of (name, position) tuples
        """
        moons = []
        lines = input_data.strip().split('\n')
        
        for i, line in enumerate(lines):
            # Parse format: <x=-1, y=0, z=2>
            match = re.match(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', line.strip())
            if match:
                x, y, z = map(int, match.groups())
                moons.append((f"Moon{i+1}", Vector3D(x, y, z)))
        
        return moons
    
    def part1(self, input_data: str) -> int:
        """
        Calculate total energy after 1000 simulation steps.
        
        Args:
            input_data: Input string with moon position data
            
        Returns:
            Total energy of the system after 1000 steps
        """
        moon_data = self._parse_moon_positions(input_data)
        system = JupiterSystem(moon_data)
        system.simulate_steps(1000)
        return system.total_energy()
    
    def part2(self, input_data: str) -> int:
        """
        Find the number of steps until the system returns to initial state.
        
        Args:
            input_data: Input string with moon position data
            
        Returns:
            Number of steps for one complete cycle
        """
        moon_data = self._parse_moon_positions(input_data)
        system = JupiterSystem(moon_data)
        return system.find_cycle_length()
    
    def analyze(self, input_data: str) -> None:
        """
        Provide comprehensive analysis of the Jupiter system simulation.
        
        Args:
            input_data: Input string with moon position data
        """
        moon_data = self._parse_moon_positions(input_data)
        
        print("=== Jupiter System Analysis ===\n")
        
        # Initial state
        system = JupiterSystem(moon_data)
        print("Initial State:")
        print(system)
        
        # Analyze at various intervals
        intervals = [10, 100, 1000]
        for steps in intervals:
            system.reset_to_initial()
            system.simulate_steps(steps)
            analysis = system.get_analysis()
            
            print(f"\nAfter {steps} steps:")
            print(f"  Total Energy: {analysis['total_energy']}")
            print(f"  Potential Energy: {analysis['total_potential_energy']}")
            print(f"  Kinetic Energy: {analysis['total_kinetic_energy']}")
            print(f"  Center of Mass: {analysis['center_of_mass']}")
            print(f"  Center Velocity: {analysis['center_velocity']}")
        
        # Find cycle information
        print(f"\nPart 1 Result: {self.part1(input_data)}")
        
        print("\nFinding system cycle...")
        system.reset_to_initial()
        cycle_length = system.find_cycle_length()
        
        print(f"\nPart 2 Result: {cycle_length}")
        print(f"Full system cycle: {cycle_length:,} steps")
        
        final_analysis = system.get_analysis()
        if final_analysis['axis_periods']:
            print(f"\nAxis cycle periods:")
            for axis, period in final_analysis['axis_periods'].items():
                print(f"  {axis.upper()}-axis: {period:,} steps")


# Legacy functions for test runner compatibility
def part1(input_data: str = None) -> int:
    """Legacy part1 function for test runner compatibility."""
    if input_data is None:
        # Auto-load input file or use embedded test data
        try:
            with open('/home/mike/src/advent_of_code/2019/day12_input.txt', 'r') as f:
                input_data = f.read()
        except FileNotFoundError:
            # Use the coordinates from the original solution
            input_data = """<x=3, y=2, z=-6>
<x=-13, y=18, z=10>
<x=-8, y=-1, z=13>
<x=5, y=10, z=4>"""
    
    solution = Day12Solution()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Legacy part2 function for test runner compatibility."""
    if input_data is None:
        # Auto-load input file or use embedded test data
        try:
            with open('/home/mike/src/advent_of_code/2019/day12_input.txt', 'r') as f:
                input_data = f.read()
        except FileNotFoundError:
            # Use the coordinates from the original solution
            input_data = """<x=3, y=2, z=-6>
<x=-13, y=18, z=10>
<x=-8, y=-1, z=13>
<x=5, y=10, z=4>"""
    
    solution = Day12Solution()
    return solution.part2(input_data)


if __name__ == "__main__":
    solution = Day12Solution()
    solution.main()