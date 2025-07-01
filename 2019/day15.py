#!/usr/bin/env python3
"""
Advent of Code 2019 Day 15: Oxygen System

Enhanced solution using the AdventSolution base class for maze exploration
with Intcode robot control and BFS pathfinding algorithms.
"""

import sys
from pathlib import Path
from collections import deque
from typing import Dict, Tuple, Set, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Add utils to path for enhanced base class
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution

class Direction(Enum):
    """Movement directions for the repair droid."""
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

class CellType(Enum):
    """Types of cells in the maze."""
    WALL = 0
    EMPTY = 1
    OXYGEN = 2

@dataclass
class Position:
    """Represents a 2D position in the maze."""
    x: int
    y: int
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def move(self, direction: Direction) -> 'Position':
        """Move in the specified direction and return new position."""
        moves = {
            Direction.NORTH: (0, 1),
            Direction.SOUTH: (0, -1),
            Direction.WEST: (-1, 0),
            Direction.EAST: (1, 0)
        }
        dx, dy = moves[direction]
        return Position(self.x + dx, self.y + dy)

class IntcodeVM:
    """
    Simplified Intcode virtual machine optimized for repair droid control.
    Implements all necessary opcodes with memory extension and relative base support.
    """
    
    def __init__(self, program: str):
        self.original_program = [int(x) for x in program.split(',')]
        self.reset()
    
    def reset(self):
        """Reset the VM to initial state."""
        self.memory = self.original_program.copy()
        # Extend memory for safety
        self.memory.extend([0] * 10000)
        self.pc = 0  # Program counter
        self.relative_base = 0
        self.inputs = []
        self.outputs = []
        self.halted = False
        self.waiting_for_input = False
    
    def add_input(self, value: int):
        """Add input value to the input queue."""
        self.inputs.append(value)
        self.waiting_for_input = False
    
    def get_parameter_value(self, offset: int, mode: int) -> int:
        """Get parameter value based on addressing mode."""
        if mode == 0:  # Position mode
            return self.memory[self.memory[self.pc + offset]]
        elif mode == 1:  # Immediate mode
            return self.memory[self.pc + offset]
        elif mode == 2:  # Relative mode
            return self.memory[self.relative_base + self.memory[self.pc + offset]]
        else:
            raise ValueError(f"Unknown parameter mode: {mode}")
    
    def get_write_address(self, offset: int, mode: int) -> int:
        """Get write address based on addressing mode."""
        if mode == 0:  # Position mode
            return self.memory[self.pc + offset]
        elif mode == 2:  # Relative mode
            return self.relative_base + self.memory[self.pc + offset]
        else:
            raise ValueError(f"Invalid write mode: {mode}")
    
    def run_until_output_or_halt(self) -> str:
        """Run until output is produced, input is needed, or program halts."""
        while not self.halted and not self.waiting_for_input:
            instruction = self.memory[self.pc]
            opcode = instruction % 100
            mode1 = (instruction // 100) % 10
            mode2 = (instruction // 1000) % 10
            mode3 = (instruction // 10000) % 10
            
            if opcode == 99:  # Halt
                self.halted = True
                return "halt"
            
            elif opcode == 1:  # Add
                val1 = self.get_parameter_value(1, mode1)
                val2 = self.get_parameter_value(2, mode2)
                addr = self.get_write_address(3, mode3)
                self.memory[addr] = val1 + val2
                self.pc += 4
            
            elif opcode == 2:  # Multiply
                val1 = self.get_parameter_value(1, mode1)
                val2 = self.get_parameter_value(2, mode2)
                addr = self.get_write_address(3, mode3)
                self.memory[addr] = val1 * val2
                self.pc += 4
            
            elif opcode == 3:  # Input
                if not self.inputs:
                    self.waiting_for_input = True
                    return "input"
                addr = self.get_write_address(1, mode1)
                self.memory[addr] = self.inputs.pop(0)
                self.pc += 2
            
            elif opcode == 4:  # Output
                val = self.get_parameter_value(1, mode1)
                self.outputs.append(val)
                self.pc += 2
                return "output"
            
            elif opcode == 5:  # Jump-if-true
                val = self.get_parameter_value(1, mode1)
                target = self.get_parameter_value(2, mode2)
                if val != 0:
                    self.pc = target
                else:
                    self.pc += 3
            
            elif opcode == 6:  # Jump-if-false
                val = self.get_parameter_value(1, mode1)
                target = self.get_parameter_value(2, mode2)
                if val == 0:
                    self.pc = target
                else:
                    self.pc += 3
            
            elif opcode == 7:  # Less than
                val1 = self.get_parameter_value(1, mode1)
                val2 = self.get_parameter_value(2, mode2)
                addr = self.get_write_address(3, mode3)
                self.memory[addr] = 1 if val1 < val2 else 0
                self.pc += 4
            
            elif opcode == 8:  # Equals
                val1 = self.get_parameter_value(1, mode1)
                val2 = self.get_parameter_value(2, mode2)
                addr = self.get_write_address(3, mode3)
                self.memory[addr] = 1 if val1 == val2 else 0
                self.pc += 4
            
            elif opcode == 9:  # Adjust relative base
                val = self.get_parameter_value(1, mode1)
                self.relative_base += val
                self.pc += 2
            
            else:
                raise ValueError(f"Unknown opcode: {opcode}")
        
        if self.waiting_for_input:
            return "input"
        return "halt"

class MazeExplorer:
    """
    Domain class for maze exploration using an Intcode-controlled repair droid.
    Handles maze discovery, pathfinding, and oxygen diffusion simulation.
    """
    
    def __init__(self, program: str):
        self.vm = IntcodeVM(program)
        self.position = Position(0, 0)
        self.maze: Dict[Position, CellType] = {Position(0, 0): CellType.EMPTY}
        self.oxygen_location: Optional[Position] = None
        
    def move_droid(self, direction: Direction) -> CellType:
        """Move the droid in the given direction and return the result."""
        self.vm.add_input(direction.value)
        self.vm.run_until_output_or_halt()
        return CellType(self.vm.outputs[-1])
    
    def explore_complete_maze(self) -> Dict[Position, CellType]:
        """
        Explore the entire maze using depth-first search.
        Returns the complete maze map.
        """
        def dfs(current_pos: Position, visited: Set[Position]):
            visited.add(current_pos)
            
            for direction in Direction:
                next_pos = current_pos.move(direction)
                
                if next_pos not in self.maze:
                    # Try to move in this direction
                    result = self.move_droid(direction)
                    
                    if result == CellType.WALL:
                        self.maze[next_pos] = CellType.WALL
                    else:
                        # Successfully moved to new position
                        self.maze[next_pos] = result
                        self.position = next_pos
                        
                        if result == CellType.OXYGEN:
                            self.oxygen_location = next_pos
                        
                        # Recursively explore from new position
                        if next_pos not in visited:
                            dfs(next_pos, visited)
                        
                        # Move back to previous position
                        opposite_direction = self._get_opposite_direction(direction)
                        self.move_droid(opposite_direction)
                        self.position = current_pos
        
        dfs(self.position, set())
        return self.maze
    
    def _get_opposite_direction(self, direction: Direction) -> Direction:
        """Get the opposite direction for backtracking."""
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST
        }
        return opposites[direction]
    
    def find_shortest_path(self, start: Position, end: Position) -> int:
        """Find the shortest path between two positions using BFS."""
        if start == end:
            return 0
        
        queue = deque([(start, 0)])
        visited = {start}
        
        while queue:
            pos, distance = queue.popleft()
            
            for direction in Direction:
                next_pos = pos.move(direction)
                
                if next_pos == end:
                    return distance + 1
                
                if (next_pos in self.maze and 
                    self.maze[next_pos] != CellType.WALL and 
                    next_pos not in visited):
                    visited.add(next_pos)
                    queue.append((next_pos, distance + 1))
        
        return -1  # No path found
    
    def simulate_oxygen_spread(self) -> int:
        """
        Simulate oxygen spreading from the oxygen system to fill all empty spaces.
        Returns the time required to fill all reachable areas.
        """
        if not self.oxygen_location:
            return -1
        
        max_time = 0
        queue = deque([(self.oxygen_location, 0)])
        visited = {self.oxygen_location}
        
        while queue:
            pos, time = queue.popleft()
            max_time = max(max_time, time)
            
            for direction in Direction:
                next_pos = pos.move(direction)
                
                if (next_pos in self.maze and 
                    self.maze[next_pos] != CellType.WALL and 
                    next_pos not in visited):
                    visited.add(next_pos)
                    queue.append((next_pos, time + 1))
        
        return max_time
    
    def get_maze_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the explored maze."""
        total_cells = len(self.maze)
        wall_count = sum(1 for cell in self.maze.values() if cell == CellType.WALL)
        empty_count = sum(1 for cell in self.maze.values() if cell == CellType.EMPTY)
        oxygen_count = sum(1 for cell in self.maze.values() if cell == CellType.OXYGEN)
        
        # Calculate maze bounds
        positions = list(self.maze.keys())
        min_x = min(pos.x for pos in positions)
        max_x = max(pos.x for pos in positions)
        min_y = min(pos.y for pos in positions)
        max_y = max(pos.y for pos in positions)
        
        return {
            'total_cells': total_cells,
            'wall_count': wall_count,
            'empty_count': empty_count,
            'oxygen_count': oxygen_count,
            'maze_width': max_x - min_x + 1,
            'maze_height': max_y - min_y + 1,
            'oxygen_location': self.oxygen_location,
            'bounds': ((min_x, min_y), (max_x, max_y))
        }

class Day15Solution(AdventSolution):
    """Enhanced solution for Advent of Code 2019 Day 15: Oxygen System."""
    
    def __init__(self):
        super().__init__(2019, 15, "Oxygen System")
        self.explorer: Optional[MazeExplorer] = None
    
    def _get_program(self, input_data: str) -> str:
        """Extract the Intcode program from input data."""
        program = input_data.strip()
        if not program:
            # Fallback to embedded program for compatibility
            program = "3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,101,0,1034,1039,101,0,1036,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,102,1,1034,1039,101,0,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1105,1,124,1001,1034,-1,1039,1008,1036,0,1041,1002,1035,1,1040,1002,1038,1,1043,1001,1037,0,1042,1105,1,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,101,0,1038,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,35,1032,1006,1032,165,1008,1040,33,1032,1006,1032,165,1102,2,1,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1101,1,0,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,27,1044,1105,1,224,1101,0,0,1044,1105,1,224,1006,1044,247,101,0,1039,1034,1002,1040,1,1035,101,0,1041,1036,1001,1043,0,1038,101,0,1042,1037,4,1044,1106,0,0,8,86,20,11,8,18,84,20,96,25,15,28,96,20,74,24,7,5,77,6,77,6,23,74,3,23,93,21,72,23,1,57,87,10,17,9,23,48,16,9,32,11,62,73,5,70,2,10,77,23,16,76,24,28,13,46,92,26,15,10,87,13,28,54,10,50,4,16,47,75,24,55,4,99,92,17,66,24,7,13,33,43,21,65,24,4,74,40,8,28,25,5,72,25,5,54,19,72,6,44,49,3,65,11,24,85,39,11,5,77,15,6,65,12,66,66,14,8,88,81,2,8,99,7,54,70,2,97,69,9,17,51,47,1,56,88,81,41,10,98,16,23,35,24,82,24,5,99,39,67,8,14,46,56,5,8,59,9,53,9,21,95,6,95,7,12,85,26,79,82,19,21,62,99,5,13,81,19,31,15,29,67,45,22,75,84,14,25,83,33,97,4,85,15,17,25,21,51,55,11,76,32,15,43,60,13,13,11,65,65,16,9,96,26,17,10,94,23,12,37,16,49,2,81,17,11,20,17,16,37,87,16,12,96,23,10,68,22,75,34,4,22,14,34,14,62,8,34,12,72,7,40,5,54,10,89,7,96,1,14,72,7,11,60,93,68,51,21,86,25,34,26,20,38,7,21,94,78,10,8,46,4,81,12,84,30,11,9,48,12,83,73,42,83,26,26,40,22,91,6,38,99,2,40,24,93,10,22,84,22,19,94,8,6,42,33,11,15,31,66,33,2,65,39,67,26,5,67,19,86,1,12,20,28,54,80,84,3,17,32,26,51,8,6,20,67,15,54,30,5,31,97,9,10,29,18,45,8,23,69,18,61,11,4,73,5,46,13,96,16,80,66,17,1,11,50,37,4,34,94,15,32,77,5,93,69,12,66,6,24,18,84,26,42,5,78,74,22,82,15,23,60,11,64,61,59,48,11,99,49,3,68,2,16,14,99,7,94,9,22,75,20,30,21,17,91,20,41,21,26,42,44,19,18,85,17,96,21,2,88,62,69,8,39,3,11,62,12,25,29,69,79,52,56,6,52,22,78,42,8,18,22,59,91,13,94,89,10,16,73,11,17,80,81,26,36,26,55,16,13,30,6,6,43,1,43,83,21,69,11,42,8,77,21,31,25,24,99,26,56,85,15,74,1,88,13,3,18,42,14,54,13,6,91,49,7,36,42,2,8,67,55,14,35,5,33,6,96,24,94,24,59,46,18,4,61,95,2,33,33,2,31,24,97,1,91,15,52,15,53,44,10,20,47,93,8,1,48,80,22,80,23,15,92,18,18,59,19,69,17,8,55,38,26,9,68,23,85,2,12,23,77,4,21,16,6,90,45,17,61,16,28,22,24,58,30,26,2,85,1,53,29,18,37,30,38,4,12,92,60,19,13,56,19,85,7,66,19,73,39,9,90,81,3,8,9,72,25,37,24,5,96,25,13,81,92,34,19,95,3,26,36,25,25,25,15,95,6,35,43,92,10,79,70,8,30,18,96,75,1,5,76,17,86,3,46,22,11,50,96,1,56,43,2,23,53,7,71,20,61,73,34,31,57,24,69,4,24,6,25,98,50,21,63,12,97,11,9,72,19,40,21,7,2,18,77,83,16,1,82,24,25,57,72,25,9,15,76,21,14,71,16,94,7,64,21,69,87,18,65,1,21,20,61,91,10,86,7,55,36,1,40,99,39,8,41,5,92,76,33,20,40,15,81,76,48,5,35,64,59,6,30,13,52,19,84,21,58,1,89,29,53,10,76,22,33,26,65,3,96,0,0,21,21,1,10,1,0,0,0,0,0,0"
        return program
    
    def part1(self, input_data: str) -> int:
        """
        Find the shortest path from the starting position to the oxygen system.
        
        Args:
            input_data: Raw input containing the Intcode program
            
        Returns:
            Length of shortest path to oxygen system
        """
        program = self._get_program(input_data)
        self.explorer = MazeExplorer(program)
        
        # Explore the complete maze
        self.explorer.explore_complete_maze()
        
        # Find shortest path from start (0,0) to oxygen system
        start_pos = Position(0, 0)
        return self.explorer.find_shortest_path(start_pos, self.explorer.oxygen_location)
    
    def part2(self, input_data: str) -> int:
        """
        Find the time required for oxygen to spread throughout the maze.
        
        Args:
            input_data: Raw input containing the Intcode program
            
        Returns:
            Time in minutes for oxygen to fill all reachable areas
        """
        if self.explorer is None:
            # If part1 wasn't run, we need to explore the maze
            program = self._get_program(input_data)
            self.explorer = MazeExplorer(program)
            self.explorer.explore_complete_maze()
        
        # Simulate oxygen spreading from the oxygen system
        return self.explorer.simulate_oxygen_spread()
    
    def analyze_maze(self) -> Dict[str, Any]:
        """
        Provide comprehensive analysis of the explored maze.
        
        Returns:
            Dictionary with detailed maze statistics and analysis
        """
        if self.explorer is None:
            return {"error": "Maze not yet explored"}
        
        stats = self.explorer.get_maze_statistics()
        
        # Add path analysis
        start_pos = Position(0, 0)
        if self.explorer.oxygen_location:
            path_length = self.explorer.find_shortest_path(start_pos, self.explorer.oxygen_location)
            oxygen_spread_time = self.explorer.simulate_oxygen_spread()
            
            stats.update({
                'path_to_oxygen': path_length,
                'oxygen_spread_time': oxygen_spread_time,
                'total_accessible_cells': stats['empty_count'] + stats['oxygen_count']
            })
        
        return stats
    
    def validate(self, expected_part1: Any = None, expected_part2: Any = None) -> bool:
        """Validate the solution with known test cases."""
        # For Day 15, we don't have simple test cases due to the complex nature
        # of the maze exploration, but we can validate that the solution runs
        # and produces reasonable results
        print("Day 15 validation: Running solution check...")
        
        try:
            # Test with empty input (should use fallback program)
            results = self.run(use_test=False)
            
            if 'part1' in results and 'part2' in results:
                part1_result = results['part1']
                part2_result = results['part2']
                
                # Basic sanity checks
                if isinstance(part1_result, int) and part1_result > 0:
                    print(f"✅ Part 1: {part1_result} (positive integer path length)")
                else:
                    print(f"❌ Part 1: {part1_result} (expected positive integer)")
                    return False
                
                if isinstance(part2_result, int) and part2_result > 0:
                    print(f"✅ Part 2: {part2_result} (positive integer time)")
                else:
                    print(f"❌ Part 2: {part2_result} (expected positive integer)")
                    return False
                
                # Part 2 should generally be larger than part 1 for this problem
                if part2_result >= part1_result:
                    print("✅ Part 2 >= Part 1 (oxygen spread time >= path length)")
                else:
                    print(f"⚠️  Part 2 ({part2_result}) < Part 1 ({part1_result}) - unusual but not impossible")
                
                return True
            
        except Exception as e:
            print(f"❌ Validation failed with error: {e}")
            return False
        
        return False

def main():
    """Main execution function."""
    solution = Day15Solution()
    solution.main()

if __name__ == "__main__":
    main()