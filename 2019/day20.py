#!/usr/bin/env python3
"""
Advent of Code 2019 Day 20: Donut Maze
Enhanced solution with object-oriented design and comprehensive analysis.
"""

import sys
import os
from typing import Dict, List, Tuple, Optional, Set, Deque
from dataclasses import dataclass
from collections import deque, defaultdict
import time

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.advent_base import AdventSolution


@dataclass
class Point:
    """Represents a 2D coordinate point."""
    x: int
    y: int
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def neighbors(self) -> List['Point']:
        """Get adjacent points (up, down, left, right)."""
        return [
            Point(self.x, self.y - 1),  # up
            Point(self.x, self.y + 1),  # down
            Point(self.x - 1, self.y),  # left
            Point(self.x + 1, self.y)   # right
        ]


@dataclass
class Portal:
    """Represents a portal entrance/exit with name and position."""
    name: str
    position: Point
    is_outer: bool = False
    
    def __str__(self) -> str:
        location = "outer" if self.is_outer else "inner"
        return f"{self.name} at {self.position} ({location})"


@dataclass
class PortalPair:
    """Represents a pair of connected portals."""
    name: str
    entrance: Portal
    exit: Portal
    
    def get_destination(self, from_portal: Portal) -> Optional[Portal]:
        """Get the destination portal from a given starting portal."""
        if from_portal.position == self.entrance.position:
            return self.exit
        elif from_portal.position == self.exit.position:
            return self.entrance
        return None


@dataclass
class State:
    """Represents a state in the maze search (position and recursion level)."""
    position: Point
    level: int = 0
    
    def __hash__(self) -> int:
        return hash((self.position, self.level))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, State):
            return False
        return self.position == other.position and self.level == other.level


