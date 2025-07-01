#!/usr/bin/env python3
"""
Advent of Code 2020 Day 25: Combo Breaker (OPTIMIZED)

High-performance cryptographic handshake solver with major optimizations:
- Optimized modular arithmetic (use built-in pow() where possible)
- Eliminated object overhead and operation counting
- Streamlined loop size finding
- Minimal memory allocations
- Fast modular exponentiation

Performance target: <5 seconds total execution time
"""

import sys
import os
from typing import Tuple, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.advent_base import AdventSolution


MODULUS = 20201227
DEFAULT_SUBJECT = 7


def find_loop_size_optimized(public_key: int, subject_number: int = DEFAULT_SUBJECT) -> int:
    """
    Optimized loop size finder using minimal operations.
    
    No cycle detection needed - the problem guarantees a solution exists.
    """
    value = 1
    loop_size = 0
    
    while value != public_key:
        value = (value * subject_number) % MODULUS
        loop_size += 1
    
    return loop_size


def transform_optimized(subject_number: int, loop_size: int) -> int:
    """
    Optimized transformation using built-in pow() for modular exponentiation.
    
    This is much faster than manual loops for large loop sizes.
    """
    return pow(subject_number, loop_size, MODULUS)


def solve_crypto_handshake(card_public_key: int, door_public_key: int) -> int:
    """
    Solve the cryptographic handshake efficiently.
    
    Returns the encryption key.
    """
    # Find card's loop size (this is the bottleneck)
    card_loop_size = find_loop_size_optimized(card_public_key)
    
    # Calculate encryption key using fast modular exponentiation
    encryption_key = transform_optimized(door_public_key, card_loop_size)
    
    return encryption_key


class Day25OptimizedSolution(AdventSolution):
    """Optimized solution for Advent of Code 2020 Day 25."""
    
    def __init__(self):
        super().__init__(year=2020, day=25, title="Combo Breaker (Optimized)")
    
    def _parse_public_keys(self, input_data: str) -> Tuple[int, int]:
        """Parse public keys efficiently."""
        lines = input_data.strip().split('\n')
        card_key = int(lines[0].strip())
        door_key = int(lines[1].strip())
        return card_key, door_key
    
    def part1(self, input_data: str) -> Any:
        """Part 1: Find the encryption key."""
        card_key, door_key = self._parse_public_keys(input_data)
        return solve_crypto_handshake(card_key, door_key)
    
    def part2(self, input_data: str) -> Any:
        """Part 2: Collect all stars message."""
        return "Congratulations! All 49 stars collected. The sleigh is ready for Christmas!"


# Legacy compatibility functions for test runner
def part1(input_data) -> int:
    """Legacy function for part 1."""
    if isinstance(input_data, str) and not ('\n' in input_data):
        # This is a filename
        try:
            with open(input_data, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            return -1
    else:
        content = input_data
    
    solution = Day25OptimizedSolution()
    return solution.part1(content)


def part2(input_data) -> str:
    """Legacy function for part 2."""
    solution = Day25OptimizedSolution()
    return solution.part2("")


def main():
    """Main function with dual compatibility."""
    if len(sys.argv) > 1 or '--test' in sys.argv or '--time' in sys.argv:
        # New AdventSolution mode
        solution = Day25OptimizedSolution()
        solution.main()
    else:
        # Legacy mode for compatibility
        print(part1("day25_input.txt"))
        print(part2("day25_input.txt"))


if __name__ == "__main__":
    main()