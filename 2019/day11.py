#!/usr/bin/env python3
"""
Advent of Code 2019 Day 11: Space Police
Enhanced solution with object-oriented design and comprehensive analysis.
"""

import sys
import os
from typing import Dict, Tuple, List, Set, Optional
from enum import Enum
from dataclasses import dataclass

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.advent_base import AdventSolution
from intcode import Intcode


class Color(Enum):
    """Paint colors for the robot."""
    BLACK = 0
    WHITE = 1


class Direction(Enum):
    """Cardinal directions for robot movement."""
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
    def turn_left(self) -> 'Direction':
        """Turn 90 degrees counter-clockwise."""
        return Direction((self.value - 1) % 4)
    
    def turn_right(self) -> 'Direction':
        """Turn 90 degrees clockwise."""
        return Direction((self.value + 1) % 4)
    
    def get_delta(self) -> Tuple[int, int]:
        """Get the (dx, dy) movement vector for this direction."""
        deltas = {
            Direction.UP: (0, 1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, -1),
            Direction.LEFT: (-1, 0)
        }
        return deltas[self]


@dataclass
class Position:
    """Represents a 2D position."""
    x: int
    y: int
    
    def move(self, direction: Direction) -> 'Position':
        """Create a new position by moving in the given direction."""
        dx, dy = direction.get_delta()
        return Position(self.x + dx, self.y + dy)
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))


class PaintingRobot:
    """
    Emergency Hull Painting Robot with advanced navigation and painting capabilities.
    
    The robot operates on an infinite 2D grid, painting panels according to
    instructions from its Intcode brain. It tracks its position, direction,
    and maintains a complete record of all painted panels.
    """
    
    def __init__(self, starting_color: Color = Color.BLACK):
        """
        Initialize the robot at the origin.
        
        Args:
            starting_color: Initial color of the starting panel
        """
        self.position = Position(0, 0)
        self.direction = Direction.UP
        self.panels: Dict[Position, Color] = {self.position: starting_color}
        self.paint_history: List[Tuple[Position, Color]] = []
        
    def get_current_color(self) -> Color:
        """Get the color of the current panel."""
        return self.panels.get(self.position, Color.BLACK)
    
    def paint_current_panel(self, color: Color) -> None:
        """Paint the current panel with the specified color."""
        self.panels[self.position] = color
        self.paint_history.append((self.position, color))
    
    def turn_and_move(self, turn_direction: int) -> None:
        """
        Turn and move forward one panel.
        
        Args:
            turn_direction: 0 for left turn, 1 for right turn
        """
        if turn_direction == 0:
            self.direction = self.direction.turn_left()
        else:
            self.direction = self.direction.turn_right()
        
        self.position = self.position.move(self.direction)
    
    def run_painting_program(self, program: str) -> int:
        """
        Execute the painting program using Intcode brain.
        
        Args:
            program: Intcode program string
            
        Returns:
            Number of panels painted at least once
        """
        # Create and configure Intcode computer
        brain = Intcode(program)
        brain.start()
        
        # Provide initial input (current panel color)
        brain.add_input(self.get_current_color().value)
        
        while not brain.halted:
            # Wait for two outputs: paint color and turn direction
            brain.wait_for_output()
            if brain.halted:
                break
                
            paint_color = brain.outputs.pop(0)
            
            brain.wait_for_output()
            if brain.halted:
                break
                
            turn_direction = brain.outputs.pop(0)
            
            # Execute robot actions
            self.paint_current_panel(Color(paint_color))
            self.turn_and_move(turn_direction)
            
            # Provide next input
            brain.add_input(self.get_current_color().value)
        
        brain.join()  # Wait for thread completion
        return len(self.panels)
    
    def get_painted_bounds(self) -> Tuple[int, int, int, int]:
        """Get the bounding rectangle of all painted panels."""
        if not self.panels:
            return 0, 0, 0, 0
        
        positions = list(self.panels.keys())
        min_x = min(pos.x for pos in positions)
        max_x = max(pos.x for pos in positions)
        min_y = min(pos.y for pos in positions)
        max_y = max(pos.y for pos in positions)
        
        return min_x, max_x, min_y, max_y
    
    def render_painting(self) -> str:
        """
        Render the painted panels as ASCII art.
        
        Returns:
            String representation of the painted panels
        """
        if not self.panels:
            return ""
        
        min_x, max_x, min_y, max_y = self.get_painted_bounds()
        
        lines = []
        # Render from top to bottom (y decreasing)
        for y in range(max_y, min_y - 1, -1):
            line = ""
            for x in range(min_x, max_x + 1):
                pos = Position(x, y)
                color = self.panels.get(pos, Color.BLACK)
                line += "█" if color == Color.WHITE else " "
            lines.append(line.rstrip())
        
        # Remove trailing empty lines
        while lines and not lines[-1].strip():
            lines.pop()
        
        return "\n".join(lines)
    
    def parse_letters_from_art(self) -> str:
        """
        Parse ASCII art into letters using shared utility.
        
        Returns:
            String of recognized letters
        """
        from utils import parse_ascii_letters
        art = self.render_painting()
        return parse_ascii_letters(art, 'thin')
    
    def get_analysis(self) -> Dict[str, any]:
        """
        Analyze the robot's painting session.
        
        Returns:
            Dictionary with comprehensive analysis data
        """
        white_panels = sum(1 for color in self.panels.values() if color == Color.WHITE)
        black_panels = len(self.panels) - white_panels
        
        # Calculate painting area
        min_x, max_x, min_y, max_y = self.get_painted_bounds()
        total_area = (max_x - min_x + 1) * (max_y - min_y + 1)
        coverage_ratio = len(self.panels) / total_area if total_area > 0 else 0
        
        # Analyze paint history
        paint_operations = len(self.paint_history)
        panels_repainted = paint_operations - len(self.panels)
        
        return {
            'total_panels_painted': len(self.panels),
            'white_panels': white_panels,
            'black_panels': black_panels,
            'paint_operations': paint_operations,
            'panels_repainted': panels_repainted,
            'painting_bounds': (min_x, max_x, min_y, max_y),
            'painting_dimensions': (max_x - min_x + 1, max_y - min_y + 1),
            'total_area': total_area,
            'coverage_ratio': coverage_ratio,
            'final_position': (self.position.x, self.position.y),
            'final_direction': self.direction.name
        }


