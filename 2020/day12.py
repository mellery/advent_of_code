#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 12: Rain Risk

Navigation system for a ship with two different movement models:
- Part 1: Ship moves directly based on commands and facing direction
- Part 2: Ship moves relative to a waypoint that can be rotated and moved

The challenge involves parsing navigation instructions and calculating Manhattan distance.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Tuple, Dict, Any, Optional
from enum import Enum
import math


class Direction(Enum):
    """Cardinal directions for navigation."""
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'


class Turn(Enum):
    """Turn directions."""
    LEFT = 'L'
    RIGHT = 'R'


class Action(Enum):
    """Navigation actions."""
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'
    LEFT = 'L'
    RIGHT = 'R'
    FORWARD = 'F'


class NavigationInstruction:
    """Represents a single navigation instruction."""
    
    def __init__(self, action: Action, value: int):
        """
        Initialize a navigation instruction.
        
        Args:
            action: The action to perform
            value: The value/magnitude for the action
        """
        self.action = action
        self.value = value
    
    def __str__(self) -> str:
        return f"{self.action.value}{self.value}"
    
    def __repr__(self) -> str:
        return f"NavigationInstruction({self.action}, {self.value})"


class Position:
    """Represents a 2D position with convenient coordinate operations."""
    
    def __init__(self, x: int = 0, y: int = 0):
        """
        Initialize position.
        
        Args:
            x: East-West coordinate (positive = East)
            y: North-South coordinate (positive = North)
        """
        self.x = x
        self.y = y
    
    def move(self, direction: Direction, distance: int) -> 'Position':
        """
        Move in a cardinal direction and return new position.
        
        Args:
            direction: Direction to move
            distance: Distance to move
            
        Returns:
            New Position after movement
        """
        new_x, new_y = self.x, self.y
        
        if direction == Direction.NORTH:
            new_y += distance
        elif direction == Direction.SOUTH:
            new_y -= distance
        elif direction == Direction.EAST:
            new_x += distance
        elif direction == Direction.WEST:
            new_x -= distance
            
        return Position(new_x, new_y)
    
    def manhattan_distance_from_origin(self) -> int:
        """Calculate Manhattan distance from origin (0,0)."""
        return abs(self.x) + abs(self.y)
    
    def __add__(self, other: 'Position') -> 'Position':
        """Add two positions."""
        return Position(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar: int) -> 'Position':
        """Multiply position by scalar."""
        return Position(self.x * scalar, self.y * scalar)
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return f"Position({self.x}, {self.y})"


