#!/usr/bin/env python3
"""
Advent of Code 2019 Day 11: Space Police (OPTIMIZED)

High-performance robot painting simulation with major optimizations:
- Synchronous Intcode execution (no threading overhead)
- Optimized data structures (tuples instead of objects)
- Simplified robot state management
- Efficient painting and movement operations

Performance target: <1 second total execution time
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import Dict, Tuple, List, Any

# Direction constants - simple integers for performance
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

# Direction deltas - precomputed for speed
DELTAS = {
    UP: (0, 1),
    RIGHT: (1, 0), 
    DOWN: (0, -1),
    LEFT: (-1, 0)
}

# Color constants
BLACK, WHITE = 0, 1


class OptimizedIntcode:
    """
    Optimized Intcode interpreter without threading overhead.
    
    Synchronous execution with simplified I/O handling for maximum performance.
    """
    
    def __init__(self, program_str: str):
        """Initialize with minimal memory allocation."""
        self.memory = [int(x) for x in program_str.strip().split(',')]
        # Extend memory - but only as much as needed
        self.memory.extend([0] * 10000)  # Much smaller than original 25000
        
        self.pc = 0
        self.relative_base = 0
        self.inputs = []
        self.input_ptr = 0
        self.halted = False
    
    def get_param(self, mode: int, offset: int) -> int:
        """Get parameter value based on mode."""
        if mode == 0:  # Position mode
            return self.memory[self.memory[self.pc + offset]]
        elif mode == 1:  # Immediate mode
            return self.memory[self.pc + offset]
        elif mode == 2:  # Relative mode
            return self.memory[self.relative_base + self.memory[self.pc + offset]]
        else:
            raise ValueError(f"Invalid parameter mode: {mode}")
    
    def get_address(self, mode: int, offset: int) -> int:
        """Get memory address for writing."""
        if mode == 0:  # Position mode
            return self.memory[self.pc + offset]
        elif mode == 2:  # Relative mode
            return self.relative_base + self.memory[self.pc + offset]
        else:
            raise ValueError(f"Invalid address mode: {mode}")
    
    def add_input(self, value: int) -> None:
        """Add input value."""
        self.inputs.append(value)
    
    def run_until_output_or_halt(self) -> Tuple[bool, int]:
        """
        Run until output is produced or program halts.
        
        Returns:
            (has_output, output_value)
        """
        while not self.halted:
            instruction = self.memory[self.pc]
            opcode = instruction % 100
            mode1 = (instruction // 100) % 10
            mode2 = (instruction // 1000) % 10
            mode3 = (instruction // 10000) % 10
            
            if opcode == 99:  # Halt
                self.halted = True
                return False, 0
            
            elif opcode == 1:  # Add
                val1 = self.get_param(mode1, 1)
                val2 = self.get_param(mode2, 2)
                addr = self.get_address(mode3, 3)
                self.memory[addr] = val1 + val2
                self.pc += 4
                
            elif opcode == 2:  # Multiply
                val1 = self.get_param(mode1, 1)
                val2 = self.get_param(mode2, 2)
                addr = self.get_address(mode3, 3)
                self.memory[addr] = val1 * val2
                self.pc += 4
                
            elif opcode == 3:  # Input
                if self.input_ptr >= len(self.inputs):
                    raise RuntimeError("No input available")
                addr = self.get_address(mode1, 1)
                self.memory[addr] = self.inputs[self.input_ptr]
                self.input_ptr += 1
                self.pc += 2
                
            elif opcode == 4:  # Output
                output = self.get_param(mode1, 1)
                self.pc += 2
                return True, output
                
            elif opcode == 5:  # Jump-if-true
                val1 = self.get_param(mode1, 1)
                val2 = self.get_param(mode2, 2)
                if val1 != 0:
                    self.pc = val2
                else:
                    self.pc += 3
                    
            elif opcode == 6:  # Jump-if-false
                val1 = self.get_param(mode1, 1)
                val2 = self.get_param(mode2, 2)
                if val1 == 0:
                    self.pc = val2
                else:
                    self.pc += 3
                    
            elif opcode == 7:  # Less than
                val1 = self.get_param(mode1, 1)
                val2 = self.get_param(mode2, 2)
                addr = self.get_address(mode3, 3)
                self.memory[addr] = 1 if val1 < val2 else 0
                self.pc += 4
                
            elif opcode == 8:  # Equals
                val1 = self.get_param(mode1, 1)
                val2 = self.get_param(mode2, 2)
                addr = self.get_address(mode3, 3)
                self.memory[addr] = 1 if val1 == val2 else 0
                self.pc += 4
                
            elif opcode == 9:  # Adjust relative base
                val1 = self.get_param(mode1, 1)
                self.relative_base += val1
                self.pc += 2
                
            else:
                raise ValueError(f"Invalid opcode: {opcode}")
        
        return False, 0


class OptimizedPaintingRobot:
    """
    High-performance painting robot with optimized data structures.
    
    Uses tuples for positions and simple integers for everything else.
    """
    
    def __init__(self, starting_color: int = BLACK):
        """Initialize robot with minimal data structures."""
        self.x = 0
        self.y = 0
        self.direction = UP
        self.panels: Dict[Tuple[int, int], int] = {(0, 0): starting_color}
    
    def get_current_color(self) -> int:
        """Get current panel color."""
        return self.panels.get((self.x, self.y), BLACK)
    
    def paint_panel(self, color: int) -> None:
        """Paint current panel."""
        self.panels[(self.x, self.y)] = color
    
    def turn_and_move(self, turn_direction: int) -> None:
        """Turn and move forward."""
        # Turn
        if turn_direction == 0:  # Turn left
            self.direction = (self.direction - 1) % 4
        else:  # Turn right
            self.direction = (self.direction + 1) % 4
        
        # Move
        dx, dy = DELTAS[self.direction]
        self.x += dx
        self.y += dy
    
    def run_painting_program(self, program: str) -> int:
        """
        Execute painting program with optimized Intcode.
        
        Returns:
            Number of panels painted at least once
        """
        computer = OptimizedIntcode(program)
        computer.add_input(self.get_current_color())
        
        while not computer.halted:
            # Get paint color
            has_output, paint_color = computer.run_until_output_or_halt()
            if not has_output:
                break
            
            # Get turn direction
            has_output, turn_direction = computer.run_until_output_or_halt()
            if not has_output:
                break
            
            # Execute robot actions
            self.paint_panel(paint_color)
            self.turn_and_move(turn_direction)
            
            # Provide next input
            computer.add_input(self.get_current_color())
        
        return len(self.panels)
    
    def render_painting(self) -> str:
        """Render painted panels as ASCII art."""
        if not self.panels:
            return ""
        
        # Get bounds
        positions = list(self.panels.keys())
        min_x = min(x for x, y in positions)
        max_x = max(x for x, y in positions)
        min_y = min(y for x, y in positions)
        max_y = max(y for x, y in positions)
        
        lines = []
        # Render from top to bottom
        for y in range(max_y, min_y - 1, -1):
            line = ""
            for x in range(min_x, max_x + 1):
                color = self.panels.get((x, y), BLACK)
                line += "█" if color == WHITE else " "
            lines.append(line.rstrip())
        
        # Remove trailing empty lines
        while lines and not lines[-1].strip():
            lines.pop()
        
        return "\n".join(lines)


class Day11OptimizedSolution(AdventSolution):
    """Optimized solution for Advent of Code 2019 Day 11."""
    
    def __init__(self):
        super().__init__(year=2019, day=11, title="Space Police (Optimized)")
        
    def part1(self, input_data: str) -> Any:
        """Part 1: Count panels painted starting on black panel."""
        robot = OptimizedPaintingRobot(starting_color=BLACK)
        return robot.run_painting_program(input_data.strip())
    
    def part2(self, input_data: str) -> Any:
        """Part 2: Paint registration identifier starting on white panel."""
        robot = OptimizedPaintingRobot(starting_color=WHITE)
        robot.run_painting_program(input_data.strip())
        
        # Parse the painted output
        painting = robot.render_painting()
        
        # Try to parse letters using ASCII art utility
        try:
            from utils import parse_ascii_letters
            return parse_ascii_letters(painting)
        except (ImportError, Exception):
            # Fallback: return the raw painting
            return painting

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        print("ℹ️ No examples provided for Day 11, skipping validation")
        #print("✅ All Day 11    validation tests passed!")
        return True


def main():
    """Main execution function."""
    solution = Day11OptimizedSolution()
    solution.main()


if __name__ == "__main__":
    main()