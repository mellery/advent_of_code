#!/usr/bin/env python3
"""
Grid Utilities and 2D Operations Library

Comprehensive 2D grid manipulation library extracted from migrated AoC solutions.
Optimized for typical AoC grid operations with consistent coordinate systems.

Key Features:
- Flexible Grid class with multiple coordinate systems
- Grid transformations (rotation, reflection, scaling)
- Neighbor iteration with 4/8-directional support
- Efficient grid parsing from string input
- Coordinate conversion utilities
- Pattern detection and region analysis

Performance Targets:
- Grid operations: < 50ms for 1000x1000 grids
- Transformations: < 100ms for typical AoC grids
- Memory usage: < 100MB for large grids
"""

from typing import (
    Dict, List, Tuple, Set, Optional, Callable, Union, Any,
    Iterator, TypeVar, Generic
)
from dataclasses import dataclass
from enum import Enum
import re

# Type definitions
Coordinate = Tuple[int, int]
CellValue = TypeVar('CellValue')

class Direction(Enum):
    """Cardinal and intercardinal directions."""
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)
    NORTHEAST = (1, -1)
    NORTHWEST = (-1, -1)
    SOUTHEAST = (1, 1)
    SOUTHWEST = (-1, 1)
    
    # Convenient aliases
    UP = NORTH
    DOWN = SOUTH
    RIGHT = EAST
    LEFT = WEST

# Common direction sets
DIRECTIONS_4 = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
DIRECTIONS_8 = [
    Direction.NORTH, Direction.NORTHEAST, Direction.EAST, Direction.SOUTHEAST,
    Direction.SOUTH, Direction.SOUTHWEST, Direction.WEST, Direction.NORTHWEST
]

# Direction vectors as tuples (for legacy compatibility)
DIRECTION_VECTORS_4 = [(0, -1), (1, 0), (0, 1), (-1, 0)]
DIRECTION_VECTORS_8 = [
    (0, -1), (1, -1), (1, 0), (1, 1),
    (0, 1), (-1, 1), (-1, 0), (-1, -1)
]

@dataclass
class GridBounds:
    """Grid boundary information."""
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    
    @property
    def width(self) -> int:
        return self.max_x - self.min_x + 1
    
    @property
    def height(self) -> int:
        return self.max_y - self.min_y + 1
    
    @property
    def area(self) -> int:
        return self.width * self.height
    
    def contains(self, x: int, y: int) -> bool:
        """Check if coordinate is within bounds."""
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