class PortalMaze:
    """
    Advanced portal maze navigation system.
    
    This class provides efficient maze parsing, portal detection,
    and pathfinding algorithms for both 2D and recursive 3D mazes.
    """
    
    def __init__(self, maze_data: str):
        """
        Initialize the PortalMaze with maze data.
        
        Args:
            maze_data: String representation of the maze
        """
        self.maze_lines = maze_data.strip().split('\n')
        self.height = len(self.maze_lines)
        self.width = max(len(line) for line in self.maze_lines) if self.maze_lines else 0
        
        # Normalize maze lines to same width
        self.maze = []
        for line in self.maze_lines:
            self.maze.append(line.ljust(self.width))
        
        self.portals: Dict[str, List[Portal]] = defaultdict(list)
        self.portal_pairs: Dict[str, PortalPair] = {}
        self.position_to_portal: Dict[Point, Portal] = {}
        self.walkable_positions: Set[Point] = set()
        
        self._parse_maze()
    
    def _parse_maze(self) -> None:
        """Parse the maze to identify walkable areas and portals."""
        # Find all walkable positions
        for y in range(self.height):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == '.':
                    self.walkable_positions.add(Point(x, y))
        
        # Find all portals
        self._find_portals()
        self._create_portal_pairs()
    
    def _find_portals(self) -> None:
        """Find all portal locations and their names."""
        for y in range(self.height):
            for x in range(len(self.maze[y])):
                char = self.maze[y][x]
                
                # Check if this is a letter (part of a portal name)
                if char.isalpha():
                    # Check horizontal portal (this letter + next letter)
                    if x + 1 < len(self.maze[y]) and self.maze[y][x + 1].isalpha():
                        portal_name = char + self.maze[y][x + 1]
                        # Find the adjacent '.' for the portal entrance
                        entrance_pos = self._find_portal_entrance(x, y, x + 1, y)
                        if entrance_pos:
                            is_outer = self._is_outer_portal(entrance_pos)
                            portal = Portal(portal_name, entrance_pos, is_outer)
                            self.portals[portal_name].append(portal)
                            self.position_to_portal[entrance_pos] = portal
                    
                    # Check vertical portal (this letter + next letter below)
                    if y + 1 < self.height and len(self.maze[y + 1]) > x and self.maze[y + 1][x].isalpha():
                        portal_name = char + self.maze[y + 1][x]
                        # Find the adjacent '.' for the portal entrance
                        entrance_pos = self._find_portal_entrance(x, y, x, y + 1)
                        if entrance_pos:
                            is_outer = self._is_outer_portal(entrance_pos)
                            portal = Portal(portal_name, entrance_pos, is_outer)
                            self.portals[portal_name].append(portal)
                            self.position_to_portal[entrance_pos] = portal
    
    def _find_portal_entrance(self, x1: int, y1: int, x2: int, y2: int) -> Optional[Point]:
        """Find the '.' position adjacent to a portal name."""
        # Check positions around the portal name letters
        positions_to_check = [
            Point(x1 - 1, y1), Point(x2 + 1, y2),  # horizontal
            Point(x1, y1 - 1), Point(x2, y2 + 1)   # vertical
        ]
        
        for pos in positions_to_check:
            if (0 <= pos.x < self.width and 0 <= pos.y < self.height and
                pos.x < len(self.maze[pos.y]) and
                self.maze[pos.y][pos.x] == '.'):
                return pos
        
        return None
    
    def _is_outer_portal(self, position: Point) -> bool:
        """Determine if a portal is on the outer edge of the maze."""
        # A portal is outer if it's close to the maze boundaries
        margin = 3  # Portals within 3 cells of edge are considered outer
        return (position.x <= margin or position.x >= self.width - margin - 1 or
                position.y <= margin or position.y >= self.height - margin - 1)
    
    def _create_portal_pairs(self) -> None:
        """Create portal pairs from individual portals."""
        for name, portal_list in self.portals.items():
            if len(portal_list) == 2:
                # Regular portal pair
                portal1, portal2 = portal_list
                self.portal_pairs[name] = PortalPair(name, portal1, portal2)
            elif len(portal_list) == 1 and name in ['AA', 'ZZ']:
                # Start/end portals (no pair)
                continue
    
    def get_neighbors(self, position: Point) -> List[Point]:
        """Get valid neighboring positions from a given point."""
        neighbors = []
        for neighbor in position.neighbors():
            if neighbor in self.walkable_positions:
                neighbors.append(neighbor)
        return neighbors
    
    def find_shortest_path(self, start_name: str = 'AA', end_name: str = 'ZZ', 
                          recursive: bool = False) -> Optional[int]:
        """
        Find the shortest path between start and end portals.
        
        Args:
            start_name: Name of starting portal
            end_name: Name of ending portal
            recursive: Whether to use recursive maze rules
            
        Returns:
            Shortest path length, or None if no path exists
        """
        # Find start and end positions
        start_portals = self.portals.get(start_name, [])
        end_portals = self.portals.get(end_name, [])
        
        if not start_portals or not end_portals:
            return None
        
        start_pos = start_portals[0].position
        end_pos = end_portals[0].position
        
        if recursive:
            return self._find_recursive_path(start_pos, end_pos)
        else:
            return self._find_simple_path(start_pos, end_pos)
    
    def _find_simple_path(self, start: Point, end: Point) -> Optional[int]:
        """Find shortest path in 2D maze (non-recursive)."""
        queue: Deque[Tuple[Point, int]] = deque([(start, 0)])
        visited: Set[Point] = {start}
        
        while queue:
            position, distance = queue.popleft()
            
            if position == end:
                return distance
            
            # Check regular movement
            for neighbor in self.get_neighbors(position):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
            
            # Check portal teleportation
            if position in self.position_to_portal:
                portal = self.position_to_portal[position]
                if portal.name in self.portal_pairs:
                    pair = self.portal_pairs[portal.name]
                    destination = pair.get_destination(portal)
                    if destination and destination.position not in visited:
                        visited.add(destination.position)
                        queue.append((destination.position, distance + 1))
        
        return None
    
    def _find_recursive_path(self, start: Point, end: Point) -> Optional[int]:
        """Find shortest path in recursive 3D maze."""
        queue: Deque[Tuple[State, int]] = deque([(State(start, 0), 0)])
        visited: Set[State] = {State(start, 0)}
        
        while queue:
            state, distance = queue.popleft()
            
            # Can only exit at level 0
            if state.position == end and state.level == 0:
                return distance
            
            # Check regular movement (same level)
            for neighbor in self.get_neighbors(state.position):
                new_state = State(neighbor, state.level)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, distance + 1))
            
            # Check portal teleportation
            if state.position in self.position_to_portal:
                portal = self.position_to_portal[state.position]
                if portal.name in self.portal_pairs:
                    pair = self.portal_pairs[portal.name]
                    destination = pair.get_destination(portal)
                    
                    if destination:
                        # Calculate new level based on outer/inner portal rules
                        new_level = state.level
                        if portal.is_outer:
                            new_level -= 1
                        else:
                            new_level += 1
                        
                        # Can't go to negative levels
                        if new_level >= 0:
                            new_state = State(destination.position, new_level)
                            if new_state not in visited:
                                visited.add(new_state)
                                queue.append((new_state, distance + 1))
        
        return None
    
    def get_maze_statistics(self) -> Dict[str, any]:
        """Get comprehensive statistics about the maze."""
        portal_count = sum(len(portals) for portals in self.portals.values())
        outer_portals = sum(1 for portals in self.portals.values() 
                           for portal in portals if portal.is_outer)
        inner_portals = portal_count - outer_portals
        
        return {
            'dimensions': (self.width, self.height),
            'walkable_positions': len(self.walkable_positions),
            'total_portals': portal_count,
            'portal_pairs': len(self.portal_pairs),
            'outer_portals': outer_portals,
            'inner_portals': inner_portals,
            'portal_names': list(self.portals.keys())
        }
    
    def visualize_portals(self) -> str:
        """Create a visualization showing portal locations."""
        lines = []
        for y in range(min(self.height, 50)):  # Limit size for readability
            line = ""
            for x in range(min(len(self.maze[y]), 80)):
                pos = Point(x, y)
                if pos in self.position_to_portal:
                    portal = self.position_to_portal[pos]
                    line += 'O' if portal.is_outer else 'I'
                elif pos in self.walkable_positions:
                    line += '.'
                else:
                    line += self.maze[y][x] if x < len(self.maze[y]) else ' '
            lines.append(line)
        
        return '\n'.join(lines)