class Day11Solution(AdventSolution):
    """Enhanced solution for Advent of Code 2019 Day 11: Space Police."""
    
    def __init__(self):
        super().__init__(year=2019, day=11, title="Space Police")
    
    def part1(self, input_data: str) -> int:
        """
        Count panels painted when starting on a black panel.
        
        Args:
            input_data: Intcode program as string
            
        Returns:
            Number of panels painted at least once
        """
        program = input_data.strip()
        robot = PaintingRobot(starting_color=Color.BLACK)
        return robot.run_painting_program(program)
    
    def part2(self, input_data: str) -> str:
        """
        Generate registration identifier when starting on a white panel.
        
        Args:
            input_data: Intcode program as string
            
        Returns:
            Parsed letters from the painted registration
        """
        program = input_data.strip()
        robot = PaintingRobot(starting_color=Color.WHITE)
        robot.run_painting_program(program)
        return robot.parse_letters_from_art()
    
    def analyze(self, input_data: str) -> None:
        """
        Provide comprehensive analysis of both painting scenarios.
        
        Args:
            input_data: Intcode program as string
        """
        program = input_data.strip()
        
        print("=== Painting Analysis ===\n")
        
        # Analyze Part 1 scenario
        print("Part 1 Analysis (Starting on Black Panel):")
        robot1 = PaintingRobot(starting_color=Color.BLACK)
        panels1 = robot1.run_painting_program(program)
        analysis1 = robot1.get_analysis()
        
        for key, value in analysis1.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        print(f"\nPart 1 Result: {panels1} panels painted")
        
        # Analyze Part 2 scenario
        print("\nPart 2 Analysis (Starting on White Panel):")
        robot2 = PaintingRobot(starting_color=Color.WHITE)
        robot2.run_painting_program(program)
        analysis2 = robot2.get_analysis()
        
        for key, value in analysis2.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        print(f"\nPart 2 Registration Identifier:")
        print(robot2.render_painting())
        
        # Comparison
        print(f"\nComparison:")
        print(f"  Additional panels painted in Part 2: {analysis2['total_panels_painted'] - analysis1['total_panels_painted']}")
        print(f"  Coverage difference: {analysis2['coverage_ratio'] - analysis1['coverage_ratio']:.2%}")


