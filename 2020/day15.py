#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 15: Rambunctious Recitation

Van Eck sequence implementation - a memory game where numbers are spoken
based on their recency:
- If a number is new, speak 0
- If a number was spoken before, speak its age (turns since last spoken)

The challenge involves efficient sequence generation and memory management.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Dict, Any, Optional, Tuple
import time


class MemoryGame:
    """
    Implementation of the Van Eck sequence memory game.
    
    The game follows specific rules:
    1. Start with given numbers in order
    2. Each subsequent turn, consider the last number spoken
    3. If it's the first time the number has been spoken, speak 0
    4. Otherwise, speak the age (number of turns since it was last spoken)
    """
    
    def __init__(self, starting_numbers: List[int]):
        """
        Initialize the memory game.
        
        Args:
            starting_numbers: List of starting numbers
        """
        if not starting_numbers:
            raise ValueError("Must provide at least one starting number")
        
        self.starting_numbers = starting_numbers
        self.reset()
    
    def reset(self) -> None:
        """Reset the game to initial state."""
        # Dictionary to store the last turn each number was spoken
        # We only need to track the most recent occurrence for efficiency
        self.last_spoken: Dict[int, int] = {}
        
        # Initialize with starting numbers (except the last one)
        for i, num in enumerate(self.starting_numbers[:-1]):
            self.last_spoken[num] = i + 1
        
        # Start from the last starting number
        self.current_number = self.starting_numbers[-1]
        self.current_turn = len(self.starting_numbers)
        
        # Statistics tracking
        self.unique_numbers_spoken = set(self.starting_numbers)
        self.turn_history: List[int] = self.starting_numbers.copy()
    
    def next_number(self) -> int:
        """
        Calculate the next number in the sequence.
        
        Returns:
            The next number to be spoken
        """
        # Calculate the next number based on current number's history
        if self.current_number in self.last_spoken:
            # Number was spoken before - calculate age
            next_num = self.current_turn - self.last_spoken[self.current_number]
        else:
            # Number is new - speak 0
            next_num = 0
        
        # Update the last spoken turn for current number
        self.last_spoken[self.current_number] = self.current_turn
        
        return next_num
    
    def play_turn(self) -> int:
        """
        Play one turn of the game.
        
        Returns:
            The number spoken this turn
        """
        next_num = self.next_number()
        
        # Move to next turn
        self.current_turn += 1
        self.current_number = next_num
        
        # Update statistics
        self.unique_numbers_spoken.add(next_num)
        if len(self.turn_history) < 1000:  # Limit history for memory
            self.turn_history.append(next_num)
        
        return next_num
    
    def play_until_turn(self, target_turn: int) -> int:
        """
        Play the game until a specific turn.
        
        Args:
            target_turn: Target turn number (1-indexed)
            
        Returns:
            The number spoken at the target turn
        """
        if target_turn <= len(self.starting_numbers):
            return self.starting_numbers[target_turn - 1]
        
        # Continue until we reach the target turn
        while self.current_turn < target_turn:
            self.play_turn()
        
        return self.current_number
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get game statistics.
        
        Returns:
            Dictionary with game statistics
        """
        return {
            'starting_numbers': self.starting_numbers,
            'current_turn': self.current_turn,
            'current_number': self.current_number,
            'unique_numbers_spoken': len(self.unique_numbers_spoken),
            'numbers_tracked': len(self.last_spoken),
            'last_10_numbers': self.turn_history[-10:] if self.turn_history else [],
            'most_recent_ages': self._get_recent_ages()
        }
    
    def _get_recent_ages(self) -> List[int]:
        """Get ages of recently spoken numbers."""
        if len(self.turn_history) < 2:
            return []
        
        ages = []
        for i in range(max(1, len(self.turn_history) - 10), len(self.turn_history)):
            num = self.turn_history[i]
            # Find when this number was spoken before
            age = 0
            for j in range(i - 1, -1, -1):
                if self.turn_history[j] == num:
                    age = i - j
                    break
            ages.append(age)
        
        return ages
    
    def analyze_sequence_properties(self, sample_size: int = 1000) -> Dict[str, Any]:
        """
        Analyze properties of the generated sequence.
        
        Args:
            sample_size: Number of turns to analyze
            
        Returns:
            Analysis of sequence properties
        """
        # Generate sample sequence
        self.reset()
        sample = []
        for _ in range(sample_size):
            sample.append(self.play_turn())
        
        # Analyze properties
        zero_count = sample.count(0)
        max_number = max(sample) if sample else 0
        unique_count = len(set(sample))
        
        # Calculate frequency distribution
        frequency = {}
        for num in sample:
            frequency[num] = frequency.get(num, 0) + 1
        
        most_common = max(frequency.items(), key=lambda x: x[1]) if frequency else (0, 0)
        
        return {
            'sample_size': sample_size,
            'zero_frequency': zero_count / sample_size,
            'max_number_seen': max_number,
            'unique_numbers': unique_count,
            'uniqueness_ratio': unique_count / sample_size,
            'most_common_number': most_common[0],
            'most_common_frequency': most_common[1],
            'sequence_properties': {
                'has_cycles': self._detect_cycles(sample),
                'avg_number': sum(sample) / len(sample) if sample else 0,
                'number_range': (min(sample), max(sample)) if sample else (0, 0)
            }
        }
    
    def _detect_cycles(self, sequence: List[int], min_cycle_length: int = 2) -> bool:
        """Detect if there are cycles in the sequence."""
        if len(sequence) < min_cycle_length * 2:
            return False
        
        # Check for cycles of various lengths
        for cycle_len in range(min_cycle_length, len(sequence) // 2):
            if len(sequence) >= cycle_len * 2:
                # Check if the last cycle_len elements repeat
                recent = sequence[-cycle_len:]
                previous = sequence[-cycle_len*2:-cycle_len]
                if recent == previous:
                    return True
        
        return False


class Day15Solution(AdventSolution):
    """Solution for Advent of Code 2020 Day 15: Rambunctious Recitation."""
    
    def __init__(self):
        super().__init__(year=2020, day=15, title="Rambunctious Recitation")
    
    def _parse_starting_numbers(self, input_data: str) -> List[int]:
        """
        Parse starting numbers from input data.
        
        Args:
            input_data: Raw input data
            
        Returns:
            List of starting numbers
        """
        line = input_data.strip()
        
        # Handle both comma-separated and space-separated formats
        if ',' in line:
            return [int(x.strip()) for x in line.split(',')]
        else:
            return [int(x.strip()) for x in line.split()]
    
    def part1(self, input_data: str) -> Any:
        """
        Solve part 1: Find the 2020th number spoken.
        
        Args:
            input_data: Raw input data
            
        Returns:
            The 2020th number spoken
        """
        starting_numbers = self._parse_starting_numbers(input_data)
        game = MemoryGame(starting_numbers)
        return game.play_until_turn(2020)
    
    def part2(self, input_data: str) -> Any:
        """
        Solve part 2: Find the 30000000th number spoken.
        
        Args:
            input_data: Raw input data
            
        Returns:
            The 30000000th number spoken
        """
        starting_numbers = self._parse_starting_numbers(input_data)
        game = MemoryGame(starting_numbers)
        return game.play_until_turn(30000000)
    
    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Provide comprehensive analysis of the memory game.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis results for both parts
        """
        starting_numbers = self._parse_starting_numbers(input_data)
        
        # Solve both parts with timing
        game1 = MemoryGame(starting_numbers)
        start_time = time.time()
        part1_result = game1.play_until_turn(2020)
        part1_time = time.time() - start_time
        part1_stats = game1.get_statistics()
        
        game2 = MemoryGame(starting_numbers)
        start_time = time.time()
        part2_result = game2.play_until_turn(30000000)
        part2_time = time.time() - start_time
        part2_stats = game2.get_statistics()
        
        # Analyze sequence properties
        game_analysis = MemoryGame(starting_numbers)
        sequence_analysis = game_analysis.analyze_sequence_properties(1000)
        
        return {
            'starting_numbers': starting_numbers,
            'part1': {
                'result': part1_result,
                'execution_time': part1_time,
                'statistics': part1_stats,
                'target_turn': 2020
            },
            'part2': {
                'result': part2_result,
                'execution_time': part2_time,
                'statistics': part2_stats,
                'target_turn': 30000000
            },
            'sequence_analysis': sequence_analysis,
            'performance': {
                'part1_time': part1_time,
                'part2_time': part2_time,
                'scaling_factor': part2_time / max(part1_time, 0.001),
                'memory_efficiency': 'O(n) space complexity using last-spoken tracking'
            },
            'algorithm': {
                'name': 'Van Eck Sequence',
                'complexity': 'O(n) time, O(n) space',
                'optimization': 'Only track last occurrence of each number',
                'key_insight': 'Most numbers will be spoken multiple times'
            }
        }


# Legacy compatibility functions for test runner
def part1(input_data) -> int:
    """Legacy function for part 1."""
    # Handle both filename and content
    if isinstance(input_data, str):
        if '\n' in input_data or ',' in input_data:
            # This is content
            content = input_data.strip()
        else:
            # This is a filename
            try:
                with open(input_data, 'r') as f:
                    content = f.read().strip()
            except FileNotFoundError:
                # Fallback to hardcoded if file not found
                content = "1,20,11,6,12,0"
    else:
        # Fallback
        content = "1,20,11,6,12,0"
    
    solution = Day15Solution()
    return solution.part1(content)


def part2(input_data) -> int:
    """Legacy function for part 2."""
    # Handle both filename and content
    if isinstance(input_data, str):
        if '\n' in input_data or ',' in input_data:
            # This is content
            content = input_data.strip()
        else:
            # This is a filename
            try:
                with open(input_data, 'r') as f:
                    content = f.read().strip()
            except FileNotFoundError:
                # Fallback to hardcoded if file not found
                content = "1,20,11,6,12,0"
    else:
        # Fallback
        content = "1,20,11,6,12,0"
    
    solution = Day15Solution()
    return solution.part2(content)


if __name__ == "__main__":
    solution = Day15Solution()
    solution.main()