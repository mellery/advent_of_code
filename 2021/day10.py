#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 10: Syntax Scoring

Finding syntax errors and completing incomplete bracket sequences.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Optional, Any


class Day10Solution(AdventSolution):
    """Solution for Advent of Code 2021 Day 10."""
    
    def __init__(self):
        super().__init__(2021, 10, "Syntax Scoring")
    
    def _get_lines(self, input_data: str) -> List[str]:
        """Parse input data into list of lines."""
        return [line.strip() for line in input_data.strip().split('\n') if line.strip()]
    
    def _remove_pairs(self, line: str) -> str:
        """Remove complete bracket pairs iteratively until no more can be removed."""
        pairs = ['()', '[]', '{}', '<>']
        prev_length = len(line)
        
        while True:
            for pair in pairs:
                line = line.replace(pair, '')
            
            # If no pairs were removed in this iteration, we're done
            if len(line) == prev_length:
                break
            prev_length = len(line)
        
        return line
    
    def _find_first_illegal_char(self, line: str) -> Optional[str]:
        """Find the first illegal closing character in a corrupted line."""
        closing_chars = {')', ']', '}', '>'}
        for char in line:
            if char in closing_chars:
                return char
        return None
    
    def part1(self, input_data: str) -> int:
        """Find syntax errors (corrupted lines) and calculate error score."""
        lines = self._get_lines(input_data)
        error_score = 0
        points = {')': 3, ']': 57, '}': 1197, '>': 25137}
        
        for line in lines:
            # Remove all complete pairs
            reduced = self._remove_pairs(line)
            
            # If there are closing characters left, the line is corrupted
            illegal_char = self._find_first_illegal_char(reduced)
            if illegal_char:
                error_score += points[illegal_char]
        
        return error_score
    
    def part2(self, input_data: str) -> int:
        """Find incomplete lines and calculate completion scores."""
        lines = self._get_lines(input_data)
        scores = []
        points = {')': 1, ']': 2, '}': 3, '>': 4}
        close_map = {'(': ')', '[': ']', '{': '}', '<': '>'}
        
        for line in lines:
            # Remove all complete pairs
            reduced = self._remove_pairs(line)
            
            # If there are no closing characters, the line is incomplete
            if not any(char in reduced for char in ')]}>'):
                # The remaining characters are unmatched opening brackets
                # We need to close them in reverse order
                completion = ''
                for char in reversed(reduced):
                    if char in close_map:
                        completion += close_map[char]
                
                # Calculate score for this completion
                score = 0
                for char in completion:
                    score = score * 5 + points[char]
                
                scores.append(score)
        
        # Return the middle score
        scores.sort()
        return scores[len(scores) // 2]







def main():
    """Main execution function."""
    solution = Day10Solution()
    solution.main()

if __name__ == "__main__":
    main()