#!/usr/bin/env python3
"""
Advent of Code 2019 Day 13: Care Package (OPTIMIZED)

High-performance arcade game simulation with major optimizations:
- Synchronous Intcode execution (no threading overhead)
- Optimized data structures (tuples instead of objects)
- Simplified AI strategy (follow-the-ball)
- Efficient game state management
- Eliminated sleep() calls and unnecessary complexity

Performance target: <1 second total execution time
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import Dict, Tuple, List, Any, Optional

# Tile constants - simple integers for performance
EMPTY, WALL, BLOCK, PADDLE, BALL = 0, 1, 2, 3, 4

# Joystick input constants
LEFT, NEUTRAL, RIGHT = -1, 0, 1


class OptimizedIntcode:
    """
    Optimized Intcode interpreter without threading overhead.
    
    Reusing the same optimized implementation from day11.py.
    """
    
    def __init__(self, program_str: str):
        """Initialize with minimal memory allocation."""
        self.memory = [int(x) for x in program_str.strip().split(',')]
        # Extend memory - only as much as needed
        self.memory.extend([0] * 10000)
        
        self.pc = 0
        self.relative_base = 0
        self.inputs = []
        self.input_ptr = 0
        self.halted = False
        self.needs_input = False
    
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
        self.needs_input = False
    
    def run_until_output_or_halt_or_input(self) -> Tuple[bool, int]:
        """
        Run until output is produced, input needed, or program halts.
        
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
                    self.needs_input = True
                    return False, 0
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


class OptimizedArcadeGame:
    """
    High-performance arcade game with optimized data structures.
    
    Uses tuples for positions and simple integers for everything else.
    """
    
    def __init__(self, program: str, free_play: bool = False):
        """Initialize game with minimal data structures."""
        self.program = program
        self.free_play = free_play
        self.grid: Dict[Tuple[int, int], int] = {}
        self.score = 0
        self.ball_x = 0
        self.ball_y = 0
        self.paddle_x = 0
        self.paddle_y = 0
    
    def count_blocks(self) -> int:
        """Count block tiles efficiently."""
        return sum(1 for tile in self.grid.values() if tile == BLOCK)
    
    def simple_ai_input(self) -> int:
        """
        Simple AI: just follow the ball horizontally.
        
        This is much more efficient than complex prediction algorithms.
        """
        if self.paddle_x < self.ball_x:
            return RIGHT
        elif self.paddle_x > self.ball_x:
            return LEFT
        else:
            return NEUTRAL
    
    def run_game_screen_only(self) -> int:
        """Run game just to build initial screen (Part 1)."""
        computer = OptimizedIntcode(self.program)
        
        # Collect all initial outputs
        outputs = []
        while True:
            has_output, output = computer.run_until_output_or_halt_or_input()
            if not has_output:
                break
            outputs.append(output)
        
        # Process outputs in triplets
        for i in range(0, len(outputs), 3):
            if i + 2 < len(outputs):
                x, y, tile_id = outputs[i], outputs[i+1], outputs[i+2]
                self.grid[(x, y)] = tile_id
        
        return self.count_blocks()
    
    def run_game_to_completion(self) -> int:
        """Run complete game with AI player (Part 2)."""
        computer = OptimizedIntcode(self.program)
        
        if self.free_play:
            computer.memory[0] = 2  # Enable free play
        
        while not computer.halted:
            # Run until we need input or halt
            outputs = []
            while True:
                has_output, output = computer.run_until_output_or_halt_or_input()
                if has_output:
                    outputs.append(output)
                else:
                    break  # Either halted or needs input
            
            # Process outputs in triplets
            for i in range(0, len(outputs), 3):
                if i + 2 < len(outputs):
                    x, y, tile_id = outputs[i], outputs[i+1], outputs[i+2]
                    
                    if x == -1 and y == 0:
                        # Score update
                        self.score = tile_id
                    else:
                        # Tile update
                        self.grid[(x, y)] = tile_id
                        
                        # Track ball and paddle positions
                        if tile_id == BALL:
                            self.ball_x, self.ball_y = x, y
                        elif tile_id == PADDLE:
                            self.paddle_x, self.paddle_y = x, y
            
            # Provide AI input if needed
            if computer.needs_input and not computer.halted:
                ai_input = self.simple_ai_input()
                computer.add_input(ai_input)
            
            # Check win condition
            if self.count_blocks() == 0:
                break
        
        return self.score


class Day13OptimizedSolution(AdventSolution):
    """Optimized solution for Advent of Code 2019 Day 13."""
    
    def __init__(self):
        super().__init__(year=2019, day=13, title="Care Package (Optimized)")
        
    def part1(self, input_data: str) -> Any:
        """Part 1: Count block tiles on initial screen."""
        game = OptimizedArcadeGame(input_data.strip())
        return game.run_game_screen_only()
    
    def part2(self, input_data: str) -> Any:
        """Part 2: Play game to completion and get final score."""
        game = OptimizedArcadeGame(input_data.strip(), free_play=True)
        return game.run_game_to_completion()


# Legacy compatibility functions for test runner
def part1(filename: str) -> Any:
    """Legacy function for part 1."""
    with open(filename, 'r') as f:
        input_data = f.read()
    
    solution = Day13OptimizedSolution()
    return solution.part1(input_data)


def part2(filename: str) -> Any:
    """Legacy function for part 2."""
    with open(filename, 'r') as f:
        input_data = f.read()
    
    solution = Day13OptimizedSolution()
    return solution.part2(input_data)


def main():
    """Main function with dual compatibility."""
    if len(sys.argv) > 1 or '--test' in sys.argv or '--time' in sys.argv:
        # New AdventSolution mode
        solution = Day13OptimizedSolution()
        solution.main()
    else:
        # Legacy mode for compatibility
        print(part1("day13_input.txt"))
        print(part2("day13_input.txt"))


if __name__ == "__main__":
    main()