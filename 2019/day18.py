#!/usr/bin/env python3
"""
Advent of Code 2019 Day 18: Many-Worlds Interpretation

Enhanced solution using the AdventSolution base class for key collection
in maze with graph algorithms, pathfinding, and state space optimization.
"""

import sys
from pathlib import Path
from collections import deque
from typing import Dict, Set, Tuple, List, Optional, Any, FrozenSet
from dataclasses import dataclass
from functools import lru_cache
import heapq
import time

# Add utils to path for enhanced base class
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution

@dataclass(frozen=True)
class Position:
    """Represents a 2D position in the maze."""
    x: int
    y: int
    
    def get_neighbors(self) -> List['Position']:
        """Get all neighboring positions (up, down, left, right)."""
        return [
            Position(self.x, self.y - 1),  # Up
            Position(self.x, self.y + 1),  # Down
            Position(self.x - 1, self.y),  # Left
            Position(self.x + 1, self.y)   # Right
        ]

@dataclass(frozen=True)
class PathInfo:
    """Information about a path between two positions."""
    distance: int
    required_keys: FrozenSet[str]

@dataclass(frozen=True)
class State:
    """State in the search space for multi-robot scenarios."""
    positions: Tuple[str, ...]  # Current positions of robots
    keys: FrozenSet[str]        # Keys collected so far

