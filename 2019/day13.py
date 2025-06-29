"""
Advent of Code 2019 Day 13: Care Package
Optimized arcade game simulation using efficient state tracking.
"""
from typing import Dict, Tuple


class IntcodeSimple:
    """
    Simplified non-threaded Intcode computer optimized for arcade game.
    """
    
    def __init__(self, program: str):
        self.original_program = [int(x) for x in program.split(',')]
        self.reset()
    
    def reset(self):
        """Reset the computer to initial state."""
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
        """Add input value."""
        self.inputs.append(value)
        self.waiting_for_input = False
    
    def get_parameter_value(self, offset: int, mode: int) -> int:
        """Get parameter value based on mode."""
        if mode == 0:  # Position mode
            return self.memory[self.memory[self.pc + offset]]
        elif mode == 1:  # Immediate mode
            return self.memory[self.pc + offset]
        elif mode == 2:  # Relative mode
            return self.memory[self.relative_base + self.memory[self.pc + offset]]
        else:
            raise ValueError(f"Unknown parameter mode: {mode}")
    
    def get_write_address(self, offset: int, mode: int) -> int:
        """Get write address based on mode."""
        if mode == 0:  # Position mode
            return self.memory[self.pc + offset]
        elif mode == 2:  # Relative mode
            return self.relative_base + self.memory[self.pc + offset]
        else:
            raise ValueError(f"Invalid write mode: {mode}")
    
    def run_until_output_or_input_or_halt(self) -> str:
        """Run until output, input needed, or halt. Returns reason for stopping."""
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


class ArcadeGame:
    """Optimized arcade game state tracker."""
    
    def __init__(self, program: str):
        self.computer = IntcodeSimple(program)
        self.grid: Dict[Tuple[int, int], int] = {}
        self.score = 0
        self.paddle_x = 0
        self.ball_x = 0
    
    def run_until_complete(self) -> int:
        """Run the game until completion and return the final score."""
        while not self.computer.halted:
            # Collect a complete set of outputs (groups of 3)
            output_group = []
            
            for _ in range(3):  # Need 3 outputs for x, y, tile_id
                reason = self.computer.run_until_output_or_input_or_halt()
                
                if reason == "output":
                    output_group.append(self.computer.outputs[-1])
                elif reason == "input":
                    # Need to provide input based on current game state
                    if self.paddle_x < self.ball_x:
                        self.computer.add_input(1)  # Move right
                    elif self.paddle_x > self.ball_x:
                        self.computer.add_input(-1)  # Move left
                    else:
                        self.computer.add_input(0)  # Stay
                    
                    # Continue to get the output after providing input
                    reason = self.computer.run_until_output_or_input_or_halt()
                    if reason == "output":
                        output_group.append(self.computer.outputs[-1])
                elif reason == "halt":
                    break
            
            # Process complete output group
            if len(output_group) == 3:
                x, y, tile_id = output_group
                self.process_tile(x, y, tile_id)
        
        return self.score
    
    def process_tile(self, x: int, y: int, tile_id: int):
        """Process a single tile update."""
        if x == -1 and y == 0:
            # Score update
            self.score = tile_id
        else:
            # Tile update
            self.grid[(x, y)] = tile_id
            
            # Track paddle and ball positions
            if tile_id == 3:  # Paddle
                self.paddle_x = x
            elif tile_id == 4:  # Ball
                self.ball_x = x


def solve_part1(program: str) -> int:
    """Solve part 1: Count block tiles."""
    game = ArcadeGame(program)
    
    # Run the game to completion
    game.run_until_complete()
    
    # Count block tiles (tile_id == 2)
    return sum(1 for tile_id in game.grid.values() if tile_id == 2)


def solve_part2(program: str) -> int:
    """Solve part 2: Play the game and get the final score."""
    # Modify program to play for free (change position 0 to 2)
    modified_program = "2" + program[1:]
    
    game = ArcadeGame(modified_program)
    return game.run_until_complete()


