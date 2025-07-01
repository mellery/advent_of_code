#!/usr/bin/env python3
"""
Advent of Code 2020 Day 23: Crab Cups (OPTIMIZED)

High-performance cup shuffling simulation with major optimizations:
- Array-based linked list (no dictionary overhead)
- Eliminated all progress printing
- Minimized object allocations
- Optimized destination finding
- Inlined critical operations

Performance target: <5 seconds for 10M moves
"""

import sys
import os
from typing import List, Tuple, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.advent_base import AdventSolution


def optimized_cup_game(initial_cups: List[int], total_cups: int, num_moves: int) -> List[int]:
    """
    Highly optimized cup game simulation using array-based linked list.
    
    Returns the final linked list representation.
    """
    # Use array instead of dictionary for O(1) access without hash overhead
    # next_cup[i] = the cup that comes after cup i
    next_cup = [0] * (total_cups + 1)  # 1-indexed
    
    # Set up initial cups
    cups = initial_cups.copy()
    if total_cups > len(initial_cups):
        max_initial = max(initial_cups)
        cups.extend(range(max_initial + 1, total_cups + 1))
    
    # Build linked list
    for i in range(len(cups)):
        current = cups[i]
        next_pos = cups[(i + 1) % len(cups)]
        next_cup[current] = next_pos
    
    current_cup = cups[0]
    max_cup = total_cups
    
    # Main game loop with all optimizations inlined
    for _ in range(num_moves):
        # Pick up three cups (inlined for performance)
        pickup1 = next_cup[current_cup]
        pickup2 = next_cup[pickup1]
        pickup3 = next_cup[pickup2]
        
        # Remove picked up cups from circle
        next_cup[current_cup] = next_cup[pickup3]
        
        # Find destination (optimized)
        destination = current_cup - 1
        if destination == 0:
            destination = max_cup
        
        # Optimized destination finding - avoid repeated checks
        while destination == pickup1 or destination == pickup2 or destination == pickup3:
            destination -= 1
            if destination == 0:
                destination = max_cup
        
        # Insert picked up cups after destination
        temp_next = next_cup[destination]
        next_cup[destination] = pickup1
        next_cup[pickup3] = temp_next
        
        # Move to next current cup
        current_cup = next_cup[current_cup]
    
    return next_cup


def get_cups_after_one(next_cup: List[int], count: int) -> str:
    """Get cups after cup 1 as string."""
    result = []
    current = next_cup[1]
    for _ in range(count):
        result.append(str(current))
        current = next_cup[current]
    return ''.join(result)


def get_two_cups_after_one(next_cup: List[int]) -> Tuple[int, int]:
    """Get the two cups immediately after cup 1."""
    cup1 = next_cup[1]
    cup2 = next_cup[cup1]
    return cup1, cup2


class Day23OptimizedSolution(AdventSolution):
    """Optimized solution for Advent of Code 2020 Day 23."""
    
    def __init__(self):
        super().__init__(year=2020, day=23, title="Crab Cups (Optimized)")
    
    def parse_cups(self, input_data: str) -> List[int]:
        """Parse initial cup arrangement efficiently."""
        cups_str = input_data.strip().replace('\n', '').replace(' ', '')
        return [int(d) for d in cups_str]
    
    def part1(self, input_data: str) -> Any:
        """Part 1: Play 100 moves and return cups after cup 1."""
        cups = self.parse_cups(input_data)
        next_cup = optimized_cup_game(cups, len(cups), 100)
        return get_cups_after_one(next_cup, len(cups) - 1)
    
    def part2(self, input_data: str) -> Any:
        """Part 2: Play 10M moves with 1M cups."""
        cups = self.parse_cups(input_data)
        next_cup = optimized_cup_game(cups, 1000000, 10000000)
        cup1, cup2 = get_two_cups_after_one(next_cup)
        return cup1 * cup2


def main():
    """Main execution function."""
    solution = Day23OptimizedSolution()
    solution.main()


if __name__ == "__main__":
    main()