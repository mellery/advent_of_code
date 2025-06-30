#!/usr/bin/env python3
"""
Pathfinding and Graph Algorithm Library

Extracted from migrated AoC solutions with optimizations for typical AoC constraints.
All algorithms support both grid-based and general graph pathfinding.

Key Features:
- Grid-based pathfinding with 4/8-directional movement
- General graph algorithms with custom edge weights
- NetworkX integration with graceful fallback
- Memory-efficient implementations for large grids
- Comprehensive result objects with path reconstruction

Performance Targets:
- Grid pathfinding: < 500ms for 1000x1000 grids
- General graphs: < 1s for 10,000 nodes
- Memory usage: < 200MB for typical AoC problems
"""

import heapq
from collections import deque, defaultdict
from typing import (
    Dict, List, Tuple, Set, Optional, Callable, Union, Any,
    NamedTuple, TypeVar, Generic
)
from dataclasses import dataclass
from enum import Enum

# Type definitions
Coordinate = Tuple[int, int]
Node = TypeVar('Node')
Weight = Union[int, float]
Graph = Dict[Node, Dict[Node, Weight]]

class PathfindingAlgorithm(Enum):
    """Available pathfinding algorithms."""
    BFS = "bfs"
    DFS = "dfs" 
    DIJKSTRA = "dijkstra"
    A_STAR = "a_star"

@dataclass
class PathfindingResult:
    """Result object for pathfinding operations."""
    algorithm: PathfindingAlgorithm
    start: Any
    end: Any
    found: bool = False
    distance: Weight = float('inf')
    path: List[Any] = None
    nodes_explored: int = 0
    execution_time: float = 0.0
    
    def __post_init__(self):
        if self.path is None:
            self.path = []