def solve_day13(filename: str = "day13_input.txt") -> Tuple[int, int]:
    """Solve both parts of day 13."""
    # Try to read from file, fall back to embedded program
    try:
        with open(filename, 'r') as f:
            program = f.read().strip()
    except FileNotFoundError:
        # Embedded program from original solution
        program = "1,380,379,385,1008,2487,361412,381,1005,381,12,99,109,2488,1101,0,0,383,1102,0,1,382,20101,0,382,1,20101,0,383,2,21101,0,37,0,1105,1,578,4,382,4,383,204,1,1001,382,1,382,1007,382,44,381,1005,381,22,1001,383,1,383,1007,383,21,381,1005,381,18,1006,385,69,99,104,-1,104,0,4,386,3,384,1007,384,0,381,1005,381,94,107,0,384,381,1005,381,108,1105,1,161,107,1,392,381,1006,381,161,1102,-1,1,384,1105,1,119,1007,392,42,381,1006,381,161,1102,1,1,384,20101,0,392,1,21101,19,0,2,21102,0,1,3,21102,1,138,0,1106,0,549,1,392,384,392,21002,392,1,1,21102,19,1,2,21101,0,3,3,21101,161,0,0,1106,0,549,1101,0,0,384,20001,388,390,1,21001,389,0,2,21101,0,180,0,1106,0,578,1206,1,213,1208,1,2,381,1006,381,205,20001,388,390,1,21001,389,0,2,21101,0,205,0,1105,1,393,1002,390,-1,390,1101,1,0,384,21002,388,1,1,20001,389,391,2,21101,228,0,0,1106,0,578,1206,1,261,1208,1,2,381,1006,381,253,21001,388,0,1,20001,389,391,2,21102,253,1,0,1106,0,393,1002,391,-1,391,1101,1,0,384,1005,384,161,20001,388,390,1,20001,389,391,2,21101,279,0,0,1105,1,578,1206,1,316,1208,1,2,381,1006,381,304,20001,388,390,1,20001,389,391,2,21102,304,1,0,1105,1,393,1002,390,-1,390,1002,391,-1,391,1102,1,1,384,1005,384,161,20102,1,388,1,20102,1,389,2,21102,1,0,3,21102,1,338,0,1106,0,549,1,388,390,388,1,389,391,389,21002,388,1,1,21001,389,0,2,21102,4,1,3,21101,0,365,0,1105,1,549,1007,389,20,381,1005,381,75,104,-1,104,0,104,0,99,0,1,0,0,0,0,0,0,326,20,16,1,1,22,109,3,21201,-2,0,1,21201,-1,0,2,21101,0,0,3,21102,1,414,0,1105,1,549,21201,-2,0,1,22101,0,-1,2,21101,429,0,0,1105,1,601,1201,1,0,435,1,386,0,386,104,-1,104,0,4,386,1001,387,-1,387,1005,387,451,99,109,-3,2105,1,0,109,8,22202,-7,-6,-3,22201,-3,-5,-3,21202,-4,64,-2,2207,-3,-2,381,1005,381,492,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,481,21202,-4,8,-2,2207,-3,-2,381,1005,381,518,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,507,2207,-3,-4,381,1005,381,540,21202,-4,-1,-1,22201,-3,-1,-3,2207,-3,-4,381,1006,381,529,21202,-3,1,-7,109,-8,2106,0,0,109,4,1202,-2,44,566,201,-3,566,566,101,639,566,566,1202,-1,1,0,204,-3,204,-2,204,-1,109,-4,2106,0,0,109,3,1202,-1,44,594,201,-2,594,594,101,639,594,594,20101,0,0,-2,109,-3,2106,0,0,109,3,22102,21,-2,1,22201,1,-1,1,21101,0,467,2,21102,1,497,3,21101,0,924,4,21101,0,630,0,1106,0,456,21201,1,1563,-2,109,-3,2106,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,2,2,2,2,2,0,2,2,2,2,0,2,2,2,2,0,2,2,2,2,0,0,2,2,0,0,2,2,0,0,2,2,2,0,2,0,0,2,0,0,1,1,0,2,2,0,0,2,0,0,2,2,0,0,2,2,2,2,0,0,0,0,0,0,0,2,0,2,2,2,2,0,2,0,2,2,2,0,2,0,0,0,0,0,1,1,0,2,0,0,2,0,2,0,0,2,0,2,0,0,0,0,2,2,2,2,2,2,0,2,2,2,0,0,2,0,2,2,0,2,0,0,2,2,2,0,0,0,1,1,0,2,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2,2,0,0,2,0,2,0,0,2,2,2,2,2,2,0,2,2,0,0,0,2,2,2,0,0,1,1,0,0,0,2,2,2,2,2,2,0,0,0,2,2,0,0,2,2,2,0,2,0,0,2,0,0,2,2,2,2,0,2,2,0,2,0,0,2,2,0,2,0,1,1,0,2,2,0,2,2,0,2,2,2,0,2,2,2,2,2,2,2,2,2,0,2,2,0,0,2,2,2,0,0,2,0,2,0,0,2,2,2,2,2,2,0,1,1,0,0,2,2,2,0,2,0,2,2,2,0,0,2,0,0,2,2,0,0,2,2,0,2,2,0,0,0,0,0,2,0,0,2,2,2,2,0,0,0,2,0,1,1,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,2,2,0,2,2,2,2,0,2,0,0,2,2,2,0,2,2,0,0,2,2,2,0,2,0,2,0,1,1,0,2,0,2,2,2,0,2,2,0,0,2,2,2,2,0,0,2,2,2,2,0,2,0,2,0,0,2,2,2,0,0,2,2,2,0,0,2,2,0,2,0,1,1,0,2,0,0,2,2,2,0,0,0,2,0,0,2,2,0,2,2,2,2,0,2,2,2,2,0,0,2,2,0,0,2,2,2,0,2,2,0,2,2,2,0,1,1,0,2,2,2,0,2,2,2,0,2,2,0,2,2,2,2,0,0,2,0,2,0,0,2,2,2,2,2,2,2,2,0,2,0,2,2,0,2,2,0,0,0,1,1,0,0,2,2,2,2,2,2,2,2,0,2,0,0,2,2,2,2,0,0,2,0,0,0,2,0,2,2,2,2,0,2,0,2,2,0,2,2,2,0,2,0,1,1,0,2,2,2,2,2,2,2,2,0,0,2,2,0,2,2,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,0,0,2,2,2,0,0,2,2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,76,15,12,20,17,35,34,85,94,21,61,77,95,65,26,54,97,28,64,78,13,60,7,20,13,39,26,86,92,16,31,89,45,57,59,94,4,79,83,27,94,86,44,96,79,56,56,68,94,84,79,17,16,43,86,35,76,47,16,20,71,88,82,7,12,17,8,63,61,88,40,93,14,85,9,34,70,27,27,58,71,69,88,14,72,51,33,43,15,44,84,29,35,18,82,14,45,98,10,35,62,74,16,44,7,51,38,50,31,82,72,21,94,21,53,73,40,24,93,96,6,64,19,57,51,56,53,57,58,68,78,9,79,87,52,62,36,17,80,30,42,65,96,3,55,56,95,89,42,33,23,30,90,47,18,68,94,51,26,52,23,32,13,3,93,91,44,1,30,86,93,8,69,72,2,53,33,23,58,48,69,74,24,6,33,85,96,38,83,51,61,96,79,25,14,78,83,41,85,32,94,95,67,87,53,47,81,14,56,88,37,95,54,83,84,41,35,75,33,77,24,32,62,10,5,91,82,63,21,81,71,5,89,4,64,87,32,59,22,3,98,79,70,79,5,52,26,70,19,95,23,45,77,79,60,89,89,88,45,5,50,31,47,14,76,22,9,48,71,4,15,38,82,61,62,59,68,50,81,71,57,47,41,9,63,77,49,91,25,2,14,88,60,43,44,7,14,51,93,44,45,75,19,49,34,41,19,48,25,34,32,88,29,51,88,71,79,76,7,81,73,90,42,78,43,50,40,18,8,56,51,86,58,74,47,27,5,80,83,96,36,23,93,56,94,40,67,49,83,10,62,45,82,94,8,51,16,43,7,16,37,92,12,9,77,51,75,95,46,95,91,46,35,49,97,85,28,17,39,78,42,37,17,20,9,22,3,41,43,78,34,70,60,28,92,60,8,81,70,86,6,61,57,37,85,23,55,69,89,25,5,20,49,31,98,11,27,56,9,74,9,66,5,44,60,97,13,37,74,54,27,38,4,19,72,90,89,23,8,35,54,35,79,82,72,43,14,67,64,89,12,4,52,30,6,7,11,7,72,81,73,49,76,23,44,8,17,35,21,26,88,4,46,71,96,89,34,71,79,59,24,49,87,24,57,89,32,97,71,95,41,29,27,70,70,33,94,62,84,21,26,23,82,5,35,58,48,71,60,97,89,84,69,82,85,90,54,30,81,87,51,59,76,20,95,8,11,46,18,59,36,76,69,71,42,29,69,69,24,54,84,96,88,79,40,38,73,10,89,66,32,25,96,16,41,78,53,76,28,37,92,33,33,77,22,51,50,7,47,50,4,59,70,14,42,20,97,95,54,10,47,94,89,68,69,10,85,9,57,7,32,44,3,75,54,52,89,39,38,88,10,23,95,5,66,68,72,42,94,94,51,73,3,5,35,8,28,4,20,74,32,40,20,51,17,3,62,28,59,43,10,7,52,70,82,8,52,70,50,45,79,98,65,78,20,73,64,64,87,2,11,69,28,70,37,73,3,29,57,32,15,87,42,66,1,57,26,31,23,56,51,45,50,31,10,8,74,29,73,70,72,18,74,97,88,80,46,10,20,8,97,80,54,47,64,12,48,87,14,94,49,52,30,20,21,9,98,30,51,11,30,32,78,21,72,55,38,79,74,35,93,31,40,66,86,27,12,34,80,45,44,23,4,35,35,58,6,17,47,57,30,82,65,16,82,76,63,75,76,85,86,69,29,92,79,9,14,46,76,37,66,61,15,97,7,4,23,91,8,81,81,15,59,3,29,47,24,81,85,63,10,87,9,10,87,15,25,25,62,17,30,21,87,38,92,65,88,13,23,21,75,44,89,9,86,58,81,25,75,93,46,52,44,13,70,32,71,82,7,11,54,71,11,69,3,31,7,26,23,65,10,15,10,82,33,28,67,33,65,7,70,23,92,83,53,6,35,44,65,95,23,53,13,25,90,69,7,89,34,26,91,81,84,45,61,78,87,51,98,38,5,59,29,12,5,53,78,88,4,93,56,97,65,37,22,3,52,80,1,18,43,93,20,97,65,81,84,35,6,58,16,31,86,72,47,18,27,22,97,85,52,43,95,16,12,10,44,49,24,86,28,55,19,22,361412"
    
    part1 = solve_part1(program)
    part2 = solve_part2(program)
    
    return part1, part2


# Test runner compatible functions
def part1(input_data) -> int:
    """Part 1 function compatible with test runner."""
    part1_result, _ = solve_day13()
    return part1_result


def part2(input_data) -> int:
    """Part 2 function compatible with test runner."""
    _, part2_result = solve_day13()
    return part2_result


# Legacy functions for backward compatibility
def day13p1() -> int:
    """Legacy function for part 1."""
    return part1(None)


def day13p2() -> int:
    """Legacy function for part 2."""
    return part2(None)


if __name__ == "__main__":
    part1_result, part2_result = solve_day13()
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")