class Waypoint:
    """Represents a waypoint relative to the ship."""
    
    def __init__(self, x: int = 10, y: int = 1):
        """
        Initialize waypoint.
        
        Args:
            x: East-West offset from ship (positive = East)
            y: North-South offset from ship (positive = North)
        """
        self.position = Position(x, y)
    
    def move(self, direction: Direction, distance: int) -> None:
        """
        Move the waypoint in a cardinal direction.
        
        Args:
            direction: Direction to move waypoint
            distance: Distance to move waypoint
        """
        self.position = self.position.move(direction, distance)
    
    def rotate(self, turn: Turn, degrees: int) -> None:
        """
        Rotate the waypoint around the ship.
        
        Args:
            turn: Direction to rotate (LEFT or RIGHT)
            degrees: Degrees to rotate (must be multiple of 90)
        """
        if degrees % 90 != 0:
            raise ValueError("Rotation degrees must be multiple of 90")
        
        # Normalize to 0-270 range
        degrees = degrees % 360
        
        # Convert LEFT turns to equivalent RIGHT turns for consistency
        if turn == Turn.LEFT:
            degrees = 360 - degrees
        
        # Perform rotation in 90-degree increments
        for _ in range(degrees // 90):
            # Clockwise 90-degree rotation: (x, y) -> (y, -x)
            old_x, old_y = self.position.x, self.position.y
            self.position.x = old_y
            self.position.y = -old_x
    
    def get_direction_description(self) -> str:
        """Get a human-readable description of waypoint position."""
        x_desc = f"{abs(self.position.x)} {'east' if self.position.x >= 0 else 'west'}"
        y_desc = f"{abs(self.position.y)} {'north' if self.position.y >= 0 else 'south'}"
        return f"{x_desc}, {y_desc}"
    
    def __str__(self) -> str:
        return f"Waypoint: {self.get_direction_description()}"


class Ship:
    """Represents a ship with navigation capabilities."""
    
    def __init__(self):
        """Initialize ship at origin facing East."""
        self.position = Position(0, 0)
        self.facing = Direction.EAST
        self.waypoint = Waypoint(10, 1)  # Default waypoint for part 2
        self.navigation_log: List[str] = []
    
    def reset(self) -> None:
        """Reset ship to initial state."""
        self.position = Position(0, 0)
        self.facing = Direction.EAST
        self.waypoint = Waypoint(10, 1)
        self.navigation_log.clear()
    
    def turn(self, turn_direction: Turn, degrees: int) -> None:
        """
        Turn the ship to face a new direction.
        
        Args:
            turn_direction: LEFT or RIGHT
            degrees: Degrees to turn (must be multiple of 90)
        """
        if degrees % 90 != 0:
            raise ValueError("Turn degrees must be multiple of 90")
        
        # Map current facing to index
        directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        current_index = directions.index(self.facing)
        
        # Calculate turn steps (90-degree increments)
        steps = degrees // 90
        if turn_direction == Turn.LEFT:
            steps = -steps
        
        # Update facing direction
        new_index = (current_index + steps) % 4
        self.facing = directions[new_index]
    
    def move_forward(self, distance: int) -> None:
        """
        Move the ship forward in its current facing direction.
        
        Args:
            distance: Distance to move forward
        """
        self.position = self.position.move(self.facing, distance)
    
    def move_toward_waypoint(self, times: int) -> None:
        """
        Move ship toward waypoint multiple times.
        
        Args:
            times: Number of times to move to waypoint
        """
        offset = self.waypoint.position * times
        self.position = self.position + offset
    
    def execute_instruction_direct(self, instruction: NavigationInstruction) -> None:
        """
        Execute instruction using direct ship movement (Part 1 rules).
        
        Args:
            instruction: Instruction to execute
        """
        action = instruction.action
        value = instruction.value
        
        if action in [Action.NORTH, Action.SOUTH, Action.EAST, Action.WEST]:
            # Move ship directly in cardinal direction
            direction = Direction(action.value)
            self.position = self.position.move(direction, value)
            
        elif action in [Action.LEFT, Action.RIGHT]:
            # Turn the ship
            turn_direction = Turn(action.value)
            self.turn(turn_direction, value)
            
        elif action == Action.FORWARD:
            # Move forward in current facing direction
            self.move_forward(value)
        
        self.navigation_log.append(f"Direct: {instruction} -> {self.get_status()}")
    
    def execute_instruction_waypoint(self, instruction: NavigationInstruction) -> None:
        """
        Execute instruction using waypoint movement (Part 2 rules).
        
        Args:
            instruction: Instruction to execute
        """
        action = instruction.action
        value = instruction.value
        
        if action in [Action.NORTH, Action.SOUTH, Action.EAST, Action.WEST]:
            # Move waypoint in cardinal direction
            direction = Direction(action.value)
            self.waypoint.move(direction, value)
            
        elif action in [Action.LEFT, Action.RIGHT]:
            # Rotate waypoint around ship
            turn_direction = Turn(action.value)
            self.waypoint.rotate(turn_direction, value)
            
        elif action == Action.FORWARD:
            # Move ship toward waypoint multiple times
            self.move_toward_waypoint(value)
        
        self.navigation_log.append(f"Waypoint: {instruction} -> {self.get_status()}")
    
    def get_manhattan_distance(self) -> int:
        """Get Manhattan distance from starting position."""
        return self.position.manhattan_distance_from_origin()
    
    def get_status(self) -> str:
        """Get current ship status."""
        return f"Ship at {self.position}, facing {self.facing.value}, {self.waypoint}"
    
    def get_analysis(self) -> Dict[str, Any]:
        """Get comprehensive analysis of navigation."""
        return {
            'final_position': (self.position.x, self.position.y),
            'manhattan_distance': self.get_manhattan_distance(),
            'facing_direction': self.facing.value,
            'waypoint_position': (self.waypoint.position.x, self.waypoint.position.y),
            'total_instructions': len(self.navigation_log),
            'position_description': self.get_position_description()
        }
    
    def get_position_description(self) -> str:
        """Get human-readable position description."""
        x_desc = f"{abs(self.position.x)} {'east' if self.position.x >= 0 else 'west'}"
        y_desc = f"{abs(self.position.y)} {'north' if self.position.y >= 0 else 'south'}"
        return f"{x_desc}, {y_desc} of starting position"


class NavigationSystem:
    """Manages navigation instruction parsing and execution."""
    
    def __init__(self, instructions_data: str):
        """
        Initialize navigation system with instruction data.
        
        Args:
            instructions_data: Raw instruction data
        """
        self.instructions = self._parse_instructions(instructions_data)
        self.ship = Ship()
    
    def _parse_instructions(self, data: str) -> List[NavigationInstruction]:
        """
        Parse navigation instructions from input data.
        
        Args:
            data: Raw instruction data
            
        Returns:
            List of NavigationInstruction objects
        """
        instructions = []
        
        for line in data.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
                
            action_char = line[0]
            value = int(line[1:])
            
            try:
                action = Action(action_char)
                instructions.append(NavigationInstruction(action, value))
            except ValueError:
                raise ValueError(f"Invalid navigation instruction: {line}")
        
        return instructions
    
    def navigate_direct(self) -> int:
        """
        Execute navigation using direct ship movement rules.
        
        Returns:
            Manhattan distance from origin
        """
        self.ship.reset()
        
        for instruction in self.instructions:
            self.ship.execute_instruction_direct(instruction)
        
        return self.ship.get_manhattan_distance()
    
    def navigate_waypoint(self) -> int:
        """
        Execute navigation using waypoint movement rules.
        
        Returns:
            Manhattan distance from origin
        """
        self.ship.reset()
        
        for instruction in self.instructions:
            self.ship.execute_instruction_waypoint(instruction)
        
        return self.ship.get_manhattan_distance()
    
    def get_instruction_summary(self) -> Dict[str, Any]:
        """Get summary of navigation instructions."""
        action_counts = {}
        total_distance = 0
        total_turns = 0
        
        for instruction in self.instructions:
            action = instruction.action.value
            action_counts[action] = action_counts.get(action, 0) + 1
            
            if action == 'F':
                total_distance += instruction.value
            elif action in ['L', 'R']:
                total_turns += instruction.value
        
        return {
            'total_instructions': len(self.instructions),
            'action_counts': action_counts,
            'total_forward_distance': total_distance,
            'total_turn_degrees': total_turns
        }


class Day12Solution(AdventSolution):
    """Solution for Advent of Code 2020 Day 12: Rain Risk."""
    
    def __init__(self):
        super().__init__(year=2020, day=12, title="Rain Risk")
    
    def part1(self, input_data: str) -> Any:
        """
        Solve part 1: Direct ship movement.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Manhattan distance after navigation
        """
        navigation_system = NavigationSystem(input_data)
        return navigation_system.navigate_direct()
    
    def part2(self, input_data: str) -> Any:
        """
        Solve part 2: Waypoint-based movement.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Manhattan distance after navigation
        """
        navigation_system = NavigationSystem(input_data)
        return navigation_system.navigate_waypoint()
    
    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Provide comprehensive analysis of the navigation system.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis results for both navigation methods
        """
        navigation_system = NavigationSystem(input_data)
        
        # Analyze direct navigation
        direct_result = navigation_system.navigate_direct()
        direct_analysis = navigation_system.ship.get_analysis()
        
        # Analyze waypoint navigation
        waypoint_result = navigation_system.navigate_waypoint()
        waypoint_analysis = navigation_system.ship.get_analysis()
        
        # Get instruction summary
        instruction_summary = navigation_system.get_instruction_summary()
        
        return {
            'instructions': instruction_summary,
            'direct_navigation': {
                'result': direct_result,
                'analysis': direct_analysis,
                'method': 'ship_movement'
            },
            'waypoint_navigation': {
                'result': waypoint_result,
                'analysis': waypoint_analysis,
                'method': 'waypoint_relative'
            },
            'comparison': {
                'distance_difference': abs(direct_result - waypoint_result),
                'waypoint_more_efficient': waypoint_result < direct_result,
                'efficiency_ratio': direct_result / waypoint_result if waypoint_result != 0 else float('inf')
            }
        }




def main():
    """Main execution function."""
    solution = Day12Solution()
    solution.main()


if __name__ == "__main__":
    main()