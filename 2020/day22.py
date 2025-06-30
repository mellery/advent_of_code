#!/usr/bin/env python3
"""
Advent of Code 2020 Day 22: Crab Combat
https://adventofcode.com/2020/day/22

Card game simulation with recursive combat rules.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, List, Tuple, Set
import copy

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class CrabCombat:
    """Manages the Crab Combat card game with both regular and recursive rules."""
    
    def __init__(self, player1_deck: List[int], player2_deck: List[int]):
        """
        Initialize the game with starting decks.
        
        Args:
            player1_deck: Player 1's starting deck
            player2_deck: Player 2's starting deck
        """
        self.original_deck1 = player1_deck.copy()
        self.original_deck2 = player2_deck.copy()
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.deck1 = self.original_deck1.copy()
        self.deck2 = self.original_deck2.copy()
        self.round_number = 0
        self.game_history = []
    
    def calculate_score(self, deck: List[int]) -> int:
        """
        Calculate the winning score for a deck.
        
        Args:
            deck: The deck to score
            
        Returns:
            The calculated score
        """
        score = 0
        size = len(deck)
        for card in deck:
            score += card * size
            size -= 1
        return score
    
    def play_regular_combat(self) -> Tuple[int, int, int]:
        """
        Play regular Combat until one player runs out of cards.
        
        Returns:
            Tuple of (winner, player1_score, player2_score)
        """
        self.reset_game()
        
        while len(self.deck1) > 0 and len(self.deck2) > 0:
            self.round_number += 1
            
            # Draw cards
            card1 = self.deck1.pop(0)
            card2 = self.deck2.pop(0)
            
            # Higher card wins
            if card1 > card2:
                self.deck1.extend([card1, card2])
            else:
                self.deck2.extend([card2, card1])
        
        # Determine winner and scores
        if len(self.deck1) > 0:
            winner = 1
            player1_score = self.calculate_score(self.deck1)
            player2_score = 0
        else:
            winner = 2
            player1_score = 0
            player2_score = self.calculate_score(self.deck2)
        
        return winner, player1_score, player2_score
    
    def play_recursive_combat(self) -> Tuple[int, int, int]:
        """
        Play Recursive Combat with sub-game rules.
        
        Returns:
            Tuple of (winner, player1_score, player2_score)
        """
        self.reset_game()
        winner = self._recursive_combat_game(self.deck1, self.deck2)[0]
        
        if winner == 1:
            player1_score = self.calculate_score(self.deck1)
            player2_score = 0
        else:
            player1_score = 0
            player2_score = self.calculate_score(self.deck2)
        
        return winner, player1_score, player2_score
    
    def _recursive_combat_game(self, deck1: List[int], deck2: List[int]) -> Tuple[int, List[int], List[int]]:
        """
        Play a recursive combat game (may be a sub-game).
        
        Args:
            deck1: Player 1's deck for this game
            deck2: Player 2's deck for this game
            
        Returns:
            Tuple of (winner, final_deck1, final_deck2)
        """
        game_states = set()
        
        while len(deck1) > 0 and len(deck2) > 0:
            # Check for repeated game state (infinite game prevention)
            state = (tuple(deck1), tuple(deck2))
            if state in game_states:
                # Player 1 wins if we've seen this state before
                return 1, deck1, deck2
            game_states.add(state)
            
            # Draw cards
            card1 = deck1.pop(0)
            card2 = deck2.pop(0)
            
            # Determine round winner
            if len(deck1) >= card1 and len(deck2) >= card2:
                # Play sub-game
                sub_deck1 = deck1[:card1]
                sub_deck2 = deck2[:card2]
                
                # Optimization: if player 1 has the highest card overall, they win
                max_card1 = max(sub_deck1) if sub_deck1 else 0
                max_card2 = max(sub_deck2) if sub_deck2 else 0
                
                if max_card1 > max_card2:
                    round_winner = 1
                else:
                    round_winner = self._recursive_combat_game(sub_deck1, sub_deck2)[0]
            else:
                # Regular combat rule
                round_winner = 1 if card1 > card2 else 2
            
            # Winner takes both cards
            if round_winner == 1:
                deck1.extend([card1, card2])
            else:
                deck2.extend([card2, card1])
        
        # Determine final winner
        winner = 1 if len(deck1) > 0 else 2
        return winner, deck1, deck2
    
    def get_game_summary(self) -> str:
        """Get a summary of the current game state."""
        summary = []
        summary.append(f"Round: {self.round_number}")
        summary.append(f"Player 1 deck ({len(self.deck1)} cards): {self.deck1}")
        summary.append(f"Player 2 deck ({len(self.deck2)} cards): {self.deck2}")
        
        if len(self.deck1) > 0:
            summary.append(f"Player 1 score: {self.calculate_score(self.deck1)}")
        if len(self.deck2) > 0:
            summary.append(f"Player 2 score: {self.calculate_score(self.deck2)}")
        
        return "\n".join(summary)


class Day22Solution(AdventSolution):
    """Solution for 2020 Day 22: Crab Combat."""

    def __init__(self):
        super().__init__(2020, 22, "Crab Combat")

    def parse_decks(self, input_data: str) -> Tuple[List[int], List[int]]:
        """
        Parse player decks from input data.
        
        Args:
            input_data: Raw input data containing both player decks
            
        Returns:
            Tuple of (player1_deck, player2_deck)
        """
        lines = input_data.strip().split('\n')
        
        player1_deck = []
        player2_deck = []
        current_player = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            elif 'Player 1' in line:
                current_player = 1
            elif 'Player 2' in line:
                current_player = 2
            elif line.isdigit():
                if current_player == 1:
                    player1_deck.append(int(line))
                elif current_player == 2:
                    player2_deck.append(int(line))
        
        return player1_deck, player2_deck

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Play regular Combat and return winning score.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            The winning player's score
        """
        player1_deck, player2_deck = self.parse_decks(input_data)
        game = CrabCombat(player1_deck, player2_deck)
        
        winner, player1_score, player2_score = game.play_regular_combat()
        
        return player1_score if winner == 1 else player2_score

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Play Recursive Combat and return winning score.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            The winning player's score
        """
        player1_deck, player2_deck = self.parse_decks(input_data)
        game = CrabCombat(player1_deck, player2_deck)
        
        winner, player1_score, player2_score = game.play_recursive_combat()
        
        return player1_score if winner == 1 else player2_score

    def analyze_game(self, input_data: str) -> str:
        """
        Analyze both regular and recursive combat games.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis summary as formatted string
        """
        player1_deck, player2_deck = self.parse_decks(input_data)
        
        analysis = []
        analysis.append("=== Crab Combat Analysis ===")
        analysis.append(f"Player 1 starting deck: {player1_deck}")
        analysis.append(f"Player 2 starting deck: {player2_deck}")
        analysis.append(f"Total cards: {len(player1_deck) + len(player2_deck)}")
        
        # Analyze regular combat
        game = CrabCombat(player1_deck, player2_deck)
        winner1, score1_p1, score1_p2 = game.play_regular_combat()
        
        analysis.append(f"\nRegular Combat:")
        analysis.append(f"  Winner: Player {winner1}")
        analysis.append(f"  Rounds played: {game.round_number}")
        analysis.append(f"  Winning score: {score1_p1 if winner1 == 1 else score1_p2}")
        
        # Analyze recursive combat
        game.reset_game()
        winner2, score2_p1, score2_p2 = game.play_recursive_combat()
        
        analysis.append(f"\nRecursive Combat:")
        analysis.append(f"  Winner: Player {winner2}")
        analysis.append(f"  Winning score: {score2_p1 if winner2 == 1 else score2_p2}")
        
        # Compare results
        if winner1 != winner2:
            analysis.append(f"\nDifferent winners! Regular: Player {winner1}, Recursive: Player {winner2}")
        else:
            analysis.append(f"\nSame winner in both games: Player {winner1}")
        
        return "\n".join(analysis)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test with example from problem description
        test_input = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
        
        player1_deck, player2_deck = self.parse_decks(test_input)
        
        # Validate parsing
        if player1_deck != [9, 2, 6, 3, 1]:
            print(f"Player 1 parsing failed: expected [9, 2, 6, 3, 1], got {player1_deck}")
            return False
        
        if player2_deck != [5, 8, 4, 7, 10]:
            print(f"Player 2 parsing failed: expected [5, 8, 4, 7, 10], got {player2_deck}")
            return False
        
        # Test regular combat
        game = CrabCombat(player1_deck, player2_deck)
        winner, p1_score, p2_score = game.play_regular_combat()
        
        if winner != 2:
            print(f"Regular combat winner test failed: expected Player 2, got Player {winner}")
            return False
        
        if p2_score != 306:
            print(f"Regular combat score test failed: expected 306, got {p2_score}")
            return False
        
        # Test recursive combat
        game = CrabCombat(player1_deck, player2_deck)
        winner, p1_score, p2_score = game.play_recursive_combat()
        
        if winner != 2:
            print(f"Recursive combat winner test failed: expected Player 2, got Player {winner}")
            return False
        
        if p2_score != 291:
            print(f"Recursive combat score test failed: expected 291, got {p2_score}")
            return False
        
        print("✅ All Day 22 validation tests passed!")
        return True


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day22Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day22Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main function to run the solution."""
    solution = Day22Solution()
    solution.main()


if __name__ == "__main__":
    main()