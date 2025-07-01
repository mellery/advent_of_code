#!/usr/bin/env python3
"""
Advent of Code 2021 Day 15: Chiton
https://adventofcode.com/2021/day/15

Enhanced solution using AdventSolution base class.
Migrated from legacy implementation.
"""

import sys
from pathlib import Path
from typing import Any, List, Dict, Optional, Tuple
import heapq

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser

# Try to import NetworkX, but provide fallback
try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False


class Day15Solution(AdventSolution):
    """Solution for 2021 Day 15: Chiton."""

    def __init__(self):
        super().__init__(2021, 15, "Chiton")

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Find lowest risk path through cave.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Lowest total risk from top-left to bottom-right
        """
        parser = InputParser(input_data)
        lines = parser.as_lines()
        
        # Build risk grid
        grid = {}
        rows = len(lines)
        cols = len(lines[0]) if lines else 0
        
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                grid[(r, c)] = int(char)
        
        if HAS_NETWORKX:
            return self._solve_with_networkx(grid, rows, cols)
        else:
            return self._solve_with_dijkstra(grid, rows, cols)

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Find path through expanded cave.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Lowest total risk in 5x expanded cave
        """
        parser = InputParser(input_data)
        lines = parser.as_lines()
        
        # Build expanded grid (5x5 tiling)
        original_rows = len(lines)
        original_cols = len(lines[0]) if lines else 0
        expanded_grid = {}
        
        for tile_r in range(5):
            for tile_c in range(5):
                for r, line in enumerate(lines):
                    for c, char in enumerate(line):
                        original_risk = int(char)
                        new_risk = original_risk + tile_r + tile_c
                        # Risk wraps from 9 back to 1
                        while new_risk > 9:
                            new_risk -= 9
                        
                        new_r = tile_r * original_rows + r
                        new_c = tile_c * original_cols + c
                        expanded_grid[(new_r, new_c)] = new_risk
        
        expanded_rows = original_rows * 5
        expanded_cols = original_cols * 5
        
        if HAS_NETWORKX:
            return self._solve_with_networkx(expanded_grid, expanded_rows, expanded_cols)
        else:
            return self._solve_with_dijkstra(expanded_grid, expanded_rows, expanded_cols)
    
    def _solve_with_networkx(self, grid: Dict[Tuple[int, int], int], rows: int, cols: int) -> int:
        """Solve using NetworkX Dijkstra implementation."""
        G = nx.DiGraph()
        
        # Add nodes and edges
        for r in range(rows):
            for c in range(cols):
                # Add edges to adjacent cells
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Edge weight is the risk of entering the target cell
                        G.add_edge((r, c), (nr, nc), weight=grid[(nr, nc)])
        
        # Find shortest path
        path = nx.dijkstra_path(G, (0, 0), (rows-1, cols-1), weight='weight')
        
        # Calculate total risk (excluding starting position)
        total_risk = sum(grid[pos] for pos in path[1:])
        return total_risk
    
    def _solve_with_dijkstra(self, grid: Dict[Tuple[int, int], int], rows: int, cols: int) -> int:
        """Solve using custom Dijkstra implementation."""
        start = (0, 0)
        end = (rows-1, cols-1)
        
        # Dijkstra's algorithm
        distances = {start: 0}
        heap = [(0, start)]
        visited = set()
        
        while heap:
            current_dist, current = heapq.heappop(heap)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == end:
                return current_dist
            
            r, c = current
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                neighbor = (nr, nc)
                
                if (0 <= nr < rows and 0 <= nc < cols and 
                    neighbor not in visited):
                    
                    new_dist = current_dist + grid[neighbor]
                    
                    if neighbor not in distances or new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        heapq.heappush(heap, (new_dist, neighbor))
        
        return -1  # No path found

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        test_input = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
        
        if expected_part1 is None:
            expected_part1 = 40  # Known result for test input
        
        if expected_part2 is None:
            expected_part2 = 315  # Known result for expanded test input
        
        test_result1 = self.part1(test_input)
        if test_result1 != expected_part1:
            print(f"Part 1 test failed: expected {expected_part1}, got {test_result1}")
            return False
        
        test_result2 = self.part2(test_input)
        if test_result2 != expected_part2:
            print(f"Part 2 test failed: expected {expected_part2}, got {test_result2}")
            return False
        
        print("✅ All Day 15 validation tests passed!")
        if not HAS_NETWORKX:
            print("ℹ️  Using fallback Dijkstra implementation (NetworkX not available)")
        return True




def main():
    """Main execution function."""
    solution = Day15Solution()
    solution.main()


if __name__ == "__main__":
    main()