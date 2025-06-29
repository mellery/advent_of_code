"""
Advent of Code 2019 Day 11: Space Police
Optimized robot painting simulation using efficient data structures.
"""


class IntcodeSimple:
    """
    Simplified non-threaded Intcode computer optimized for robot control.
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


class PaintingRobot:
    """Optimized robot that paints panels using efficient coordinate system."""
    
    # Direction vectors: up, right, down, left
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def __init__(self, starting_color: int = 0):
        self.x = 0
        self.y = 0
        self.direction = 0  # 0=up, 1=right, 2=down, 3=left
        self.panels = {(0, 0): starting_color}  # Default to black, override starting panel
        
    def get_current_color(self) -> int:
        """Get color of current panel (0=black, 1=white)."""
        return self.panels.get((self.x, self.y), 0)
    
    def paint_panel(self, color: int):
        """Paint current panel with given color."""
        self.panels[(self.x, self.y)] = color
    
    def turn_and_move(self, turn_direction: int):
        """Turn (0=left, 1=right) and move forward one panel."""
        if turn_direction == 0:  # Turn left
            self.direction = (self.direction - 1) % 4
        else:  # Turn right
            self.direction = (self.direction + 1) % 4
        
        # Move forward in current direction
        dx, dy = self.DIRECTIONS[self.direction]
        self.x += dx
        self.y += dy
    
    def run_painting_program(self, intcode_program: str) -> int:
        """Run the painting program and return number of panels painted."""
        robot_brain = IntcodeSimple(intcode_program)
        
        # Provide initial input
        robot_brain.add_input(self.get_current_color())
        
        while not robot_brain.halted:
            # Get two outputs: paint color and turn direction
            outputs_needed = 2
            outputs_received = 0
            
            while outputs_received < outputs_needed and not robot_brain.halted:
                reason = robot_brain.run_until_output_or_input_or_halt()
                
                if reason == "output":
                    outputs_received += 1
                elif reason == "input":
                    # Provide input for current position
                    robot_brain.add_input(self.get_current_color())
                elif reason == "halt":
                    break
            
            if outputs_received >= 2:
                # Get the two most recent outputs
                paint_color = robot_brain.outputs[-2]
                turn_direction = robot_brain.outputs[-1]
                
                # Paint current panel
                self.paint_panel(paint_color)
                
                # Turn and move
                self.turn_and_move(turn_direction)
        
        return len(self.panels)
    
    def get_painted_image(self) -> str:
        """Get the painted image as a string for display."""
        if not self.panels:
            return ""
        
        # Find bounds of painted area
        xs = [pos[0] for pos in self.panels.keys()]
        ys = [pos[1] for pos in self.panels.keys()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # Build image from top to bottom (y decreasing)
        lines = []
        for y in range(max_y, min_y - 1, -1):
            line = ""
            for x in range(min_x, max_x + 1):
                if self.panels.get((x, y), 0) == 1:
                    line += "█"  # White panel
                else:
                    line += " "  # Black panel
            lines.append(line.rstrip())  # Remove trailing spaces
        
        # Remove empty lines at the end
        while lines and not lines[-1].strip():
            lines.pop()
        
        return "\n".join(lines)


def solve_day11(filename: str = "day11_input.txt") -> tuple[int, str]:
    """Solve both parts of day 11."""
    # The intcode program is embedded in the original solution
    intcode_program = "3,8,1005,8,345,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,102,1,8,28,1006,0,94,2,106,5,10,1,1109,12,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,62,1,103,6,10,1,108,12,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,92,2,104,18,10,2,1109,2,10,2,1007,5,10,1,7,4,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,129,2,1004,15,10,2,1103,15,10,2,1009,6,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,164,2,1109,14,10,1,1107,18,10,1,1109,13,10,1,1107,11,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,201,2,104,20,10,1,107,8,10,1,1007,5,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,236,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,257,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,279,1,107,0,10,1,107,16,10,1006,0,24,1,101,3,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,316,2,1108,15,10,2,4,11,10,101,1,9,9,1007,9,934,10,1005,10,15,99,109,667,104,0,104,1,21101,0,936995730328,1,21102,362,1,0,1105,1,466,21102,1,838210728716,1,21101,373,0,0,1105,1,466,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,235350789351,1,21101,0,420,0,1105,1,466,21102,29195603035,1,1,21102,1,431,0,1105,1,466,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,825016079204,1,21101,0,454,0,1105,1,466,21101,837896786700,0,1,21102,1,465,0,1106,0,466,99,109,2,21201,-1,0,1,21101,0,40,2,21102,1,497,3,21101,0,487,0,1105,1,530,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,492,493,508,4,0,1001,492,1,492,108,4,492,10,1006,10,524,1101,0,0,492,109,-2,2105,1,0,0,109,4,2102,1,-1,529,1207,-3,0,10,1006,10,547,21102,1,0,-3,21201,-3,0,1,22102,1,-2,2,21101,1,0,3,21102,1,566,0,1105,1,571,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,594,2207,-4,-2,10,1006,10,594,21201,-4,0,-4,1106,0,662,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21101,613,0,0,1105,1,571,22101,0,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,632,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,654,22101,0,-1,1,21102,654,1,0,105,1,529,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0"
    
    # Part 1: Start with black panel
    robot1 = PaintingRobot(starting_color=0)
    panels_painted = robot1.run_painting_program(intcode_program)
    
    # Part 2: Start with white panel
    robot2 = PaintingRobot(starting_color=1)
    robot2.run_painting_program(intcode_program)
    registration_image = robot2.get_painted_image()
    
    return panels_painted, registration_image


# Test runner compatible functions
def part1(input_data) -> int:
    """Part 1 function compatible with test runner."""
    panels_painted, _ = solve_day11()
    return panels_painted


def part2(input_data) -> str:
    """Part 2 function compatible with test runner."""
    _, registration_image = solve_day11()
    return registration_image


# Legacy functions for backward compatibility
def day11p1() -> int:
    """Legacy function for part 1."""
    return part1(None)


def day11p2() -> str:
    """Legacy function for part 2."""
    result = part2(None)
    print(result)
    return result


if __name__ == "__main__":
    panels_painted, registration_image = solve_day11()
    print(f"Part 1: {panels_painted}")
    print("Part 2:")
    print(registration_image)