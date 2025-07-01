#!/usr/bin/env python3
"""
Advent of Code 2019 Day 7: Amplification Circuit
https://adventofcode.com/2019/day/7

Enhanced solution using AdventSolution base class.
Migrated from legacy implementation with improvements.
"""

import sys
from pathlib import Path
from typing import Any, List, Dict, Optional, Tuple
import itertools

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class IntcodeSimple:
    """
    Simplified non-threaded Intcode computer for better performance.
    Optimized for day 7's amplifier circuit simulation.
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
    
    def run_until_output_or_halt(self) -> bool:
        """Run until output is produced or program halts. Returns True if output produced."""
        while not self.halted and not self.waiting_for_input:
            instruction = self.memory[self.pc]
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
                    return False
                addr = self.get_write_address(1, mode1)
                self.memory[addr] = self.inputs.pop(0)
                self.pc += 2
            
            elif opcode == 4:  # Output
                val = self.get_parameter_value(1, mode1)
                self.outputs.append(val)
                self.pc += 2
                return True  # Output produced
            
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
        
        return False


class Day7Solution(AdventSolution):
    """Solution for 2019 Day 7: Amplification Circuit."""

    def __init__(self):
        super().__init__(2019, 7, "Amplification Circuit")

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Find maximum signal through amplifier chain.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Maximum signal that can be sent to thrusters
        """
        program = input_data.strip()
        max_signal = 0
        
        for phase_sequence in itertools.permutations([0, 1, 2, 3, 4]):
            signal = 0
            
            # Run through each amplifier in sequence
            for phase in phase_sequence:
                amp = IntcodeSimple(program)
                amp.add_input(phase)  # Phase setting
                amp.add_input(signal)  # Input signal
                
                # Run until output
                amp.run_until_output_or_halt()
                signal = amp.outputs[0]
            
            max_signal = max(max_signal, signal)
        
        return max_signal

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Find maximum signal with feedback loop.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Maximum signal with feedback loop configuration
        """
        program = input_data.strip()
        max_signal = 0
        
        for phase_sequence in itertools.permutations([5, 6, 7, 8, 9]):
            # Initialize all amplifiers
            amps = [IntcodeSimple(program) for _ in range(5)]
            
            # Set phase settings
            for i, phase in enumerate(phase_sequence):
                amps[i].add_input(phase)
            
            # Start with signal 0 to amplifier A
            signal = 0
            amp_index = 0
            
            # Run feedback loop until amplifier E halts
            while not amps[4].halted:
                current_amp = amps[amp_index]
                current_amp.add_input(signal)
                
                # Run until output or halt
                produced_output = current_amp.run_until_output_or_halt()
                
                if produced_output:
                    signal = current_amp.outputs[-1]  # Get latest output
                
                # Move to next amplifier
                amp_index = (amp_index + 1) % 5
            
            max_signal = max(max_signal, signal)
        
        return max_signal

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test case from problem description
        test_program = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
        
        if expected_part1 is None:
            expected_part1 = 43210  # Expected result for test case
        
        test_result1 = self.part1(test_program)
        if test_result1 != expected_part1:
            print(f"Part 1 test failed: expected {expected_part1}, got {test_result1}")
            return False
        
        # Test case for part 2
        test_program2 = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
        if expected_part2 is None:
            expected_part2 = 139629729  # Expected result for test case
        
        test_result2 = self.part2(test_program2)
        if test_result2 != expected_part2:
            print(f"Part 2 test failed: expected {expected_part2}, got {test_result2}")
            return False
        
        print("✅ All validation tests passed!")
        return True


def main():
    """Main execution function."""
    solution = Day7Solution()
    solution.main()


if __name__ == "__main__":
    main()