class KeyMaze:
    """
    Domain class for key collection maze navigation.
    Handles maze parsing, graph construction, and pathfinding with constraints.
    """
    
    def __init__(self, maze_data: str):
        self.grid = self._parse_maze(maze_data)
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0
        
        # Extract important positions
        self.start_positions: List[Position] = []
        self.keys: Dict[str, Position] = {}
        self.doors: Dict[str, Position] = {}
        
        self._extract_positions()
        
        # Build graph of distances between important positions
        self.graph: Dict[str, Dict[str, PathInfo]] = {}
        self._build_graph()
    
    def _parse_maze(self, maze_data: str) -> List[List[str]]:
        """Parse maze data into a 2D grid."""
        lines = [line.strip() for line in maze_data.strip().split('\n') if line.strip()]
        return [list(line) for line in lines]
    
    def _extract_positions(self):
        """Extract start positions, keys, and doors from the maze."""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                pos = Position(x, y)
                
                if cell == '@':
                    self.start_positions.append(pos)
                elif cell.islower():  # Key
                    self.keys[cell] = pos
                elif cell.isupper():  # Door
                    self.doors[cell] = pos
    
    def _build_graph(self):
        """Build a graph of distances between important positions."""
        # All important positions (starts + keys)
        important_positions = {}
        
        # Add start positions
        for i, pos in enumerate(self.start_positions):
            important_positions[f'@{i}'] = pos
        
        # Add key positions
        important_positions.update(self.keys)
        
        # Build graph
        for name, pos in important_positions.items():
            self.graph[name] = {}
            distances = self._bfs_distances(pos)
            
            for other_name, other_pos in important_positions.items():
                if other_name != name and other_pos in distances:
                    # Find required keys for this path
                    required_keys = self._find_required_keys(pos, other_pos)
                    self.graph[name][other_name] = PathInfo(
                        distance=distances[other_pos],
                        required_keys=required_keys
                    )
    
    def _bfs_distances(self, start: Position) -> Dict[Position, int]:
        """BFS to find distances from start to all reachable positions."""
        distances = {}
        queue = deque([(start, 0)])
        visited = {start}
        
        while queue:
            pos, dist = queue.popleft()
            distances[pos] = dist
            
            for neighbor in pos.get_neighbors():
                if (0 <= neighbor.y < self.height and 
                    0 <= neighbor.x < self.width and
                    neighbor not in visited and 
                    self.grid[neighbor.y][neighbor.x] != '#'):
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return distances
    
    def _find_required_keys(self, start: Position, end: Position) -> FrozenSet[str]:
        """Find required keys to travel from start to end."""
        # BFS to find path and collect doors along the way
        queue = deque([start])
        visited = {start}
        parent = {start: None}
        
        # Find path to target
        while queue:
            pos = queue.popleft()
            if pos == end:
                break
            
            for neighbor in pos.get_neighbors():
                if (0 <= neighbor.y < self.height and 
                    0 <= neighbor.x < self.width and
                    neighbor not in visited and 
                    self.grid[neighbor.y][neighbor.x] != '#'):
                    visited.add(neighbor)
                    parent[neighbor] = pos
                    queue.append(neighbor)
        
        # Reconstruct path and find doors
        required_keys = set()
        current = end
        while current is not None:
            cell = self.grid[current.y][current.x]
            if cell.isupper():  # Door
                required_keys.add(cell.lower())
            current = parent.get(current)
        
        return frozenset(required_keys)
    
    def solve_single_robot(self) -> int:
        """Solve for a single robot starting at position @0."""
        all_keys = frozenset(self.keys.keys())
        start_pos = '@0'
        
        # A* search with heuristic
        heap = [(0, 0, start_pos, frozenset())]  # (f_score, g_score, position, keys)
        best_distance = {}
        
        while heap:
            f_score, g_score, pos, collected_keys = heapq.heappop(heap)
            
            state = (pos, collected_keys)
            if state in best_distance and best_distance[state] <= g_score:
                continue
            best_distance[state] = g_score
            
            if collected_keys == all_keys:
                return g_score
            
            # Try to collect each uncollected key
            for key in all_keys - collected_keys:
                if key in self.graph[pos]:
                    path_info = self.graph[pos][key]
                    
                    # Check if we have all required keys
                    if path_info.required_keys.issubset(collected_keys):
                        new_g = g_score + path_info.distance
                        new_keys = collected_keys | {key}
                        new_state = (key, new_keys)
                        
                        if new_state not in best_distance or best_distance[new_state] > new_g:
                            # Simple heuristic: remaining keys count
                            h_score = len(all_keys - new_keys)
                            f_score = new_g + h_score
                            heapq.heappush(heap, (f_score, new_g, key, new_keys))
        
        return -1  # No solution found
    
    def solve_multiple_robots(self) -> int:
        """Solve for multiple robots."""
        all_keys = frozenset(self.keys.keys())
        start_positions = tuple(f'@{i}' for i in range(len(self.start_positions)))
        
        # A* search with state space
        heap = [(0, 0, start_positions, frozenset())]
        best_distance = {}
        
        while heap:
            f_score, g_score, positions, collected_keys = heapq.heappop(heap)
            
            state = (positions, collected_keys)
            if state in best_distance and best_distance[state] <= g_score:
                continue
            best_distance[state] = g_score
            
            if collected_keys == all_keys:
                return g_score
            
            # Try moving each robot to collect each uncollected key
            for key in all_keys - collected_keys:
                for i, pos in enumerate(positions):
                    if key in self.graph[pos]:
                        path_info = self.graph[pos][key]
                        
                        # Check if we have all required keys
                        if path_info.required_keys.issubset(collected_keys):
                            new_g = g_score + path_info.distance
                            new_positions = tuple(
                                key if j == i else positions[j] 
                                for j in range(len(positions))
                            )
                            new_keys = collected_keys | {key}
                            new_state = (new_positions, new_keys)
                            
                            if new_state not in best_distance or best_distance[new_state] > new_g:
                                # Heuristic: remaining keys count
                                h_score = len(all_keys - new_keys)
                                f_score = new_g + h_score
                                heapq.heappush(heap, (f_score, new_g, new_positions, new_keys))
        
        return -1  # No solution found
    
    def get_maze_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the maze."""
        total_cells = self.height * self.width
        wall_count = sum(row.count('#') for row in self.grid)
        empty_count = total_cells - wall_count
        
        return {
            'width': self.width,
            'height': self.height,
            'total_cells': total_cells,
            'wall_count': wall_count,
            'empty_count': empty_count,
            'start_positions': len(self.start_positions),
            'key_count': len(self.keys),
            'door_count': len(self.doors),
            'keys': list(self.keys.keys()),
            'graph_size': sum(len(connections) for connections in self.graph.values())
        }
    
    def analyze_connectivity(self) -> Dict[str, Any]:
        """Analyze the connectivity and complexity of the maze."""
        analysis = {}
        
        # Key accessibility analysis
        key_accessibility = {}
        for key in self.keys:
            accessible_from = []
            for start_name in [f'@{i}' for i in range(len(self.start_positions))]:
                if key in self.graph[start_name]:
                    accessible_from.append(start_name)
            key_accessibility[key] = accessible_from
        
        analysis['key_accessibility'] = key_accessibility
        
        # Door dependency analysis
        door_dependencies = {}
        for key in self.keys:
            dependencies = set()
            for start_name in [f'@{i}' for i in range(len(self.start_positions))]:
                if key in self.graph[start_name]:
                    dependencies.update(self.graph[start_name][key].required_keys)
            door_dependencies[key] = list(dependencies)
        
        analysis['door_dependencies'] = door_dependencies
        
        # Calculate complexity metrics
        max_dependencies = max(len(deps) for deps in door_dependencies.values()) if door_dependencies else 0
        total_dependencies = sum(len(deps) for deps in door_dependencies.values())
        
        analysis['complexity'] = {
            'max_dependencies': max_dependencies,
            'total_dependencies': total_dependencies,
            'avg_dependencies': total_dependencies / len(self.keys) if self.keys else 0
        }
        
        return analysis

class Day18Solution(AdventSolution):
    """Enhanced solution for Advent of Code 2019 Day 18: Many-Worlds Interpretation."""
    
    def __init__(self):
        super().__init__(2019, 18, "Many-Worlds Interpretation")
        self.maze: Optional[KeyMaze] = None
    
    def _parse_input(self, input_data: str) -> str:
        """Parse input data and return maze string."""
        maze_data = input_data.strip()
        if not maze_data:
            # Fallback for testing
            maze_data = """#########