class GridPathfinder:
    """Optimized pathfinding for 2D grids."""
    
    def __init__(self, grid: Dict[Coordinate, Any], 
                 directions: int = 4,
                 wall_value: Any = '#',
                 passable_fn: Optional[Callable[[Any], bool]] = None):
        """
        Initialize grid pathfinder.
        
        Args:
            grid: Dictionary mapping (row, col) to cell values
            directions: 4 or 8 directional movement
            wall_value: Value representing impassable cells
            passable_fn: Custom function to determine if cell is passable
        """
        self.grid = grid
        self.directions = directions
        self.wall_value = wall_value
        self.passable_fn = passable_fn or (lambda cell: cell != wall_value)
        
        # Cache grid bounds for efficiency
        if grid:
            coords = list(grid.keys())
            self.min_row = min(r for r, c in coords)
            self.max_row = max(r for r, c in coords)
            self.min_col = min(c for r, c in coords)
            self.max_col = max(c for r, c in coords)
        else:
            self.min_row = self.max_row = self.min_col = self.max_col = 0
    
    def neighbors(self, pos: Coordinate) -> List[Coordinate]:
        """Get valid neighbors for a grid position."""
        row, col = pos
        if self.directions == 4:
            deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        else:  # 8 directions
            deltas = [(0, 1), (1, 0), (0, -1), (-1, 0), 
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        neighbors = []
        for dr, dc in deltas:
            new_row, new_col = row + dr, col + dc
            new_pos = (new_row, new_col)
            
            # Check bounds and passability
            if (self.min_row <= new_row <= self.max_row and 
                self.min_col <= new_col <= self.max_col and
                new_pos in self.grid and
                self.passable_fn(self.grid[new_pos])):
                neighbors.append(new_pos)
        
        return neighbors
    
    def get_weight(self, from_pos: Coordinate, to_pos: Coordinate) -> Weight:
        """Get edge weight between adjacent positions."""
        # Default: uniform weight of 1
        # Override for weighted grids (e.g., risk levels)
        return 1
    
    def heuristic(self, pos: Coordinate, goal: Coordinate) -> Weight:
        """Heuristic function for A* (Manhattan distance by default)."""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def dijkstra_grid(grid: Dict[Coordinate, Any],
                  start: Coordinate,
                  end: Coordinate,
                  directions: int = 4,
                  weight_fn: Optional[Callable[[Coordinate, Coordinate], Weight]] = None,
                  passable_fn: Optional[Callable[[Any], bool]] = None) -> PathfindingResult:
    """
    Dijkstra's algorithm optimized for grid pathfinding.
    
    Extracted from 2021 Day 15 (Chiton) with performance optimizations.
    
    Args:
        grid: Dictionary mapping (row, col) to cell values
        start: Starting coordinate
        end: Target coordinate  
        directions: 4 or 8 directional movement
        weight_fn: Function to calculate edge weights
        passable_fn: Function to determine if cell is passable
        
    Returns:
        PathfindingResult with path and distance information
    """
    import time
    start_time = time.time()
    
    pathfinder = GridPathfinder(grid, directions, passable_fn=passable_fn)
    
    # Default weight function
    if weight_fn is None:
        weight_fn = lambda from_pos, to_pos: pathfinder.get_weight(from_pos, to_pos)
    
    # Priority queue: (distance, position)
    pq = [(0, start)]
    distances = {start: 0}
    previous = {}
    explored = 0
    
    while pq:
        current_dist, current_pos = heapq.heappop(pq)
        explored += 1
        
        if current_pos == end:
            # Reconstruct path
            path = []
            pos = end
            while pos is not None:
                path.append(pos)
                pos = previous.get(pos)
            path.reverse()
            
            return PathfindingResult(
                algorithm=PathfindingAlgorithm.DIJKSTRA,
                start=start,
                end=end,
                found=True,
                distance=current_dist,
                path=path,
                nodes_explored=explored,
                execution_time=time.time() - start_time
            )
        
        if current_dist > distances.get(current_pos, float('inf')):
            continue
        
        for neighbor in pathfinder.neighbors(current_pos):
            weight = weight_fn(current_pos, neighbor)
            distance = current_dist + weight
            
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                previous[neighbor] = current_pos
                heapq.heappush(pq, (distance, neighbor))
    
    return PathfindingResult(
        algorithm=PathfindingAlgorithm.DIJKSTRA,
        start=start,
        end=end,
        found=False,
        nodes_explored=explored,
        execution_time=time.time() - start_time
    )

def bfs_shortest_path(grid: Dict[Coordinate, Any],
                      start: Coordinate, 
                      end: Coordinate,
                      directions: int = 4,
                      passable_fn: Optional[Callable[[Any], bool]] = None) -> PathfindingResult:
    """
    BFS shortest path for unweighted grids.
    
    Optimized for cases where all edges have equal weight.
    
    Args:
        grid: Dictionary mapping (row, col) to cell values
        start: Starting coordinate
        end: Target coordinate
        directions: 4 or 8 directional movement
        passable_fn: Function to determine if cell is passable
        
    Returns:
        PathfindingResult with path and distance information
    """
    import time
    start_time = time.time()
    
    pathfinder = GridPathfinder(grid, directions, passable_fn=passable_fn)
    
    queue = deque([(start, 0)])
    visited = {start}
    previous = {}
    explored = 0
    
    while queue:
        current_pos, distance = queue.popleft()
        explored += 1
        
        if current_pos == end:
            # Reconstruct path
            path = []
            pos = end
            while pos is not None:
                path.append(pos)
                pos = previous.get(pos)
            path.reverse()
            
            return PathfindingResult(
                algorithm=PathfindingAlgorithm.BFS,
                start=start,
                end=end,
                found=True,
                distance=distance,
                path=path,
                nodes_explored=explored,
                execution_time=time.time() - start_time
            )
        
        for neighbor in pathfinder.neighbors(current_pos):
            if neighbor not in visited:
                visited.add(neighbor)
                previous[neighbor] = current_pos
                queue.append((neighbor, distance + 1))
    
    return PathfindingResult(
        algorithm=PathfindingAlgorithm.BFS,
        start=start,
        end=end,
        found=False,
        nodes_explored=explored,
        execution_time=time.time() - start_time
    )

def dfs_all_paths(grid: Dict[Coordinate, Any],
                  start: Coordinate,
                  end: Coordinate,
                  directions: int = 4,
                  passable_fn: Optional[Callable[[Any], bool]] = None,
                  max_paths: int = 1000,
                  path_constraint_fn: Optional[Callable[[List[Coordinate]], bool]] = None) -> List[List[Coordinate]]:
    """
    Find all paths using DFS with constraints.
    
    Extracted from 2021 Day 12 (Passage Pathing) patterns.
    
    Args:
        grid: Dictionary mapping (row, col) to cell values
        start: Starting coordinate
        end: Target coordinate
        directions: 4 or 8 directional movement  
        passable_fn: Function to determine if cell is passable
        max_paths: Maximum number of paths to find (prevent infinite search)
        path_constraint_fn: Function to validate path constraints
        
    Returns:
        List of all valid paths as coordinate lists
    """
    pathfinder = GridPathfinder(grid, directions, passable_fn=passable_fn)
    all_paths = []
    
    def dfs_recursive(current_pos: Coordinate, path: List[Coordinate], visited: Set[Coordinate]):
        if len(all_paths) >= max_paths:
            return
        
        if current_pos == end:
            if path_constraint_fn is None or path_constraint_fn(path):
                all_paths.append(path.copy())
            return
        
        for neighbor in pathfinder.neighbors(current_pos):
            if neighbor not in visited:
                path.append(neighbor)
                visited.add(neighbor)
                dfs_recursive(neighbor, path, visited)
                path.pop()
                visited.remove(neighbor)
    
    dfs_recursive(start, [start], {start})
    return all_paths

def a_star_search(grid: Dict[Coordinate, Any],
                  start: Coordinate,
                  end: Coordinate, 
                  directions: int = 4,
                  weight_fn: Optional[Callable[[Coordinate, Coordinate], Weight]] = None,
                  heuristic_fn: Optional[Callable[[Coordinate, Coordinate], Weight]] = None,
                  passable_fn: Optional[Callable[[Any], bool]] = None) -> PathfindingResult:
    """
    A* search algorithm for optimal pathfinding with heuristic.
    
    Args:
        grid: Dictionary mapping (row, col) to cell values
        start: Starting coordinate
        end: Target coordinate
        directions: 4 or 8 directional movement
        weight_fn: Function to calculate edge weights
        heuristic_fn: Heuristic function (defaults to Manhattan distance)
        passable_fn: Function to determine if cell is passable
        
    Returns:
        PathfindingResult with path and distance information
    """
    import time
    start_time = time.time()
    
    pathfinder = GridPathfinder(grid, directions, passable_fn=passable_fn)
    
    # Default functions
    if weight_fn is None:
        weight_fn = lambda from_pos, to_pos: pathfinder.get_weight(from_pos, to_pos)
    if heuristic_fn is None:
        heuristic_fn = pathfinder.heuristic
    
    # Priority queue: (f_score, g_score, position)
    pq = [(heuristic_fn(start, end), 0, start)]
    g_scores = {start: 0}
    previous = {}
    explored = 0
    
    while pq:
        f_score, g_score, current_pos = heapq.heappop(pq)
        explored += 1
        
        if current_pos == end:
            # Reconstruct path
            path = []
            pos = end
            while pos is not None:
                path.append(pos)
                pos = previous.get(pos)
            path.reverse()
            
            return PathfindingResult(
                algorithm=PathfindingAlgorithm.A_STAR,
                start=start,
                end=end,
                found=True,
                distance=g_score,
                path=path,
                nodes_explored=explored,
                execution_time=time.time() - start_time
            )
        
        if g_score > g_scores.get(current_pos, float('inf')):
            continue
        
        for neighbor in pathfinder.neighbors(current_pos):
            tentative_g = g_score + weight_fn(current_pos, neighbor)
            
            if tentative_g < g_scores.get(neighbor, float('inf')):
                g_scores[neighbor] = tentative_g
                previous[neighbor] = current_pos
                f_score = tentative_g + heuristic_fn(neighbor, end)
                heapq.heappush(pq, (f_score, tentative_g, neighbor))
    
    return PathfindingResult(
        algorithm=PathfindingAlgorithm.A_STAR,
        start=start,
        end=end,
        found=False,
        nodes_explored=explored,
        execution_time=time.time() - start_time
    )

# NetworkX integration with fallback
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
    
    def dijkstra_networkx_fallback(graph: Graph, start: Node, end: Node) -> PathfindingResult:
        """NetworkX Dijkstra implementation as fallback for complex graphs."""
        import time
        start_time = time.time()
        
        G = nx.DiGraph()
        for node, edges in graph.items():
            for neighbor, weight in edges.items():
                G.add_edge(node, neighbor, weight=weight)
        
        try:
            path = nx.shortest_path(G, start, end, weight='weight')
            distance = nx.shortest_path_length(G, start, end, weight='weight')
            
            return PathfindingResult(
                algorithm=PathfindingAlgorithm.DIJKSTRA,
                start=start,
                end=end,
                found=True,
                distance=distance,
                path=path,
                nodes_explored=len(G.nodes),
                execution_time=time.time() - start_time
            )
        except nx.NetworkXNoPath:
            return PathfindingResult(
                algorithm=PathfindingAlgorithm.DIJKSTRA,
                start=start,
                end=end,
                found=False,
                execution_time=time.time() - start_time
            )
            
except ImportError:
    NETWORKX_AVAILABLE = False
    
    def dijkstra_networkx_fallback(graph: Graph, start: Node, end: Node) -> PathfindingResult:
        """Fallback when NetworkX is not available."""
        raise ImportError("NetworkX not available for complex graph algorithms")

# Convenience function for automatic algorithm selection
def find_path(grid: Dict[Coordinate, Any],
              start: Coordinate,
              end: Coordinate,
              algorithm: str = "auto",
              **kwargs) -> PathfindingResult:
    """
    Automatic pathfinding algorithm selection.
    
    Args:
        grid: Dictionary mapping (row, col) to cell values
        start: Starting coordinate
        end: Target coordinate
        algorithm: "auto", "bfs", "dijkstra", or "a_star"
        **kwargs: Additional arguments passed to pathfinding function
        
    Returns:
        PathfindingResult with optimal algorithm choice
    """
    if algorithm == "auto":
        # Choose algorithm based on grid characteristics
        grid_size = len(grid)
        has_weights = "weight_fn" in kwargs
        
        if grid_size < 1000 and not has_weights:
            algorithm = "bfs"
        elif has_weights:
            algorithm = "dijkstra"
        else:
            algorithm = "a_star"
    
    algorithms = {
        "bfs": bfs_shortest_path,
        "dijkstra": dijkstra_grid,
        "a_star": a_star_search
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    return algorithms[algorithm](grid, start, end, **kwargs)