# Legacy functions for test runner compatibility
def part1(input_data: str = None) -> int:
    """Legacy part1 function for test runner compatibility."""
    if input_data is None:
        # Auto-load input file
        try:
            with open('/home/mike/src/advent_of_code/2019/day11_input.txt', 'r') as f:
                input_data = f.read()
        except FileNotFoundError:
            # Fallback to embedded program
            input_data = "3,8,1005,8,345,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,102,1,8,28,1006,0,94,2,106,5,10,1,1109,12,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,62,1,103,6,10,1,108,12,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,92,2,104,18,10,2,1109,2,10,2,1007,5,10,1,7,4,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,129,2,1004,15,10,2,1103,15,10,2,1009,6,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,164,2,1109,14,10,1,1107,18,10,1,1109,13,10,1,1107,11,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,201,2,104,20,10,1,107,8,10,1,1007,5,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,236,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,257,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,279,1,107,0,10,1,107,16,10,1006,0,24,1,101,3,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,316,2,1108,15,10,2,4,11,10,101,1,9,9,1007,9,934,10,1005,10,15,99,109,667,104,0,104,1,21101,0,936995730328,1,21102,362,1,0,1105,1,466,21102,1,838210728716,1,21101,373,0,0,1105,1,466,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,235350789351,1,21101,0,420,0,1105,1,466,21102,29195603035,1,1,21102,1,431,0,1105,1,466,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,825016079204,1,21101,0,454,0,1105,1,466,21101,837896786700,0,1,21102,1,465,0,1106,0,466,99,109,2,21201,-1,0,1,21101,0,40,2,21102,1,497,3,21101,0,487,0,1105,1,530,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,492,493,508,4,0,1001,492,1,492,108,4,492,10,1006,10,524,1101,0,0,492,109,-2,2105,1,0,0,109,4,2102,1,-1,529,1207,-3,0,10,1006,10,547,21102,1,0,-3,21201,-3,0,1,22102,1,-2,2,21101,1,0,3,21102,1,566,0,1105,1,571,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,594,2207,-4,-2,10,1006,10,594,21201,-4,0,-4,1106,0,662,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21101,613,0,0,1105,1,571,22101,0,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,632,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,654,22101,0,-1,1,21102,654,1,0,105,1,529,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0"
    
    solution = Day11Solution()
    return solution.part1(input_data)


def part2(input_data: str = None) -> str:
    """Legacy part2 function for test runner compatibility."""
    if input_data is None:
        # Auto-load input file
        try:
            with open('/home/mike/src/advent_of_code/2019/day11_input.txt', 'r') as f:
                input_data = f.read()
        except FileNotFoundError:
            # Fallback to embedded program
            input_data = "3,8,1005,8,345,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,102,1,8,28,1006,0,94,2,106,5,10,1,1109,12,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,62,1,103,6,10,1,108,12,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,92,2,104,18,10,2,1109,2,10,2,1007,5,10,1,7,4,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,129,2,1004,15,10,2,1103,15,10,2,1009,6,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,164,2,1109,14,10,1,1107,18,10,1,1109,13,10,1,1107,11,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,201,2,104,20,10,1,107,8,10,1,1007,5,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,236,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,257,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,279,1,107,0,10,1,107,16,10,1006,0,24,1,101,3,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,316,2,1108,15,10,2,4,11,10,101,1,9,9,1007,9,934,10,1005,10,15,99,109,667,104,0,104,1,21101,0,936995730328,1,21102,362,1,0,1105,1,466,21102,1,838210728716,1,21101,373,0,0,1105,1,466,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,235350789351,1,21101,0,420,0,1105,1,466,21102,29195603035,1,1,21102,1,431,0,1105,1,466,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,825016079204,1,21101,0,454,0,1105,1,466,21101,837896786700,0,1,21102,1,465,0,1106,0,466,99,109,2,21201,-1,0,1,21101,0,40,2,21102,1,497,3,21101,0,487,0,1105,1,530,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,492,493,508,4,0,1001,492,1,492,108,4,492,10,1006,10,524,1101,0,0,492,109,-2,2105,1,0,0,109,4,2102,1,-1,529,1207,-3,0,10,1006,10,547,21102,1,0,-3,21201,-3,0,1,22102,1,-2,2,21101,1,0,3,21102,1,566,0,1105,1,571,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,594,2207,-4,-2,10,1006,10,594,21201,-4,0,-4,1106,0,662,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21101,613,0,0,1105,1,571,22101,0,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,632,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,654,22101,0,-1,1,21102,654,1,0,105,1,529,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0"
    
    solution = Day11Solution()
    return solution.part2(input_data)


if __name__ == "__main__":
    solution = Day11Solution()
    solution.main()