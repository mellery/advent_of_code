#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 13: Transparent Origami

Folding transparent paper with dots on it.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from utils.ascii_art_parser import parse_ascii_letters
from typing import Any, Dict, Tuple, List, Set


def parse_input_from_data(input_data: str) -> Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]:
    """Parse the input data to get dots and fold instructions."""
    lines = input_data.strip().split('\n')
    dots = set()
    folds = []
    
    # Parse dots
    i = 0
    while i < len(lines) and lines[i].strip():
        x, y = map(int, lines[i].strip().split(','))
        dots.add((x, y))
        i += 1
    
    # Skip empty line
    i += 1
    
    # Parse fold instructions
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('fold along '):
            fold_instruction = line.replace('fold along ', '')
            direction, value = fold_instruction.split('=')
            folds.append((direction, int(value)))
        i += 1
    
    return dots, folds


def fold_paper(dots: Set[Tuple[int, int]], direction: str, fold_line: int) -> Set[Tuple[int, int]]:
    """Fold the paper along the specified line."""
    new_dots = set()
    
    for x, y in dots:
        if direction == 'y':
            if y < fold_line:
                new_dots.add((x, y))
            elif y > fold_line:
                # Reflect across the fold line
                new_y = fold_line - (y - fold_line)
                new_dots.add((x, new_y))
            # Points on the fold line disappear
        else:  # direction == 'x'
            if x < fold_line:
                new_dots.add((x, y))
            elif x > fold_line:
                # Reflect across the fold line
                new_x = fold_line - (x - fold_line)
                new_dots.add((new_x, y))
            # Points on the fold line disappear
    
    return new_dots


def visualize_dots(dots: Set[Tuple[int, int]]) -> str:
    """Create a visual representation of the dots."""
    if not dots:
        return ""
    
    max_x = max(x for x, y in dots)
    max_y = max(y for x, y in dots)
    
    lines = []
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            if (x, y) in dots:
                line += "#"
            else:
                line += "."
        lines.append(line)
    
    return "\n".join(lines)


class Day13Solution(AdventSolution):
    """Day 13: Transparent Origami"""
    
    def __init__(self):
        super().__init__(2021, 13, "Transparent Origami")
    
    def part1(self, input_data: str) -> Any:
        """
        Count visible dots after the first fold.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Number of visible dots after first fold
        """
        dots, folds = parse_input_from_data(input_data)
        
        if folds:
            direction, fold_line = folds[0]
            dots = fold_paper(dots, direction, fold_line)
        
        return len(dots)
    
    def part2(self, input_data: str) -> Any:
        """
        Apply all folds and return the resulting pattern.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            The letters formed by the dots
        """
        dots, folds = parse_input_from_data(input_data)
        
        for direction, fold_line in folds:
            dots = fold_paper(dots, direction, fold_line)
        
        # Generate the visual pattern
        pattern = visualize_dots(dots)
        
        # Use ASCII art parser with day13 font style
        letters = parse_ascii_letters(pattern, 'day13')
        
        # If that fails, try other font styles
        if not letters or '?' in letters:
            letters = parse_ascii_letters(pattern, 'thick')
        
        if not letters or '?' in letters:
            letters = parse_ascii_letters(pattern, 'thin')
        
        return letters


def main():
    """Main execution function."""
    solution = Day13Solution()
    solution.main()


if __name__ == "__main__":
    main()