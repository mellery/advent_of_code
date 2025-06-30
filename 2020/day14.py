#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 14: Docking Data

Bitmask operations and memory management with floating bit addresses.
Two different memory systems:
- Part 1: Apply bitmask to values before storing
- Part 2: Apply bitmask to memory addresses (floating bits)

The challenge involves binary operations and combinatorial address generation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import Dict, List, Tuple, Any, Optional
import re
from itertools import product


class BitMask:
    """Represents a bitmask with support for floating bits."""
    
    def __init__(self, mask_string: str):
        """
        Initialize a bitmask.
        
        Args:
            mask_string: 36-character string with '0', '1', or 'X'
        """
        if len(mask_string) != 36:
            raise ValueError(f"Mask must be 36 characters, got {len(mask_string)}")
        
        self.mask = mask_string
        self.length = len(mask_string)
        self.floating_positions = [i for i, bit in enumerate(mask_string) if bit == 'X']
        self.floating_count = len(self.floating_positions)
    
    def apply_to_value(self, value: int) -> int:
        """
        Apply bitmask to a value (Part 1 logic).
        
        Args:
            value: Integer value to mask
            
        Returns:
            Masked value
        """
        # Convert to binary string with proper padding
        binary_str = format(value, f'0{self.length}b')
        result_bits = []
        
        for i, (mask_bit, value_bit) in enumerate(zip(self.mask, binary_str)):
            if mask_bit == 'X':
                result_bits.append(value_bit)
            else:
                result_bits.append(mask_bit)
        
        return int(''.join(result_bits), 2)
    
    def apply_to_address(self, address: int) -> List[int]:
        """
        Apply bitmask to memory address (Part 2 logic).
        
        Args:
            address: Memory address to mask
            
        Returns:
            List of all possible addresses after floating bit expansion
        """
        # Convert to binary string with proper padding
        binary_str = format(address, f'0{self.length}b')
        masked_bits = list(binary_str)
        
        # Apply mask: 0 -> unchanged, 1 -> set to 1, X -> floating
        for i, mask_bit in enumerate(self.mask):
            if mask_bit == '1':
                masked_bits[i] = '1'
            elif mask_bit == 'X':
                masked_bits[i] = 'X'
        
        # Generate all combinations for floating bits
        if self.floating_count == 0:
            return [int(''.join(masked_bits), 2)]
        
        addresses = []
        for combo in product(['0', '1'], repeat=self.floating_count):
            result_bits = masked_bits[:]
            for pos, bit_value in zip(self.floating_positions, combo):
                result_bits[pos] = bit_value
            addresses.append(int(''.join(result_bits), 2))
        
        return addresses
    
    def __str__(self) -> str:
        return self.mask
    
    def __repr__(self) -> str:
        return f"BitMask('{self.mask}')"


class Memory:
    """
    Memory system that supports different addressing modes.
    """
    
    def __init__(self, addressing_mode: str = 'value'):
        """
        Initialize memory system.
        
        Args:
            addressing_mode: 'value' for Part 1, 'address' for Part 2
        """
        self.memory: Dict[int, int] = {}
        self.addressing_mode = addressing_mode
        self.current_mask: Optional[BitMask] = None
        self.operations_log: List[Dict[str, Any]] = []
    
    def set_mask(self, mask: BitMask) -> None:
        """
        Set the current bitmask.
        
        Args:
            mask: BitMask to use for subsequent operations
        """
        self.current_mask = mask
        self.operations_log.append({
            'type': 'mask',
            'mask': str(mask),
            'floating_bits': mask.floating_count
        })
    
    def write(self, address: int, value: int) -> None:
        """
        Write value to memory using current addressing mode.
        
        Args:
            address: Memory address
            value: Value to write
        """
        if self.current_mask is None:
            raise ValueError("No mask set")
        
        if self.addressing_mode == 'value':
            # Part 1: Apply mask to value
            masked_value = self.current_mask.apply_to_value(value)
            self.memory[address] = masked_value
            
            self.operations_log.append({
                'type': 'write_value',
                'address': address,
                'original_value': value,
                'masked_value': masked_value
            })
            
        elif self.addressing_mode == 'address':
            # Part 2: Apply mask to address
            masked_addresses = self.current_mask.apply_to_address(address)
            
            for addr in masked_addresses:
                self.memory[addr] = value
            
            self.operations_log.append({
                'type': 'write_address',
                'original_address': address,
                'masked_addresses': masked_addresses,
                'value': value,
                'addresses_written': len(masked_addresses)
            })
        
        else:
            raise ValueError(f"Unknown addressing mode: {self.addressing_mode}")
    
    def sum_values(self) -> int:
        """
        Calculate sum of all values in memory.
        
        Returns:
            Sum of all memory values
        """
        return sum(self.memory.values())
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """
        Get memory usage statistics.
        
        Returns:
            Dictionary with memory statistics
        """
        return {
            'addresses_used': len(self.memory),
            'total_value': self.sum_values(),
            'min_address': min(self.memory.keys()) if self.memory else 0,
            'max_address': max(self.memory.keys()) if self.memory else 0,
            'operations_count': len(self.operations_log)
        }
    
    def clear(self) -> None:
        """Clear all memory and operation logs."""
        self.memory.clear()
        self.operations_log.clear()
        self.current_mask = None