class Grid(Generic[CellValue]):
    """
    Flexible 2D grid implementation optimized for AoC problems.
    
    Supports multiple coordinate systems and efficient operations.
    Extracted patterns from 2020 Day 20, 2021 Day 15, and other grid-based solutions.
    """
    
    def __init__(self, 
                 data: Optional[Dict[Coordinate, CellValue]] = None,
                 default_value: Optional[CellValue] = None,
                 coordinate_system: str = "xy"):
        """
        Initialize grid.
        
        Args:
            data: Initial grid data as coordinate->value mapping
            default_value: Default value for unset coordinates
            coordinate_system: "xy" (x=col, y=row) or "rc" (row, col)
        """
        self.data: Dict[Coordinate, CellValue] = data or {}
        self.default_value = default_value
        self.coordinate_system = coordinate_system
        
        # Cache bounds for performance
        self._bounds_cache: Optional[GridBounds] = None
        self._bounds_dirty = True
    
    def __getitem__(self, coord: Coordinate) -> CellValue:
        """Get cell value at coordinate."""
        if coord in self.data:
            return self.data[coord]
        elif self.default_value is not None:
            return self.default_value
        else:
            raise KeyError(f"Coordinate {coord} not in grid")
    
    def __setitem__(self, coord: Coordinate, value: CellValue):
        """Set cell value at coordinate."""
        self.data[coord] = value
        self._bounds_dirty = True
    
    def __contains__(self, coord: Coordinate) -> bool:
        """Check if coordinate exists in grid."""
        return coord in self.data
    
    def __len__(self) -> int:
        """Get number of cells in grid."""
        return len(self.data)
    
    def __iter__(self) -> Iterator[Coordinate]:
        """Iterate over coordinates."""
        return iter(self.data)
    
    def items(self) -> Iterator[Tuple[Coordinate, CellValue]]:
        """Iterate over coordinate-value pairs."""
        return self.data.items()
    
    def values(self) -> Iterator[CellValue]:
        """Iterate over cell values."""
        return self.data.values()
    
    def keys(self) -> Iterator[Coordinate]:
        """Iterate over coordinates."""
        return self.data.keys()
    
    @property
    def bounds(self) -> GridBounds:
        """Get grid boundaries."""
        if self._bounds_dirty or self._bounds_cache is None:
            self._update_bounds()
        return self._bounds_cache
    
    def _update_bounds(self):
        """Update cached bounds."""
        if not self.data:
            self._bounds_cache = GridBounds(0, 0, 0, 0)
        else:
            coords = list(self.data.keys())
            if self.coordinate_system == "xy":
                xs, ys = zip(*coords)
                self._bounds_cache = GridBounds(min(xs), max(xs), min(ys), max(ys))
            else:  # rc system
                ys, xs = zip(*coords)
                self._bounds_cache = GridBounds(min(xs), max(xs), min(ys), max(ys))
        
        self._bounds_dirty = False
    
    def get(self, coord: Coordinate, default: Optional[CellValue] = None) -> CellValue:
        """Get cell value with optional default."""
        return self.data.get(coord, default or self.default_value)
    
    def neighbors(self, coord: Coordinate, 
                  directions: int = 4,
                  include_diagonals: bool = None) -> List[Coordinate]:
        """
        Get neighbor coordinates.
        
        Args:
            coord: Center coordinate
            directions: 4 or 8 (overrides include_diagonals)
            include_diagonals: Include diagonal neighbors (legacy parameter)
            
        Returns:
            List of valid neighbor coordinates
        """
        if include_diagonals is not None:
            directions = 8 if include_diagonals else 4
        
        x, y = coord
        if directions == 4:
            deltas = DIRECTION_VECTORS_4
        else:
            deltas = DIRECTION_VECTORS_8
        
        neighbors = []
        for dx, dy in deltas:
            neighbor = (x + dx, y + dy)
            if neighbor in self.data:
                neighbors.append(neighbor)
        
        return neighbors
    
    def neighbors_bounded(self, coord: Coordinate, 
                         directions: int = 4) -> List[Coordinate]:
        """Get neighbors within grid bounds."""
        x, y = coord
        bounds = self.bounds
        
        if directions == 4:
            deltas = DIRECTION_VECTORS_4
        else:
            deltas = DIRECTION_VECTORS_8
        
        neighbors = []
        for dx, dy in deltas:
            new_x, new_y = x + dx, y + dy
            if bounds.contains(new_x, new_y):
                neighbors.append((new_x, new_y))
        
        return neighbors
    
    def rotate_90(self, clockwise: bool = True) -> 'Grid[CellValue]':
        """
        Rotate grid 90 degrees.
        
        Extracted from 2020 Day 20 (Jurassic Jigsaw) piece rotation logic.
        """
        rotated_data = {}
        bounds = self.bounds
        
        for (x, y), value in self.data.items():
            if clockwise:
                # (x, y) -> (y, width - 1 - x)
                new_x = y - bounds.min_y
                new_y = bounds.max_x - x
            else:
                # (x, y) -> (height - 1 - y, x)  
                new_x = bounds.max_y - y
                new_y = x - bounds.min_x
            
            rotated_data[(new_x, new_y)] = value
        
        return Grid(rotated_data, self.default_value, self.coordinate_system)
    
    def rotate_180(self) -> 'Grid[CellValue]':
        """Rotate grid 180 degrees."""
        return self.rotate_90().rotate_90()
    
    def rotate_270(self) -> 'Grid[CellValue]':
        """Rotate grid 270 degrees (or 90 counter-clockwise)."""
        return self.rotate_90(clockwise=False)
    
    def flip_horizontal(self) -> 'Grid[CellValue]':
        """Flip grid horizontally (mirror over vertical axis)."""
        flipped_data = {}
        bounds = self.bounds
        
        for (x, y), value in self.data.items():
            new_x = bounds.max_x - x + bounds.min_x
            flipped_data[(new_x, y)] = value
        
        return Grid(flipped_data, self.default_value, self.coordinate_system)
    
    def flip_vertical(self) -> 'Grid[CellValue]':
        """Flip grid vertically (mirror over horizontal axis)."""
        flipped_data = {}
        bounds = self.bounds
        
        for (x, y), value in self.data.items():
            new_y = bounds.max_y - y + bounds.min_y
            flipped_data[(x, new_y)] = value
        
        return Grid(flipped_data, self.default_value, self.coordinate_system)
    
    def all_orientations(self) -> List['Grid[CellValue]']:
        """
        Generate all 8 possible orientations (4 rotations × 2 flips).
        
        Useful for pattern matching where orientation is unknown.
        """
        orientations = []
        
        # Original and 3 rotations
        current = self
        for _ in range(4):
            orientations.append(current)
            current = current.rotate_90()
        
        # Flipped and 3 rotations of flipped
        current = self.flip_horizontal()
        for _ in range(4):
            orientations.append(current)
            current = current.rotate_90()
        
        return orientations
    
    def extract_region(self, top_left: Coordinate, 
                      bottom_right: Coordinate) -> 'Grid[CellValue]':
        """Extract rectangular region as new grid."""
        x1, y1 = top_left
        x2, y2 = bottom_right
        
        region_data = {}
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if (x, y) in self.data:
                    # Offset coordinates to start from (0, 0)
                    region_data[(x - x1, y - y1)] = self.data[(x, y)]
        
        return Grid(region_data, self.default_value, self.coordinate_system)
    
    def expand(self, factor: int, 
               expansion_fn: Optional[Callable[[Coordinate, CellValue], CellValue]] = None) -> 'Grid[CellValue]':
        """
        Expand grid by given factor.
        
        Extracted from 2021 Day 15 (Chiton) 5x5 grid expansion logic.
        
        Args:
            factor: Expansion factor (e.g., 5 for 5x5 expansion)
            expansion_fn: Function to transform values in expanded regions
        """
        expanded_data = {}
        bounds = self.bounds
        
        for tile_x in range(factor):
            for tile_y in range(factor):
                for (x, y), value in self.data.items():
                    # Calculate new coordinates
                    new_x = x + tile_x * bounds.width
                    new_y = y + tile_y * bounds.height
                    
                    # Apply expansion transformation if provided
                    if expansion_fn:
                        new_value = expansion_fn((tile_x, tile_y), value)
                    else:
                        new_value = value
                    
                    expanded_data[(new_x, new_y)] = new_value
        
        return Grid(expanded_data, self.default_value, self.coordinate_system)
    
    def find_pattern(self, pattern: 'Grid[CellValue]',
                     allow_rotations: bool = False) -> List[Coordinate]:
        """
        Find all occurrences of pattern in grid.
        
        Args:
            pattern: Pattern grid to search for
            allow_rotations: Search all 8 orientations of pattern
            
        Returns:
            List of top-left coordinates where pattern was found
        """
        matches = []
        patterns_to_check = [pattern]
        
        if allow_rotations:
            patterns_to_check = pattern.all_orientations()
        
        for p in patterns_to_check:
            p_bounds = p.bounds
            bounds = self.bounds
            
            # Check each possible position
            for x in range(bounds.min_x, bounds.max_x - p_bounds.width + 2):
                for y in range(bounds.min_y, bounds.max_y - p_bounds.height + 2):
                    if self._pattern_matches_at(p, x, y):
                        matches.append((x, y))
        
        return matches
    
    def _pattern_matches_at(self, pattern: 'Grid[CellValue]',
                           offset_x: int, offset_y: int) -> bool:
        """Check if pattern matches at given offset."""
        for (px, py), pvalue in pattern.items():
            grid_x, grid_y = px + offset_x, py + offset_y
            if (grid_x, grid_y) not in self.data:
                return False
            if self.data[(grid_x, grid_y)] != pvalue:
                return False
        return True
    
    def flood_fill(self, start: Coordinate,
                   fill_value: CellValue,
                   target_value: Optional[CellValue] = None,
                   connectivity: int = 4) -> Set[Coordinate]:
        """
        Flood fill algorithm for region marking.
        
        Args:
            start: Starting coordinate
            fill_value: Value to fill with
            target_value: Value to replace (defaults to value at start)
            connectivity: 4 or 8 connected
            
        Returns:
            Set of coordinates that were filled
        """
        if start not in self.data:
            return set()
        
        if target_value is None:
            target_value = self.data[start]
        
        if target_value == fill_value:
            return set()
        
        filled = set()
        stack = [start]
        
        while stack:
            coord = stack.pop()
            if coord in filled or coord not in self.data:
                continue
            
            if self.data[coord] != target_value:
                continue
            
            # Fill this cell
            self.data[coord] = fill_value
            filled.add(coord)
            
            # Add neighbors to stack
            for neighbor in self.neighbors(coord, connectivity):
                if neighbor not in filled:
                    stack.append(neighbor)
        
        return filled
    
    def count_regions(self, value: CellValue, connectivity: int = 4) -> int:
        """Count connected regions of given value."""
        visited = set()
        regions = 0
        
        for coord, cell_value in self.data.items():
            if cell_value == value and coord not in visited:
                # Start new region
                regions += 1
                stack = [coord]
                
                while stack:
                    current = stack.pop()
                    if current in visited:
                        continue
                    
                    if current in self.data and self.data[current] == value:
                        visited.add(current)
                        
                        for neighbor in self.neighbors(current, connectivity):
                            if neighbor not in visited:
                                stack.append(neighbor)
        
        return regions
    
    def to_string(self, 
                  empty_char: str = '.',
                  value_map: Optional[Dict[CellValue, str]] = None) -> str:
        """
        Convert grid to string representation.
        
        Args:
            empty_char: Character for empty cells
            value_map: Mapping from cell values to display characters
        """
        if not self.data:
            return ""
        
        bounds = self.bounds
        lines = []
        
        for y in range(bounds.min_y, bounds.max_y + 1):
            line = ""
            for x in range(bounds.min_x, bounds.max_x + 1):
                if (x, y) in self.data:
                    value = self.data[(x, y)]
                    if value_map and value in value_map:
                        char = value_map[value]
                    else:
                        char = str(value)
                else:
                    char = empty_char
                line += char
            lines.append(line)
        
        return '\n'.join(lines)

