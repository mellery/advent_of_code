#!/usr/bin/env python3
"""
Advent of Code 2020 Day 23: Crab Cups
https://adventofcode.com/2020/day/23

Cup shuffling game simulation using linked list optimization for large-scale moves.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class CupGame:
    """Manages the Crab Cups game with efficient linked list implementation."""
    
    def __init__(self, initial_cups: List[int], total_cups: int = None):
        """
        Initialize the cup game.
        
        Args:
            initial_cups: The initial arrangement of cups
            total_cups: Total number of cups (extends with sequential numbers if > len(initial_cups))
        """
        self.initial_cups = initial_cups.copy()
        
        # Extend to total_cups if specified
        if total_cups and total_cups > len(initial_cups):
            max_cup = max(initial_cups)
            extended_cups = initial_cups.copy()
            for i in range(max_cup + 1, total_cups + 1):
                extended_cups.append(i)
            self.cups = extended_cups
        else:
            self.cups = initial_cups.copy()
        
        self.total_cups = len(self.cups)
        self.max_cup = max(self.cups)
        
        # Create linked list representation for O(1) operations
        # next_cup[i] = the cup that comes after cup i
        self.next_cup = {}
        for i in range(len(self.cups)):
            current_cup = self.cups[i]
            next_cup = self.cups[(i + 1) % len(self.cups)]
            self.next_cup[current_cup] = next_cup
        
        self.current_cup = self.cups[0]
        self.moves_made = 0
    
    def play_moves(self, num_moves: int, progress_interval: int = 100000):
        """
        Play the specified number of moves.
        
        Args:
            num_moves: Number of moves to play
            progress_interval: How often to print progress (0 to disable)
        """
        for move in range(num_moves):
            if progress_interval > 0 and move % progress_interval == 0 and move > 0:
                print(f"-- move: {move + 1} --")
            
            self._play_single_move()
        
        self.moves_made += num_moves
    
    def _play_single_move(self):
        """Play a single move of the game."""
        # Pick up the three cups clockwise from current cup
        pickup1 = self.next_cup[self.current_cup]
        pickup2 = self.next_cup[pickup1]
        pickup3 = self.next_cup[pickup2]
        picked_up = [pickup1, pickup2, pickup3]
        
        # Remove picked up cups from the circle
        self.next_cup[self.current_cup] = self.next_cup[pickup3]
        
        # Find destination cup
        destination = self.current_cup - 1
        if destination == 0:
            destination = self.max_cup
        
        # Keep decrementing until we find a cup not in picked_up
        while destination in picked_up:
            destination -= 1
            if destination == 0:
                destination = self.max_cup
        
        # Insert picked up cups after destination
        temp_next = self.next_cup[destination]
        self.next_cup[destination] = pickup1
        self.next_cup[pickup3] = temp_next
        
        # Move to next current cup
        self.current_cup = self.next_cup[self.current_cup]
    
    def get_cup_order_from(self, start_cup: int, count: int = None) -> List[int]:
        """
        Get the order of cups starting from a specific cup.
        
        Args:
            start_cup: The cup to start from
            count: Number of cups to return (None for all)
            
        Returns:
            List of cups in order
        """
        if count is None:
            count = self.total_cups
        
        result = []
        current = start_cup
        for _ in range(count):
            result.append(current)
            current = self.next_cup[current]
        
        return result
    
    def get_cups_after_one(self) -> str:
        """Get the arrangement of cups after cup 1 as a string."""
        cups_after_one = self.get_cup_order_from(1, self.total_cups)[1:]  # Skip cup 1 itself
        return ''.join(map(str, cups_after_one))
    
    def get_two_cups_after_one(self) -> tuple:
        """Get the two cups immediately after cup 1."""
        cup1 = self.next_cup[1]
        cup2 = self.next_cup[cup1]
        return cup1, cup2
    
    def get_game_state_summary(self) -> str:
        """Get a summary of the current game state."""
        if self.total_cups <= 20:  # Only show full state for small games
            current_order = self.get_cup_order_from(self.current_cup)
            formatted_cups = []
            for i, cup in enumerate(current_order):
                if i == 0:  # Current cup
                    formatted_cups.append(f"({cup})")
                else:
                    formatted_cups.append(str(cup))
            
            return f"cups: {' '.join(formatted_cups)}"
        else:
            # For large games, just show key information
            cup1, cup2 = self.get_two_cups_after_one()
            return f"Moves: {self.moves_made}, Current: {self.current_cup}, After cup 1: {cup1}, {cup2}"


class Day23Solution(AdventSolution):
    """Solution for 2020 Day 23: Crab Cups."""

    def __init__(self):
        super().__init__(2020, 23, "Crab Cups")

    def parse_cups(self, input_data: str) -> List[int]:
        """
        Parse initial cup arrangement from input.
        
        Args:
            input_data: Raw input data (string of digits)
            
        Returns:
            List of cup numbers
        """
        # Handle both single line input and potential multi-line
        cups_str = input_data.strip().replace('\n', '').replace(' ', '')
        return [int(d) for d in cups_str]

    def part1(self, input_data: str) -> str:
        """
        Solve part 1: Play 100 moves and return cups after cup 1.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            String of cups after cup 1
        """
        cups = self.parse_cups(input_data)
        game = CupGame(cups)
        game.play_moves(100, progress_interval=0)  # No progress for small games
        return game.get_cups_after_one()

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Play 10M moves with 1M cups, multiply two cups after cup 1.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Product of the two cups after cup 1
        """
        cups = self.parse_cups(input_data)
        game = CupGame(cups, total_cups=1000000)
        game.play_moves(10000000, progress_interval=100000)
        
        cup1, cup2 = game.get_two_cups_after_one()
        return cup1 * cup2

    def analyze_game(self, input_data: str, moves: int = 100) -> str:
        """
        Analyze the cup game progression.
        
        Args:
            input_data: Raw input data
            moves: Number of moves to analyze
            
        Returns:
            Analysis summary as formatted string
        """
        cups = self.parse_cups(input_data)
        
        analysis = []
        analysis.append("=== Crab Cups Analysis ===")
        analysis.append(f"Initial cups: {cups}")
        analysis.append(f"Total cups: {len(cups)}")
        analysis.append(f"Moves to simulate: {moves}")
        
        game = CupGame(cups)
        
        # Show initial state
        analysis.append(f"\nInitial state: {game.get_game_state_summary()}")
        
        # Show progression for small number of moves
        if moves <= 10:
            for move in range(1, moves + 1):
                game.play_moves(1, progress_interval=0)
                analysis.append(f"After move {move}: {game.get_game_state_summary()}")
        else:
            # For larger games, show key milestones
            milestones = [1, 10, 100] if moves >= 100 else [1, moves // 2, moves]
            for milestone in milestones:
                if milestone <= moves:
                    target_moves = milestone - game.moves_made
                    if target_moves > 0:
                        game.play_moves(target_moves, progress_interval=0)
                    analysis.append(f"After move {milestone}: {game.get_game_state_summary()}")
        
        # Final result
        if game.moves_made < moves:
            game.play_moves(moves - game.moves_made, progress_interval=0)
        
        analysis.append(f"\nFinal result after {moves} moves:")
        analysis.append(f"Cups after cup 1: {game.get_cups_after_one()}")
        
        return "\n".join(analysis)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test with example from problem description
        test_input = "389125467"
        
        cups = self.parse_cups(test_input)
        
        # Validate parsing
        if cups != [3, 8, 9, 1, 2, 5, 4, 6, 7]:
            print(f"Parsing test failed: expected [3, 8, 9, 1, 2, 5, 4, 6, 7], got {cups}")
            return False
        
        # Test small number of moves
        game = CupGame(cups)
        game.play_moves(10, progress_interval=0)
        
        expected_after_10 = game.get_cups_after_one()
        if expected_after_10 != "92658374":
            print(f"10 moves test failed: expected '92658374', got '{expected_after_10}'")
            return False
        
        # Test part 1 (100 moves)
        game = CupGame(cups)
        game.play_moves(100, progress_interval=0)
        part1_result = game.get_cups_after_one()
        
        if part1_result != "67384529":
            print(f"Part 1 test failed: expected '67384529', got '{part1_result}'")
            return False
        
        # Test part 2 setup (just verify the structure, not the full computation)
        large_game = CupGame(cups, total_cups=1000000)
        if large_game.total_cups != 1000000:
            print(f"Part 2 setup failed: expected 1000000 cups, got {large_game.total_cups}")
            return False
        
        # Verify the extension worked correctly
        if large_game.next_cup[7] != 10:  # Cup 7 should connect to cup 10
            print(f"Part 2 extension failed: cup 7 should connect to 10, got {large_game.next_cup[7]}")
            return False
        
        print("✅ All Day 23 validation tests passed!")
        return True


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> str:
    """Part 1 function compatible with test runner."""
    solution = Day23Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day23Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main function to run the solution."""
    solution = Day23Solution()
    solution.main()


if __name__ == "__main__":
    main()