#b.A.@.a#
#########"""
        return maze_data
    
    def part1(self, input_data: str) -> int:
        """
        Find the shortest path to collect all keys with a single robot.
        
        Args:
            input_data: Raw input containing the maze
            
        Returns:
            Minimum steps to collect all keys
        """
        maze_data = self._parse_input(input_data)
        self.maze = KeyMaze(maze_data)
        
        return self.maze.solve_single_robot()
    
    def part2(self, input_data: str) -> int:
        """
        Find the shortest path to collect all keys with multiple robots.
        For part 2, the maze is modified to have 4 starting positions.
        
        Args:
            input_data: Raw input containing the maze
            
        Returns:
            Minimum steps to collect all keys with multiple robots
        """
        maze_data = self._parse_input(input_data)
        
        # For part 2, we need to modify the maze to have 4 robots
        # This typically involves replacing the center area around @ with walls
        # and creating 4 separate starting positions
        modified_maze_data = self._modify_maze_for_part2(maze_data)
        
        self.maze = KeyMaze(modified_maze_data)
        return self.maze.solve_multiple_robots()
    
    def _modify_maze_for_part2(self, maze_data: str) -> str:
        """
        Modify the maze for part 2 by splitting into 4 quadrants.
        
        Args:
            maze_data: Original maze data
            
        Returns:
            Modified maze data with 4 starting positions
        """
        lines = maze_data.strip().split('\n')
        grid = [list(line) for line in lines]
        
        # Find the original @ position
        start_pos = None
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == '@':
                    start_pos = (x, y)
                    break
            if start_pos:
                break
        
        if not start_pos:
            return maze_data  # No modification needed
        
        x, y = start_pos
        
        # Modify the 3x3 area around the start position
        # Replace with:
        # @#@
        # ###
        # @#@
        if (y-1 >= 0 and y+1 < len(grid) and 
            x-1 >= 0 and x+1 < len(grid[0])):
            
            # Set the pattern
            grid[y-1][x-1] = '@'  # Top-left
            grid[y-1][x] = '#'    # Top-center
            grid[y-1][x+1] = '@'  # Top-right
            grid[y][x-1] = '#'    # Middle-left
            grid[y][x] = '#'      # Middle-center
            grid[y][x+1] = '#'    # Middle-right
            grid[y+1][x-1] = '@'  # Bottom-left
            grid[y+1][x] = '#'    # Bottom-center
            grid[y+1][x+1] = '@'  # Bottom-right
        
        # Convert back to string
        return '\n'.join(''.join(row) for row in grid)
    
    def analyze_maze(self) -> Dict[str, Any]:
        """
        Provide comprehensive analysis of the key maze.
        
        Returns:
            Dictionary with detailed maze analysis
        """
        if self.maze is None:
            return {"error": "Maze not yet parsed"}
        
        stats = self.maze.get_maze_statistics()
        connectivity = self.maze.analyze_connectivity()
        
        return {
            'statistics': stats,
            'connectivity': connectivity,
            'analysis_timestamp': time.time()
        }
    
    def validate(self, expected_part1: Any = None, expected_part2: Any = None) -> bool:
        """Validate the solution with known test cases."""
        print("Day 18 validation: Testing with known examples...")
        
        # Test case 1: Simple maze
        test_maze1 = """#########
#b.A.@.a#
#########"""
        
        try:
            maze1 = KeyMaze(test_maze1)
            result1 = maze1.solve_single_robot()
            expected1 = 8  # Known result for this maze
            
            if result1 == expected1:
                print(f"✅ Test 1: {result1} steps (correct)")
            else:
                print(f"❌ Test 1: expected {expected1}, got {result1}")
                return False
            
            # Test case 2: More complex maze
            test_maze2 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""
            
            maze2 = KeyMaze(test_maze2)
            result2 = maze2.solve_single_robot()
            expected2 = 86  # Known result for this maze
            
            if result2 == expected2:
                print(f"✅ Test 2: {result2} steps (correct)")
            else:
                print(f"❌ Test 2: expected {expected2}, got {result2}")
                return False
            
            print("✅ All validation tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ Validation failed with error: {e}")
            return False

