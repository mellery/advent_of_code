#!/usr/bin/env python3
"""
Advent of Code Algorithm Libraries

This package provides reusable algorithm implementations extracted from 
migrated solutions. All algorithms are optimized for typical AoC constraints
and integrate seamlessly with the AdventSolution base class.

Available modules:
- pathfinding: Graph algorithms (BFS, DFS, Dijkstra, A*)
- grid: 2D grid utilities and transformations  
- vm: Virtual machine components and patterns
- parsing: Expression parsing and pattern matching
- math_utils: Mathematical utilities and number theory
- data_structures: Specialized data structures for AoC problems

Usage:
    from utils.algorithms import pathfinding, grid
    from utils.algorithms.pathfinding import dijkstra_grid
    from utils.algorithms.grid import Grid
"""

# Core algorithm imports for convenience
from .pathfinding import (
    dijkstra_grid,
    bfs_shortest_path,
    dfs_all_paths,
    a_star_search,
    PathfindingResult
)

from .grid import (
    Grid,
    Direction,
    Coordinate,
    DIRECTIONS_4,
    DIRECTIONS_8,
    parse_grid,
    neighbors_4,
    neighbors_8
)

from .vm import (
    VMBase,
    VMState,
    Instruction,
    ParameterMode
)

from .parsing import (
    ExpressionEvaluator,
    PatternMatcher,
    parse_numbers,
    extract_patterns
)

from .math_utils import (
    gcd,
    lcm,
    prime_factors,
    is_prime,
    manhattan_distance,
    euclidean_distance
)

__version__ = "1.0.0"
__author__ = "Advent of Code Enhanced Architecture"

# Algorithm performance categories for benchmarking
PERFORMANCE_TARGETS = {
    "pathfinding": {"fast": 0.1, "medium": 0.5, "slow": 2.0},
    "grid": {"fast": 0.05, "medium": 0.2, "slow": 1.0},
    "vm": {"fast": 0.1, "medium": 1.0, "slow": 5.0},
    "parsing": {"fast": 0.05, "medium": 0.2, "slow": 1.0},
    "math": {"fast": 0.01, "medium": 0.1, "slow": 0.5}
}

# Common AoC constraint assumptions
AOC_CONSTRAINTS = {
    "max_grid_size": 1000,
    "max_graph_nodes": 10000,
    "max_vm_memory": 100000,
    "max_expression_depth": 100
}