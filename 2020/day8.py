#!/usr/bin/env python3
"""
Advent of Code 2020 Day 8: Handheld Halting
https://adventofcode.com/2020/day/8

Enhanced solution using AdventSolution base class.
Assembly interpreter with instruction modification and infinite loop detection.
"""

import sys
from pathlib import Path
from typing import Any, List, Dict, Optional, Tuple, Set

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class HandheldConsole:
    """Simulates a handheld gaming console with a simple instruction set."""
    
    def __init__(self, instructions: List[Tuple[str, int]]):
        """
        Initialize the console with a program.
        
        Args:
            instructions: List of (operation, argument) tuples
        """
        self.instructions = instructions.copy()
        self.pc = 0  # Program counter
        self.accumulator = 0
        self.visited_instructions: Set[int] = set()
        self.terminated = False
        self.infinite_loop = False
    
    def reset(self):
        """Reset the console state."""
        self.pc = 0
        self.accumulator = 0
        self.visited_instructions.clear()
        self.terminated = False
        self.infinite_loop = False
    
    def step(self) -> bool:
        """
        Execute one instruction.
        
        Returns:
            True if execution should continue, False if terminated or infinite loop
        """
        # Check for termination (PC beyond program)
        if self.pc >= len(self.instructions):
            self.terminated = True
            return False
        
        # Check for infinite loop
        if self.pc in self.visited_instructions:
            self.infinite_loop = True
            return False
        
        # Mark current instruction as visited
        self.visited_instructions.add(self.pc)
        
        # Get current instruction
        operation, argument = self.instructions[self.pc]
        
        # Execute instruction
        if operation == 'acc':
            self.accumulator += argument
            self.pc += 1
        elif operation == 'jmp':
            self.pc += argument
        elif operation == 'nop':
            self.pc += 1
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        return True
    
    def run(self) -> Tuple[bool, int]:
        """
        Run the program until termination or infinite loop.
        
        Returns:
            Tuple of (terminated_normally, final_accumulator_value)
        """
        while self.step():
            pass
        
        return self.terminated, self.accumulator
    
    def run_with_modification(self, modify_pc: int) -> Tuple[bool, int]:
        """
        Run program with a single instruction modification.
        
        Args:
            modify_pc: Program counter of instruction to modify (jmp<->nop)
            
        Returns:
            Tuple of (terminated_normally, final_accumulator_value)
        """
        # Save original instruction
        original_op, arg = self.instructions[modify_pc]
        
        # Modify instruction
        if original_op == 'jmp':
            self.instructions[modify_pc] = ('nop', arg)
        elif original_op == 'nop':
            self.instructions[modify_pc] = ('jmp', arg)
        else:
            # Can't modify acc instructions
            return False, 0
        
        # Reset and run
        self.reset()
        terminated, acc_value = self.run()
        
        # Restore original instruction
        self.instructions[modify_pc] = (original_op, arg)
        
        return terminated, acc_value


class Day8Solution(AdventSolution):
    """Solution for 2020 Day 8: Handheld Halting."""

    def __init__(self):
        super().__init__(2020, 8, "Handheld Halting")

    def parse_instructions(self, input_data: str) -> List[Tuple[str, int]]:
        """
        Parse input into instruction list.
        
        Args:
            input_data: Raw input data
            
        Returns:
            List of (operation, argument) tuples
        """
        instructions = []
        
        for line in input_data.strip().split('\n'):
            parts = line.strip().split(' ')
            operation = parts[0]
            argument = int(parts[1])
            instructions.append((operation, argument))
        
        return instructions

    def part1(self, input_data: str) -> Any:
        """
        Find the accumulator value just before any instruction is executed twice.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Accumulator value before infinite loop
        """
        instructions = self.parse_instructions(input_data)
        console = HandheldConsole(instructions)
        
        terminated, accumulator = console.run()
        
        # Part 1 expects an infinite loop, not termination
        if terminated:
            return f"Program terminated normally with accumulator: {accumulator}"
        
        return accumulator

    def part2(self, input_data: str) -> Any:
        """
        Fix the program by changing exactly one jmp to nop or nop to jmp.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Accumulator value when program terminates normally
        """
        instructions = self.parse_instructions(input_data)
        console = HandheldConsole(instructions)
        
        # Find all jmp and nop instructions that could be modified
        modifiable_instructions = []
        for i, (op, arg) in enumerate(instructions):
            if op in ['jmp', 'nop']:
                modifiable_instructions.append(i)
        
        # Try modifying each instruction
        for pc_to_modify in modifiable_instructions:
            terminated, accumulator = console.run_with_modification(pc_to_modify)
            
            if terminated:
                return accumulator
        
        return "No solution found"

    def debug_program(self, input_data: str) -> str:
        """
        Debug helper to show program execution trace.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Debug information string
        """
        instructions = self.parse_instructions(input_data)
        console = HandheldConsole(instructions)
        
        debug_info = []
        debug_info.append(f"Program has {len(instructions)} instructions")
        debug_info.append("Execution trace:")
        
        step_count = 0
        while console.step() and step_count < 20:  # Limit trace to first 20 steps
            prev_pc = list(console.visited_instructions)[-1] if console.visited_instructions else 0
            op, arg = instructions[prev_pc]
            debug_info.append(f"  Step {step_count}: PC={prev_pc}, {op} {arg:+d}, ACC={console.accumulator}")
            step_count += 1
        
        if console.infinite_loop:
            debug_info.append(f"Infinite loop detected at instruction {console.pc}")
        elif console.terminated:
            debug_info.append("Program terminated normally")
        else:
            debug_info.append("Trace truncated...")
        
        return "\n".join(debug_info)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
        expected_part1 = 5
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        expected_part2 = 8

        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False
        
        print("✅ All Day 8 validation tests passed!")
        return True

def main():
    """Main execution function."""
    solution = Day8Solution()
    
    # Uncomment to run debug trace
    # print(solution.debug_program(open('day8_input.txt').read()))
    
    solution.main()


if __name__ == "__main__":
    main()