class Day20Solution(AdventSolution):
    """Enhanced solution for Advent of Code 2019 Day 20: Donut Maze."""
    
    def __init__(self):
        super().__init__(year=2019, day=20, title="Donut Maze")
    
    def part1(self, input_data: str) -> int:
        """
        Find shortest path through the donut maze (2D).
        
        Args:
            input_data: Maze layout as string
            
        Returns:
            Shortest path length from AA to ZZ
        """
        maze = PortalMaze(input_data)
        result = maze.find_shortest_path('AA', 'ZZ', recursive=False)
        return result if result is not None else -1
    
    def part2(self, input_data: str) -> int:
        """
        Find shortest path through the recursive donut maze (3D).
        
        Args:
            input_data: Maze layout as string
            
        Returns:
            Shortest path length from AA to ZZ in recursive maze
        """
        maze = PortalMaze(input_data)
        result = maze.find_shortest_path('AA', 'ZZ', recursive=True)
        return result if result is not None else -1
    
    def analyze(self, input_data: str) -> None:
        """
        Provide comprehensive analysis of the donut maze.
        
        Args:
            input_data: Maze layout as string
        """
        maze = PortalMaze(input_data)
        
        print("=== Donut Maze Analysis ===\n")
        
        # Maze statistics
        stats = maze.get_maze_statistics()
        print("Maze Statistics:")
        print(f"  Dimensions: {stats['dimensions'][0]} x {stats['dimensions'][1]}")
        print(f"  Walkable positions: {stats['walkable_positions']}")
        print(f"  Total portals: {stats['total_portals']}")
        print(f"  Portal pairs: {stats['portal_pairs']}")
        print(f"  Outer portals: {stats['outer_portals']}")
        print(f"  Inner portals: {stats['inner_portals']}")
        print(f"  Portal names: {', '.join(sorted(stats['portal_names']))}")
        
        # Portal details
        print(f"\nPortal Details:")
        for name, portals in sorted(maze.portals.items()):
            for portal in portals:
                print(f"  {portal}")
        
        # Part 1 analysis
        print(f"\nPart 1 Analysis (2D maze):")
        start_time = time.time()
        path1 = maze.find_shortest_path('AA', 'ZZ', recursive=False)
        time1 = time.time() - start_time
        
        if path1 is not None:
            print(f"  Shortest path length: {path1}")
            print(f"  Search time: {time1:.4f} seconds")
        else:
            print("  No path found")
        
        # Part 2 analysis
        print(f"\nPart 2 Analysis (recursive 3D maze):")
        start_time = time.time()
        path2 = maze.find_shortest_path('AA', 'ZZ', recursive=True)
        time2 = time.time() - start_time
        
        if path2 is not None:
            print(f"  Shortest path length: {path2}")
            print(f"  Search time: {time2:.4f} seconds")
        else:
            print("  No path found")
        
        # Complexity comparison
        if path1 is not None and path2 is not None:
            print(f"\nComplexity Comparison:")
            print(f"  2D vs 3D path length ratio: {path2/path1:.2f}")
            print(f"  2D vs 3D search time ratio: {time2/time1:.2f}")
        
        # Portal layout visualization (limited size)
        print(f"\nPortal Layout (O=outer, I=inner, .=walkable):")
        visualization = maze.visualize_portals()
        lines = visualization.split('\n')
        for i, line in enumerate(lines[:20]):  # Show first 20 lines
            print(f"  {line}")
        if len(lines) > 20:
            print(f"  ... ({len(lines) - 20} more lines)")
        
        print(f"\nResults:")
        if path1 is not None:
            print(f"  Part 1: {path1}")
        if path2 is not None:
            print(f"  Part 2: {path2}")


# Legacy functions for test runner compatibility
def part1(filename: str) -> int:
    """Legacy part1 function for test runner compatibility."""
    try:
        with open(filename, 'r') as f:
            input_data = f.read()
    except FileNotFoundError:
        return -1
    
    solution = Day20Solution()
    return solution.part1(input_data)


def part2(filename: str) -> int:
    """Legacy part2 function for test runner compatibility."""
    try:
        with open(filename, 'r') as f:
            input_data = f.read()
    except FileNotFoundError:
        return -1
    
    solution = Day20Solution()
    return solution.part2(input_data)


if __name__ == "__main__":
    solution = Day20Solution()
    solution.main()