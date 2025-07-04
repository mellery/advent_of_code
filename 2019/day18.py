#!/usr/bin/env python3
"""
Advent of Code 2019 Day 18: Many-Worlds Interpretation (OPTIMIZED)

High-performance key collection maze with major optimizations:
- Optimized data structures (tuples instead of objects)
- Improved graph construction (single BFS per node)
- Better state representation (bitmasking for keys)
- Enhanced heuristics for A* search
- Memory-efficient pathfinding

Performance target: <5 seconds total execution time
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from collections import deque
from typing import Dict, Set, Tuple, List, Any, Optional
import heapq

# Direction vectors for neighbors
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right


class OptimizedKeyMaze:
    """
    High-performance key collection maze with optimized algorithms.
    
    Key optimizations:
    - Tuple-based positions (no object overhead)
    - Bitmasking for key sets (faster operations)
    - Single BFS for graph construction
    - Improved A* heuristics
    """
    
    def __init__(self, maze_data: str):
        """Initialize with performance-optimized parsing."""
        lines = [line.strip() for line in maze_data.strip().split('\n') if line.strip()]
        self.grid = [list(line) for line in lines]
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0
        
        # Extract positions efficiently
        self.start_positions: List[Tuple[int, int]] = []
        self.keys: Dict[str, Tuple[int, int]] = {}
        self.doors: Dict[str, Tuple[int, int]] = {}
        self.key_to_bit: Dict[str, int] = {}
        
        self._extract_positions()
        
        # Build optimized graph
        self.graph: Dict[str, Dict[str, Tuple[int, int]]] = {}  # name -> {other_name: (distance, required_keys_bitmask)}
        self._build_optimized_graph()
        
        self.total_keys = len(self.keys)
        self.all_keys_mask = (1 << self.total_keys) - 1  # Bitmask with all keys set
    
    def _extract_positions(self):
        """Extract important positions with key bit mapping."""
        key_idx = 0
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                
                if cell == '@':
                    self.start_positions.append((x, y))
                elif cell.islower():  # Key
                    self.keys[cell] = (x, y)
                    self.key_to_bit[cell] = key_idx
                    key_idx += 1
                elif cell.isupper():  # Door
                    self.doors[cell] = (x, y)
    
    def _build_optimized_graph(self):
        """Build graph with single BFS per node and bitmask optimization."""
        # All important positions
        important_nodes = {}
        
        # Add start positions
        for i, pos in enumerate(self.start_positions):
            important_nodes[f'@{i}'] = pos
        
        # Add key positions
        important_nodes.update(self.keys)
        
        # Build graph with optimized BFS
        for name, pos in important_nodes.items():
            self.graph[name] = {}
            paths = self._bfs_all_paths(pos)
            
            for other_name, other_pos in important_nodes.items():
                if other_name != name and other_pos in paths:
                    distance, required_keys_mask = paths[other_pos]
                    self.graph[name][other_name] = (distance, required_keys_mask)
    
    def _bfs_all_paths(self, start: Tuple[int, int]) -> Dict[Tuple[int, int], Tuple[int, int]]:
        """
        Single BFS to find distances and required keys to all reachable positions.
        
        Returns:
            Dict mapping position to (distance, required_keys_bitmask)
        """
        paths = {}
        queue = deque([(start, 0, 0)])  # (position, distance, required_keys_mask)
        visited = {start: 0}  # position -> best_required_keys_mask
        
        while queue:
            (x, y), dist, keys_mask = queue.popleft()
            
            # Store result
            if (x, y) not in paths or paths[(x, y)][1] > keys_mask:
                paths[(x, y)] = (dist, keys_mask)
            
            # Explore neighbors
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                
                if (0 <= ny < self.height and 0 <= nx < self.width and 
                    self.grid[ny][nx] != '#'):
                    
                    new_keys_mask = keys_mask
                    cell = self.grid[ny][nx]
                    
                    # Check if this is a door
                    if cell.isupper():
                        key_needed = cell.lower()
                        if key_needed in self.key_to_bit:
                            new_keys_mask |= (1 << self.key_to_bit[key_needed])
                    
                    neighbor = (nx, ny)
                    
                    # Only continue if we found a better path (fewer required keys)
                    if (neighbor not in visited or visited[neighbor] > new_keys_mask):
                        visited[neighbor] = new_keys_mask
                        queue.append((neighbor, dist + 1, new_keys_mask))
        
        return paths
    
    def solve_single_robot(self) -> int:
        """Optimized A* search for single robot."""
        start_pos = '@0'
        
        # Priority queue: (f_score, g_score, position, keys_bitmask)
        heap = [(0, 0, start_pos, 0)]
        best_distance = {}  # (position, keys_mask) -> distance
        
        while heap:
            f_score, g_score, pos, keys_mask = heapq.heappop(heap)
            
            state = (pos, keys_mask)
            if state in best_distance and best_distance[state] <= g_score:
                continue
            best_distance[state] = g_score
            
            # Check if we collected all keys
            if keys_mask == self.all_keys_mask:
                return g_score
            
            # Try to collect each uncollected key
            for key, key_pos in self.keys.items():
                key_bit = 1 << self.key_to_bit[key]
                
                # Skip if already collected
                if keys_mask & key_bit:
                    continue
                
                if key in self.graph[pos]:
                    distance, required_keys_mask = self.graph[pos][key]
                    
                    # Check if we have all required keys
                    if (keys_mask & required_keys_mask) == required_keys_mask:
                        new_g = g_score + distance
                        new_keys = keys_mask | key_bit
                        new_state = (key, new_keys)
                        
                        if new_state not in best_distance or best_distance[new_state] > new_g:
                            # Improved heuristic: estimate remaining distance
                            h_score = self._estimate_remaining_distance(key, new_keys)
                            f_score = new_g + h_score
                            heapq.heappush(heap, (f_score, new_g, key, new_keys))
        
        return -1  # No solution found
    
    def solve_multiple_robots(self) -> int:
        """Optimized A* search for multiple robots."""
        start_positions = tuple(f'@{i}' for i in range(len(self.start_positions)))
        
        # Priority queue: (f_score, g_score, positions_tuple, keys_bitmask)
        heap = [(0, 0, start_positions, 0)]
        best_distance = {}
        
        while heap:
            f_score, g_score, positions, keys_mask = heapq.heappop(heap)
            
            state = (positions, keys_mask)
            if state in best_distance and best_distance[state] <= g_score:
                continue
            best_distance[state] = g_score
            
            # Check if we collected all keys
            if keys_mask == self.all_keys_mask:
                return g_score
            
            # Try moving each robot to collect each uncollected key
            for key, key_pos in self.keys.items():
                key_bit = 1 << self.key_to_bit[key]
                
                # Skip if already collected
                if keys_mask & key_bit:
                    continue
                
                for i, pos in enumerate(positions):
                    if key in self.graph[pos]:
                        distance, required_keys_mask = self.graph[pos][key]
                        
                        # Check if we have all required keys
                        if (keys_mask & required_keys_mask) == required_keys_mask:
                            new_g = g_score + distance
                            new_positions = tuple(
                                key if j == i else positions[j] 
                                for j in range(len(positions))
                            )
                            new_keys = keys_mask | key_bit
                            new_state = (new_positions, new_keys)
                            
                            if new_state not in best_distance or best_distance[new_state] > new_g:
                                # Improved heuristic for multiple robots
                                h_score = self._estimate_remaining_distance_multi(new_positions, new_keys)
                                f_score = new_g + h_score
                                heapq.heappush(heap, (f_score, new_g, new_positions, new_keys))
        
        return -1  # No solution found
    
    def _estimate_remaining_distance(self, current_pos: str, keys_mask: int) -> int:
        """
        Improved heuristic: estimate minimum distance to collect remaining keys.
        
        This is still admissible but more informed than just counting keys.
        """
        if keys_mask == self.all_keys_mask:
            return 0
        
        # Find closest uncollected key
        min_distance = float('inf')
        for key, key_pos in self.keys.items():
            key_bit = 1 << self.key_to_bit[key]
            
            if not (keys_mask & key_bit):  # Key not collected
                if key in self.graph[current_pos]:
                    distance, required_keys_mask = self.graph[current_pos][key]
                    
                    # Check if we can reach this key
                    if (keys_mask & required_keys_mask) == required_keys_mask:
                        min_distance = min(min_distance, distance)
        
        return min_distance if min_distance != float('inf') else 0
    
    def _estimate_remaining_distance_multi(self, positions: Tuple[str, ...], keys_mask: int) -> int:
        """Heuristic for multiple robots: closest key from any robot."""
        if keys_mask == self.all_keys_mask:
            return 0
        
        min_distance = float('inf')
        for key, key_pos in self.keys.items():
            key_bit = 1 << self.key_to_bit[key]
            
            if not (keys_mask & key_bit):  # Key not collected
                for pos in positions:
                    if key in self.graph[pos]:
                        distance, required_keys_mask = self.graph[pos][key]
                        
                        if (keys_mask & required_keys_mask) == required_keys_mask:
                            min_distance = min(min_distance, distance)
        
        return min_distance if min_distance != float('inf') else 0


class Day18OptimizedSolution(AdventSolution):
    """Optimized solution for Advent of Code 2019 Day 18."""
    
    def __init__(self):
        super().__init__(year=2019, day=18, title="Many-Worlds Interpretation (Optimized)")
        
    def part1(self, input_data: str) -> Any:
        """Part 1: Single robot key collection."""
        maze = OptimizedKeyMaze(input_data)
        return maze.solve_single_robot()
    
    def part2(self, input_data: str) -> Any:
        """Part 2: Multiple robot key collection."""
        # Transform the maze for part 2 (split start into 4 robots)
        lines = input_data.strip().split('\n')
        modified_lines = []
        
        # Find the starting position
        start_row, start_col = None, None
        for i, line in enumerate(lines):
            if '@' in line:
                start_row, start_col = i, line.index('@')
                break
        
        if start_row is not None:
            # Replace the 3x3 area around @ with the 4-robot pattern
            for i, line in enumerate(lines):
                if i == start_row - 1:
                    modified_line = line[:start_col-1] + '@#@' + line[start_col+2:]
                elif i == start_row:
                    modified_line = line[:start_col-1] + '###' + line[start_col+2:]
                elif i == start_row + 1:
                    modified_line = line[:start_col-1] + '@#@' + line[start_col+2:]
                else:
                    modified_line = line
                modified_lines.append(modified_line)
        else:
            modified_lines = lines
        
        modified_input = '\n'.join(modified_lines)
        maze = OptimizedKeyMaze(modified_input)
        return maze.solve_multiple_robots()

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""
        expected_part1 = 81
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        example_input = """#######
#a.#Cd#
##...##
#..@..#
##...##
#cB#Ab#
#######"""
        expected_part2 = 8
        
        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False
        
        print("✅ All Day 18 validation tests passed!")
        return True
    
def main():
    """Main execution function."""
    solution = Day18OptimizedSolution()
    solution.main()


if __name__ == "__main__":
    main()