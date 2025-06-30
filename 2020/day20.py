#!/usr/bin/env python3
"""
Advent of Code 2020 Day 20: Jurassic Jigsaw
https://adventofcode.com/2020/day/20

Enhanced solution using AdventSolution base class.
Puzzle piece matching with rotation/flipping, graph algorithms, and pattern recognition.
"""

import sys
import re
import math
import copy
import random
from pathlib import Path
from typing import Any, List, Dict, Optional, Tuple

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser

try:
    import networkx as nx
except ImportError:
    print("Warning: networkx not available. Install with: pip install networkx")
    nx = None


class Piece:
    """Represents a puzzle piece with rotation and flipping capabilities."""
    
    def __init__(self):
        self.id = 0
        self.orient = 0
        self.image = []
        self.image2 = []

    def removeBorder(self):
        """Remove border from piece image."""
        temp = []
        for i in self.image[1:-1]:
            temp.append(i[1:-1])
        self.image2 = copy.deepcopy(temp)

    def rotate90(self):
        """Rotate piece 90 degrees clockwise."""
        temp = list(zip(*self.image[::-1]))
        temp2 = []
        for t in temp:
            temp2.append("".join(t))
        self.image = copy.deepcopy(temp2)

    def rotate180(self):
        """Rotate piece 180 degrees."""
        self.rotate90()
        self.rotate90()

    def rotate270(self):
        """Rotate piece 270 degrees clockwise."""
        self.rotate90()
        self.rotate90()
        self.rotate90()

    def flipX(self):
        """Flip piece horizontally."""
        temp = []
        for i in self.image:
            temp.append(i[::-1])
        self.image = copy.deepcopy(temp)

    def flipY(self):
        """Flip piece vertically."""
        temp = []
        for i in self.image[::-1]:
            temp.append(i)
        self.image = copy.deepcopy(temp)    

    def printImage(self):
        """Print the main image."""
        for r in self.image:
            print(r)
        print('\n')

    def printImage2(self):
        """Print the border-removed image."""
        for r in self.image2:
            print(r)
        print('\n')

    def sides(self):
        """Get all four sides of the piece."""
        return [self.sideA(), self.sideB(), self.sideC(), self.sideD()]

    def sideA(self):
        """Get top side."""
        return self.image[0]

    def sideB(self):
        """Get right side."""
        temp = ""
        for x in range(0, len(self.image)):
            temp = temp + self.image[x][len(self.image)-1]
        return temp

    def sideC(self):
        """Get left side."""
        temp = ""
        for x in range(0, len(self.image)):
            temp = temp + self.image[x][0]
        return temp

    def sideD(self):
        """Get bottom side."""
        return self.image[len(self.image)-1]