# Utility functions for grid creation and manipulation

def parse_grid(input_data: str,
               value_map: Optional[Dict[str, Any]] = None,
               coordinate_system: str = "xy") -> Grid:
    """
    Parse grid from string input.
    
    Common pattern extracted from multiple AoC solutions.
    
    Args:
        input_data: Multi-line string representing grid
        value_map: Mapping from characters to cell values
        coordinate_system: "xy" or "rc" coordinate system
        
    Returns:
        Grid object
    """
    lines = input_data.strip().split('\n')
    grid_data = {}
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if coordinate_system == "xy":
                coord = (x, y)
            else:  # rc system
                coord = (y, x)
            
            value = value_map.get(char, char) if value_map else char
            grid_data[coord] = value
    
    return Grid(grid_data, coordinate_system=coordinate_system)

def neighbors_4(coord: Coordinate) -> List[Coordinate]:
    """Get 4-directional neighbors (utility function)."""
    x, y = coord
    return [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]

def neighbors_8(coord: Coordinate) -> List[Coordinate]:
    """Get 8-directional neighbors (utility function)."""
    x, y = coord
    return [
        (x-1, y-1), (x, y-1), (x+1, y-1),
        (x-1, y),             (x+1, y),
        (x-1, y+1), (x, y+1), (x+1, y+1)
    ]

def manhattan_distance(coord1: Coordinate, coord2: Coordinate) -> int:
    """Calculate Manhattan distance between coordinates."""
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def euclidean_distance(coord1: Coordinate, coord2: Coordinate) -> float:
    """Calculate Euclidean distance between coordinates."""
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

def bresenham_line(start: Coordinate, end: Coordinate) -> List[Coordinate]:
    """
    Generate coordinates along line using Bresenham's algorithm.
    
    Useful for line-of-sight and trajectory calculations.
    """
    x0, y0 = start
    x1, y1 = end
    
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    while True:
        points.append((x0, y0))
        
        if x0 == x1 and y0 == y1:
            break
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    
    return points

# Legacy compatibility aliases
def create_grid_from_lines(lines: List[str]) -> Dict[Coordinate, str]:
    """Legacy function for backward compatibility."""
    grid = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(x, y)] = char
    return grid