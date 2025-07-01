#!/usr/bin/env python3
"""
Optimized Intcode Computer Implementation

High-performance Intcode interpreter without threading overhead.
Provides both object-oriented and functional interfaces for maximum flexibility.

This replaces the original threaded implementation with a much faster
synchronous version optimized for Advent of Code 2019 problems.
"""

from typing import List, Optional, Union, Any


def get_digit(number: int, n: int) -> int:
    """
    Get the nth digit from the right of a number (0-indexed).
    
    Args:
        number: The number to extract from
        n: Position from right (0 = rightmost)
        
    Returns:
        The digit at position n
    """
    return number // 10**n % 10


class IntcodeOptimized:
    """
    Optimized Intcode computer with synchronous execution.
    
    This implementation provides the same functionality as the original
    threaded version but with much better performance due to:
    - No threading overhead
    - Reduced memory allocation
    - Simplified I/O handling
    - Optimized instruction execution
    """
    
    def __init__(self, commandstr: str):
        """
        Initialize the Intcode computer.
        
        Args:
            commandstr: Comma-separated string of integers representing the program
        """
        self.commands: List[int] = [int(i) for i in commandstr.split(',')]
        # Extend memory (reduced from 25000 for better performance)
        self.commands.extend([0] * 10000)
        
        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.halted: bool = False
        self.needInput: bool = False
        self.pc: int = 0
        self.relative_base: int = 0
    
    def add_input(self, val: int) -> None:
        """
        Add an input value to the input queue.
        
        Args:
            val: Integer value to add to inputs
        """
        self.inputs.append(val)
        self.needInput = False
    
    def get_parameter_value(self, offset: int, mode: int) -> int:
        """Get parameter value based on addressing mode."""
        if mode == 0:  # Position mode
            return self.commands[self.commands[self.pc + offset]]
        elif mode == 1:  # Immediate mode
            return self.commands[self.pc + offset]
        elif mode == 2:  # Relative mode
            return self.commands[self.relative_base + self.commands[self.pc + offset]]
        else:
            raise ValueError(f"Unknown parameter mode: {mode}")
    
    def get_write_address(self, offset: int, mode: int) -> int:
        """Get write address based on addressing mode."""
        if mode == 0:  # Position mode
            return self.commands[self.pc + offset]
        elif mode == 2:  # Relative mode
            return self.relative_base + self.commands[self.pc + offset]
        else:
            raise ValueError(f"Invalid write mode: {mode}")
    
    def run(self) -> List[int]:
        """
        Execute the Intcode program completely.
        
        Returns:
            List of output values produced by the program
        """
        while not self.halted:
            if not self.step():
                break
        return self.outputs
    
    def step(self) -> bool:
        """
        Execute one instruction.
        
        Returns:
            False if halted or needs input, True otherwise
        """
        if self.halted:
            return False
            
        instruction = self.commands[self.pc]
        opcode = instruction % 100
        mode1 = (instruction // 100) % 10
        mode2 = (instruction // 1000) % 10
        mode3 = (instruction // 10000) % 10
        
        if opcode == 99:  # Halt
            self.halted = True
            return False
        
        elif opcode == 1:  # Add
            val1 = self.get_parameter_value(1, mode1)
            val2 = self.get_parameter_value(2, mode2)
            addr = self.get_write_address(3, mode3)
            self.commands[addr] = val1 + val2
            self.pc += 4
        
        elif opcode == 2:  # Multiply
            val1 = self.get_parameter_value(1, mode1)
            val2 = self.get_parameter_value(2, mode2)
            addr = self.get_write_address(3, mode3)
            self.commands[addr] = val1 * val2
            self.pc += 4
        
        elif opcode == 3:  # Input
            if not self.inputs:
                self.needInput = True
                return False
            addr = self.get_write_address(1, mode1)
            self.commands[addr] = self.inputs.pop(0)
            self.pc += 2
        
        elif opcode == 4:  # Output
            val = self.get_parameter_value(1, mode1)
            self.outputs.append(val)
            self.pc += 2
        
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
            self.commands[addr] = 1 if val1 < val2 else 0
            self.pc += 4
        
        elif opcode == 8:  # Equals
            val1 = self.get_parameter_value(1, mode1)
            val2 = self.get_parameter_value(2, mode2)
            addr = self.get_write_address(3, mode3)
            self.commands[addr] = 1 if val1 == val2 else 0
            self.pc += 4
        
        elif opcode == 9:  # Adjust relative base
            val = self.get_parameter_value(1, mode1)
            self.relative_base += val
            self.pc += 2
        
        else:
            raise ValueError(f"Unknown opcode: {opcode}")
        
        return True
    
    def run_until_output_or_halt(self) -> bool:
        """
        Run until output is produced or program halts.
        
        Returns:
            True if output was produced, False if halted
        """
        initial_output_count = len(self.outputs)
        
        while not self.halted:
            if not self.step():
                break
            if len(self.outputs) > initial_output_count:
                return True
        
        return False
    
    def wait_for_output(self) -> None:
        """Wait until an output is available (compatibility method)."""
        while len(self.outputs) == 0 and not self.halted:
            if not self.step():
                break
    
    # Threading compatibility methods
    def start(self) -> None:
        """Start execution (compatibility method for threaded interface)."""
        self.run()
    
    def join(self) -> None:
        """Wait for completion (compatibility method for threaded interface)."""
        # Already completed synchronously
        pass


# Backward compatibility alias
Intcode = IntcodeOptimized


def run_intcode_simple(program: str, noun: Optional[int] = None, verb: Optional[int] = None) -> int:
    """
    Run Intcode program with optional noun/verb modifications and return first output.
    
    This is a simplified functional interface for basic Intcode execution.
    
    Args:
        program: Comma-separated Intcode program string
        noun: Optional value to set at position 1
        verb: Optional value to set at position 2
    
    Returns:
        First output value from the program
    """
    computer = IntcodeOptimized(program)
    
    if noun is not None:
        computer.commands[1] = noun
    if verb is not None:
        computer.commands[2] = verb
    
    outputs = computer.run()
    return outputs[0] if outputs else computer.commands[0]


def run_intcode_with_input(program: str, input_values: Union[int, List[int]]) -> List[int]:
    """
    Run Intcode program with input values and return all outputs.
    
    Args:
        program: Comma-separated Intcode program string
        input_values: Single input value or list of input values
    
    Returns:
        List of all output values from the program
    """
    computer = IntcodeOptimized(program)
    
    if isinstance(input_values, int):
        computer.add_input(input_values)
    else:
        for val in input_values:
            computer.add_input(val)
    
    return computer.run()