# Legacy compatibility functions
def part1(input_data: str = None) -> int:
    """Legacy function for part 1 compatibility with test runner."""
    solution = Day18Solution()
    if input_data is None:
        # Use default input discovery
        results = solution.run(part=1)
        return results.get('part1', 0)
    else:
        return solution.part1(input_data)

def part2(input_data: str = None) -> int:
    """Legacy function for part 2 compatibility with test runner."""
    solution = Day18Solution()
    if input_data is None:
        # Use default input discovery
        results = solution.run(part=2)
        return results.get('part2', 0)
    else:
        return solution.part2(input_data)

def solve_part1(input_file: str) -> int:
    """Legacy function for direct solving."""
    try:
        with open(input_file, 'r') as f:
            maze_data = f.read()
    except FileNotFoundError:
        # Return a default result for testing
        return -1
    
    maze = KeyMaze(maze_data)
    return maze.solve_single_robot()

def solve_part2(input_file: str) -> int:
    """Legacy function for direct solving."""
    solution = Day18Solution()
    try:
        with open(input_file, 'r') as f:
            input_data = f.read()
    except FileNotFoundError:
        # Return a default result for testing
        return -1
    
    return solution.part2(input_data)

def day18p1(input_file: str = "day18_input.txt") -> int:
    """Legacy function for part 1 with timing."""
    print(f"Solving part 1 for {input_file}...")
    start_time = time.time()
    result = solve_part1(input_file)
    elapsed = time.time() - start_time
    print(f"Part 1: {result} (solved in {elapsed:.2f}s)")
    return result

def day18p2(input_file: str = "day18_input2.txt") -> int:
    """Legacy function for part 2 with timing."""
    print(f"Solving part 2 for {input_file}...")
    start_time = time.time()
    result = solve_part2(input_file)
    elapsed = time.time() - start_time
    print(f"Part 2: {result} (solved in {elapsed:.2f}s)")
    return result

def main():
    """Main execution function."""
    solution = Day18Solution()
    solution.main()

if __name__ == "__main__":
    main()