class DockingComputer:
    """
    Manages the docking computer's memory operations.
    """
    
    def __init__(self, program: str, addressing_mode: str = 'value'):
        """
        Initialize docking computer.
        
        Args:
            program: Program instructions as string
            addressing_mode: 'value' for Part 1, 'address' for Part 2
        """
        self.program = program
        self.memory = Memory(addressing_mode)
        self.instructions = self._parse_program()
    
    def _parse_program(self) -> List[Dict[str, Any]]:
        """
        Parse program instructions.
        
        Returns:
            List of parsed instructions
        """
        instructions = []
        
        for line in self.program.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('mask = '):
                mask_str = line.split('= ')[1]
                instructions.append({
                    'type': 'mask',
                    'mask': mask_str
                })
            
            elif line.startswith('mem['):
                # Parse mem[address] = value
                match = re.match(r'mem\[(\d+)\] = (\d+)', line)
                if match:
                    address = int(match.group(1))
                    value = int(match.group(2))
                    instructions.append({
                        'type': 'write',
                        'address': address,
                        'value': value
                    })
                else:
                    raise ValueError(f"Invalid memory instruction: {line}")
            
            else:
                raise ValueError(f"Unknown instruction: {line}")
        
        return instructions
    
    def execute(self) -> int:
        """
        Execute the program and return sum of memory values.
        
        Returns:
            Sum of all values in memory after execution
        """
        self.memory.clear()
        
        for instruction in self.instructions:
            if instruction['type'] == 'mask':
                mask = BitMask(instruction['mask'])
                self.memory.set_mask(mask)
            
            elif instruction['type'] == 'write':
                self.memory.write(instruction['address'], instruction['value'])
        
        return self.memory.sum_values()
    
    def get_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis of the program execution.
        
        Returns:
            Analysis results
        """
        memory_stats = self.memory.get_memory_usage()
        
        mask_instructions = [i for i in self.instructions if i['type'] == 'mask']
        write_instructions = [i for i in self.instructions if i['type'] == 'write']
        
        return {
            'addressing_mode': self.memory.addressing_mode,
            'instructions': {
                'total': len(self.instructions),
                'mask_changes': len(mask_instructions),
                'memory_writes': len(write_instructions)
            },
            'memory': memory_stats,
            'masks_used': [instr['mask'] for instr in mask_instructions],
            'complexity': {
                'unique_masks': len(set(instr['mask'] for instr in mask_instructions)),
                'avg_floating_bits': self._calculate_avg_floating_bits(mask_instructions)
            }
        }
    
    def _calculate_avg_floating_bits(self, mask_instructions: List[Dict[str, Any]]) -> float:
        """Calculate average number of floating bits across all masks."""
        if not mask_instructions:
            return 0.0
        
        total_floating = sum(mask['mask'].count('X') for mask in mask_instructions)
        return total_floating / len(mask_instructions)


class Day14Solution(AdventSolution):
    """Solution for Advent of Code 2020 Day 14: Docking Data."""
    
    def __init__(self):
        super().__init__(year=2020, day=14, title="Docking Data")
    
    def part1(self, input_data: str) -> Any:
        """
        Solve part 1: Apply bitmask to values before storing.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Sum of all values in memory
        """
        computer = DockingComputer(input_data, addressing_mode='value')
        return computer.execute()
    
    def part2(self, input_data: str) -> Any:
        """
        Solve part 2: Apply bitmask to memory addresses.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Sum of all values in memory
        """
        computer = DockingComputer(input_data, addressing_mode='address')
        return computer.execute()
    
    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Provide comprehensive analysis of the docking data problem.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis results for both parts
        """
        # Analyze both parts
        computer_v1 = DockingComputer(input_data, addressing_mode='value')
        part1_result = computer_v1.execute()
        part1_analysis = computer_v1.get_analysis()
        
        computer_v2 = DockingComputer(input_data, addressing_mode='address')
        part2_result = computer_v2.execute()
        part2_analysis = computer_v2.get_analysis()
        
        return {
            'part1': {
                'result': part1_result,
                'analysis': part1_analysis,
                'method': 'value_masking'
            },
            'part2': {
                'result': part2_result,
                'analysis': part2_analysis,
                'method': 'address_masking'
            },
            'comparison': {
                'memory_addresses_part1': part1_analysis['memory']['addresses_used'],
                'memory_addresses_part2': part2_analysis['memory']['addresses_used'],
                'complexity_difference': part2_analysis['memory']['addresses_used'] / max(1, part1_analysis['memory']['addresses_used'])
            },
            'algorithm': {
                'part1_complexity': 'O(n) where n is number of instructions',
                'part2_complexity': 'O(n * 2^f) where f is floating bits per mask',
                'floating_bit_impact': f"Each X bit doubles the address space"
            }
        }


# Legacy compatibility functions for test runner
def part1(filename: str) -> Any:
    """Legacy function for part 1."""
    with open(filename, 'r') as f:
        input_data = f.read()
    
    solution = Day14Solution()
    return solution.part1(input_data)


def part2(filename: str) -> Any:
    """Legacy function for part 2."""
    with open(filename, 'r') as f:
        input_data = f.read()
    
    solution = Day14Solution()
    return solution.part2(input_data)


if __name__ == "__main__":
    solution = Day14Solution()
    solution.main()
