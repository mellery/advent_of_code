#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 4: Bingo

"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Any


class Day4Solution(AdventSolution):
    """Solution for Advent of Code 2021 Day 4."""
    
    def __init__(self):
        super().__init__(2021, 4, "Bingo")
    
    def part1(self, input_data: str) -> int:
        balls, *boards = input_data.strip().split('\n\n')
        balls = list(map(int, balls.split(',')))
        # Parse boards as 5x5 grids
        boards = [
            [list(map(int, row.split())) for row in board.strip().split('\n')]
            for board in boards
        ]
        marks = [
            [[False]*5 for _ in range(5)]
            for _ in boards
        ]

        for ball in balls:
            for b, board in enumerate(boards):
                for i in range(5):
                    for j in range(5):
                        if board[i][j] == ball:
                            marks[b][i][j] = True
                # Check rows and columns
                for i in range(5):
                    if all(marks[b][i][j] for j in range(5)) or all(marks[b][j][i] for j in range(5)):
                        # Calculate score
                        unmarked_sum = sum(
                            board[x][y]
                            for x in range(5)
                            for y in range(5)
                            if not marks[b][x][y]
                        )
                        return unmarked_sum * ball
        print("No winning board found.")
        return None

    def part2(self, input_data: str) -> int:
        balls, *boards = input_data.strip().split('\n\n')
        balls = list(map(int, balls.split(',')))
        # Parse boards as 5x5 grids
        boards = [
            [list(map(int, row.split())) for row in board.strip().split('\n')]
            for board in boards
        ]
        marks = [
            [[False]*5 for _ in range(5)]
            for _ in boards
        ]

        for ball in balls:
            # Mark numbers on all boards
            for b, board in enumerate(boards):
                for i in range(5):
                    for j in range(5):
                        if board[i][j] == ball:
                            marks[b][i][j] = True
            
            # Check for winning boards and remove them
            boards_to_remove = []
            for b, board in enumerate(boards):
                # Check rows and columns
                for i in range(5):
                    if all(marks[b][i][j] for j in range(5)) or all(marks[b][j][i] for j in range(5)):
                        if len(boards) == 1:
                            # Last board wins - calculate score
                            unmarked_sum = sum(
                                board[x][y]
                                for x in range(5)
                                for y in range(5)
                                if not marks[b][x][y]
                            )
                            return unmarked_sum * ball
                        boards_to_remove.append(b)
                        break
            
            # Remove winning boards (in reverse order to maintain indices)
            for b in reversed(boards_to_remove):
                boards.pop(b)
                marks.pop(b)

        print("No winning board found.")
        return None

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
        expected_part1 = 4512
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        expected_part2 = 1924

        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False
        
        print("✅ All Day 4 validation tests passed!")
        return True


def main():
    """Main execution function."""
    solution = Day4Solution()
    solution.main()


if __name__ == "__main__":
    main()
