#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 16: Packet Decoder

Decoding nested packets from a binary transmission.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    get_lines, setup_day_args, find_input_file, validate_solution, run_solution
)
from utils.advent_base import AdventSolution
from typing import Any, List, Tuple
import operator


class Packet:
    """Represents a BITS packet with version, type ID, and value or sub-packets."""
    
    def __init__(self, binary_data: str, start: int = 0):
        self.version = int(binary_data[start:start+3], 2)
        self.type_id = int(binary_data[start+3:start+6], 2)
        self.sub_packets = []
        self.value = 0
        self.length = 0  # Total bits consumed by this packet
        
        if self.type_id == 4:  # Literal value
            self._parse_literal(binary_data, start + 6)
        else:  # Operator packet
            self._parse_operator(binary_data, start + 6)
    
    def _parse_literal(self, binary_data: str, start: int):
        """Parse a literal value packet."""
        value_bits = ""
        pos = start
        
        while pos < len(binary_data):
            group = binary_data[pos:pos+5]
            if len(group) < 5:
                break
                
            value_bits += group[1:5]  # Skip the first bit (continuation bit)
            pos += 5
            
            if group[0] == '0':  # Last group
                break
        
        self.value = int(value_bits, 2) if value_bits else 0
        self.length = pos - start + 6  # Include header (6 bits)
    
    def _parse_operator(self, binary_data: str, start: int):
        """Parse an operator packet."""
        length_type_id = binary_data[start]
        pos = start + 1
        
        if length_type_id == '0':  # Next 15 bits are total length of sub-packets
            sub_packet_length = int(binary_data[pos:pos+15], 2)
            pos += 15
            
            sub_packets_data = binary_data[pos:pos+sub_packet_length]
            sub_pos = 0
            
            while sub_pos < len(sub_packets_data):
                try:
                    packet = Packet(sub_packets_data, sub_pos)
                    if packet.length == 0:  # Invalid packet
                        break
                    self.sub_packets.append(packet)
                    sub_pos += packet.length
                except (ValueError, IndexError):
                    break
            
            self.length = pos + sub_packet_length - start + 6
            
        else:  # Next 11 bits are number of sub-packets
            num_sub_packets = int(binary_data[pos:pos+11], 2)
            pos += 11
            
            for _ in range(num_sub_packets):
                try:
                    packet = Packet(binary_data, pos)
                    if packet.length == 0:  # Invalid packet
                        break
                    self.sub_packets.append(packet)
                    pos += packet.length
                except (ValueError, IndexError):
                    break
            
            self.length = pos - start + 6
        
        # Calculate the value based on type ID
        self._calculate_value()
    
    def _calculate_value(self):
        """Calculate the value of an operator packet based on its type ID."""
        if not self.sub_packets:
            self.value = 0
            return
        
        sub_values = [packet.get_value() for packet in self.sub_packets]
        
        if self.type_id == 0:  # Sum
            self.value = sum(sub_values)
        elif self.type_id == 1:  # Product
            self.value = 1
            for val in sub_values:
                self.value *= val
        elif self.type_id == 2:  # Minimum
            self.value = min(sub_values)
        elif self.type_id == 3:  # Maximum
            self.value = max(sub_values)
        elif self.type_id == 5:  # Greater than
            self.value = 1 if sub_values[0] > sub_values[1] else 0
        elif self.type_id == 6:  # Less than
            self.value = 1 if sub_values[0] < sub_values[1] else 0
        elif self.type_id == 7:  # Equal to
            self.value = 1 if sub_values[0] == sub_values[1] else 0
    
    def get_version_sum(self) -> int:
        """Get the sum of version numbers for this packet and all sub-packets."""
        total = self.version
        for packet in self.sub_packets:
            total += packet.get_version_sum()
        return total
    
    def get_value(self) -> int:
        """Get the calculated value of this packet."""
        return self.value


def hex_to_binary(hex_string: str) -> str:
    """Convert hexadecimal string to binary string."""
    # Remove any whitespace and convert to uppercase
    hex_string = hex_string.strip().upper()
    
    # Convert each hex digit to 4-bit binary
    binary = ""
    for hex_digit in hex_string:
        if hex_digit in "0123456789ABCDEF":
            binary += format(int(hex_digit, 16), '04b')
    
    return binary


def parse_transmission(hex_input: str) -> Packet:
    """Parse a hexadecimal transmission into a packet."""
    binary_data = hex_to_binary(hex_input)
    return Packet(binary_data)


class Day16Solution(AdventSolution):
    """Day 16: Packet Decoder"""
    
    def __init__(self):
        super().__init__(2021, 16, "Packet Decoder")
    
    def part1(self, filename: str) -> Any:
        """
        Sum the version numbers in all packets.
        
        Args:
            filename: Path to the input file
            
        Returns:
            Sum of all version numbers in the transmission
        """
        lines = get_lines(filename)
        hex_input = lines[0].strip()
        
        packet = parse_transmission(hex_input)
        return packet.get_version_sum()
    
    def part2(self, filename: str) -> Any:
        """
        Evaluate the expression represented by the packet hierarchy.
        
        Args:
            filename: Path to the input file
            
        Returns:
            The value calculated by evaluating the outermost packet
        """
        lines = get_lines(filename)
        hex_input = lines[0].strip()
        
        packet = parse_transmission(hex_input)
        return packet.get_value()


# Legacy functions for backward compatibility
def part1(filename: str) -> Any:
    """Legacy function for part 1."""
    solution = Day16Solution()
    return solution.part1(filename)


def part2(filename: str) -> Any:
    """Legacy function for part 2."""
    solution = Day16Solution()
    return solution.part2(filename)


def main():
    """Main function to run the solution."""
    solution = Day16Solution()
    
    # Check if we're being called by the legacy test runner
    if len(sys.argv) > 1 and '--legacy' in sys.argv:
        # Legacy mode - use the old approach
        day = '16'
        args = setup_day_args(day)
        
        # Determine input file
        if args.use_test:
            input_file = args.test
        else:
            input_file = find_input_file(day) or args.input
        
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found")
            return
        
        print(f"Advent of Code 2021 - Day {day}")
        print(f"Using input file: {input_file}")
        print("-" * 40)
        
        # Run validation if test file exists
        test_file = args.test
        if os.path.exists(test_file) and not args.use_test:
            print("Running validation tests...")
            # Note: Test values would need to be determined from actual test cases
            validate_solution(part1, part2, test_file, 
                            expected_part1=None, expected_part2=None)
            print("-" * 40)
        
        # Run the actual solution
        run_solution(part1, part2, input_file, args)
    else:
        # Enhanced mode - use AdventSolution
        solution.run()


if __name__ == "__main__":
    main()