class Day20Solution(AdventSolution):
    """Solution for 2020 Day 20: Jurassic Jigsaw."""

    def __init__(self):
        super().__init__(2020, 20, "Jurassic Jigsaw")
        self.edges = ['A', 'B', 'C', 'D']

    def parse_input(self, input_data: str) -> Dict[int, Piece]:
        """Parse input into puzzle pieces."""
        lines = input_data.strip().split('\n')
        puzzle = {}
        
        id_num = 0
        tile = []
        
        for line in lines:
            temp = line.strip()
            
            if 'Tile' in temp:
                if id_num not in puzzle and id_num != 0:
                    p = Piece()
                    p.id = id_num
                    p.image = tile.copy()
                    puzzle[id_num] = p
                    tile = []
                
                id_num = int(temp.split(' ')[1][:-1])
                
            elif len(temp) > 1:
                tile.append(temp)
        
        # Add the last tile
        if id_num not in puzzle and id_num != 0:
            p = Piece()
            p.id = id_num
            p.image = tile.copy()
            puzzle[id_num] = p
        
        return puzzle

    def match_edges(self, P1: Piece, P2: Piece) -> str:
        """Check if two pieces have matching edges."""
        side = "none"
        e = self.edges
        
        if P1.sideA() in P2.sides():
            side = "A-" + e[P2.sides().index(P1.sideA())]
        elif P1.sideB() in P2.sides():
            side = "B-" + e[P2.sides().index(P1.sideB())]
        elif P1.sideC() in P2.sides():
            side = "C-" + e[P2.sides().index(P1.sideC())]
        elif P1.sideD() in P2.sides():
            side = "D-" + e[P2.sides().index(P1.sideD())]
        elif P1.sideA()[::-1] in P2.sides():
            side = "Arev-" + e[P2.sides().index(P1.sideA()[::-1])]
        elif P1.sideB()[::-1] in P2.sides():
            side = "Brev-" + e[P2.sides().index(P1.sideB()[::-1])]
        elif P1.sideC()[::-1] in P2.sides():
            side = "Crev-" + e[P2.sides().index(P1.sideC()[::-1])]
        elif P1.sideD()[::-1] in P2.sides():
            side = "Drev-" + e[P2.sides().index(P1.sideD()[::-1])]
        
        return side

    def find_corners(self, puzzle: Dict[int, Piece]) -> List[int]:
        """Find corner pieces by counting edge matches."""
        corners = []
        
        if nx is None:
            # Fallback without networkx
            for k1, v1 in puzzle.items():
                matches = 0
                for k2, v2 in puzzle.items():
                    if k1 != k2:
                        # Check all edge combinations
                        for side in v1.sides() + [s[::-1] for s in v1.sides()]:
                            if side in v2.sides():
                                matches += 1
                                break
                if matches == 2:  # Corner pieces have exactly 2 matching neighbors
                    corners.append(k1)
            return corners
        
        # Use networkx for graph-based approach
        G = nx.Graph()
        
        for k1, v1 in puzzle.items():
            matches = 0
            for k2, v2 in puzzle.items():
                if k1 != k2:
                    # Check all possible edge matches
                    edge_found = False
                    for side in v1.sides():
                        if side in v2.sides() or side[::-1] in v2.sides():
                            if not edge_found:
                                G.add_edge(str(k1), str(k2))
                                matches += 1
                                edge_found = True
            
            if matches == 2:
                corners.append(k1)
        
        return corners

    def assemble_image(self, puzzle: Dict[int, Piece]) -> List[str]:
        """
        Assemble the complete image from puzzle pieces using backtracking.
        
        Args:
            puzzle: Dictionary of puzzle pieces
            
        Returns:
            List of strings representing the assembled image (borders removed)
        """
        grid_size = int(math.sqrt(len(puzzle)))
        grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        
        def get_all_orientations(piece):
            """Get all 8 possible orientations of a piece."""
            orientations = []
            current = copy.deepcopy(piece)
            
            # 4 rotations
            for _ in range(4):
                orientations.append(copy.deepcopy(current))
                current.rotate90()
            
            # Flip and 4 more rotations
            current.flipX()
            for _ in range(4):
                orientations.append(copy.deepcopy(current))
                current.rotate90()
            
            return orientations
        
        def fits(piece, row, col):
            """Check if a piece fits at the given position."""
            # Check top neighbor
            if row > 0:
                top_neighbor = grid[row-1][col]
                if top_neighbor and piece.sideA() != top_neighbor.sideD():
                    return False
            
            # Check left neighbor  
            if col > 0:
                left_neighbor = grid[row][col-1]
                if left_neighbor and piece.sideC() != left_neighbor.sideB():
                    return False
            
            # Check right neighbor
            if col < grid_size - 1:
                right_neighbor = grid[row][col+1]
                if right_neighbor and piece.sideB() != right_neighbor.sideC():
                    return False
            
            # Check bottom neighbor
            if row < grid_size - 1:
                bottom_neighbor = grid[row+1][col]
                if bottom_neighbor and piece.sideD() != bottom_neighbor.sideA():
                    return False
            
            return True
        
        def solve(used_pieces):
            """Backtracking solver."""
            # Find next empty position
            for row in range(grid_size):
                for col in range(grid_size):
                    if grid[row][col] is None:
                        # Try each unused piece
                        for piece_id, piece in puzzle.items():
                            if piece_id in used_pieces:
                                continue
                            
                            # Try all orientations
                            for oriented_piece in get_all_orientations(piece):
                                if fits(oriented_piece, row, col):
                                    grid[row][col] = oriented_piece
                                    used_pieces.add(piece_id)
                                    
                                    if solve(used_pieces):
                                        return True
                                    
                                    # Backtrack
                                    grid[row][col] = None
                                    used_pieces.remove(piece_id)
                        
                        return False  # No piece fits here
            
            return True  # All positions filled
        
        # Start solving
        if not solve(set()):
            return []  # Failed to solve
        
        # Remove borders and combine into final image
        for row in range(grid_size):
            for col in range(grid_size):
                if grid[row][col]:
                    grid[row][col].removeBorder()
        
        # Combine pieces into final image
        piece_height = 8  # 10 - 2 (border removal)
        final_image = []
        
        for row in range(grid_size):
            for line_idx in range(piece_height):
                line = ""
                for col in range(grid_size):
                    if grid[row][col] and line_idx < len(grid[row][col].image2):
                        line += grid[row][col].image2[line_idx]
                final_image.append(line)
        
        return final_image

    def look_for_monsters(self, p: Piece) -> int:
        """Look for sea monsters in the assembled image."""
        # Sea monster pattern:
        #                   # 
        # #    ##    ##    ###
        #  #  #  #  #  #  #   
        
        monster_pattern = [
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   "
        ]
        
        monsters = 0
        image = p.image
        
        # Check each possible position for a sea monster
        for row in range(len(image) - len(monster_pattern) + 1):
            for col in range(len(image[0]) - len(monster_pattern[0]) + 1):
                # Check if monster pattern matches at this position
                is_monster = True
                for pattern_row in range(len(monster_pattern)):
                    for pattern_col in range(len(monster_pattern[pattern_row])):
                        if monster_pattern[pattern_row][pattern_col] == '#':
                            if (row + pattern_row >= len(image) or 
                                col + pattern_col >= len(image[row + pattern_row]) or
                                image[row + pattern_row][col + pattern_col] != '#'):
                                is_monster = False
                                break
                    if not is_monster:
                        break
                
                if is_monster:
                    monsters += 1
        
        return monsters

    def part1(self, input_data: str) -> Any:
        """
        Find the four corner pieces and multiply their IDs.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Product of corner piece IDs
        """
        puzzle = self.parse_input(input_data)
        corners = self.find_corners(puzzle)
        
        result = 1
        for corner_id in corners:
            result *= corner_id
        
        return result

    def part2(self, input_data: str) -> Any:
        """
        Assemble the image and count water roughness (# not part of sea monsters).
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Water roughness count
        """
        puzzle = self.parse_input(input_data)
        
        # Assemble the full image
        assembled_image = self.assemble_image(puzzle)
        if not assembled_image:
            return "Failed to assemble image"
        
        # Create a piece to search for monsters
        search_piece = Piece()
        search_piece.image = assembled_image
        
        # Try different orientations to find monsters
        max_monsters = 0
        best_config = None
        
        for rotation in [0, 90, 180, 270]:
            for flip in ['none', 'x', 'y', 'xy']:
                test_piece = copy.deepcopy(search_piece)
                
                # Apply transformations
                if rotation == 90:
                    test_piece.rotate90()
                elif rotation == 180:
                    test_piece.rotate180()
                elif rotation == 270:
                    test_piece.rotate270()
                
                if 'x' in flip:
                    test_piece.flipX()
                if 'y' in flip:
                    test_piece.flipY()
                
                monsters = self.look_for_monsters(test_piece)
                if monsters > max_monsters:
                    max_monsters = monsters
                    best_config = (rotation, flip)
        
        # Count total # symbols in the correctly oriented image
        if best_config:
            final_piece = copy.deepcopy(search_piece)
            rotation, flip = best_config
            
            if rotation == 90:
                final_piece.rotate90()
            elif rotation == 180:
                final_piece.rotate180()
            elif rotation == 270:
                final_piece.rotate270()
            
            if 'x' in flip:
                final_piece.flipX()
            if 'y' in flip:
                final_piece.flipY()
            
            total_pounds = sum(line.count('#') for line in final_piece.image)
        else:
            total_pounds = sum(line.count('#') for line in assembled_image)
        
        # Each monster has 15 # symbols
        return total_pounds - (max_monsters * 15)


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day20Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day20Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main execution function."""
    solution = Day20Solution()
    solution.main()


if __name__ == "__main__":
    main()