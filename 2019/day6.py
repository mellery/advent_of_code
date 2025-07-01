#!/usr/bin/env python3
"""
Advent of Code 2019 - Day 6: Universal Orbit Map

Before you leave, the Elves in accounting just need you to fix your orbit map.
You need to count the total number of direct and indirect orbits in the map.

Key Concepts:
- Tree traversal and path finding
- Orbital mechanics (parent-child relationships)
- Graph analysis and shortest paths
- Ancestor finding and path intersection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque


@dataclass
class CelestialBody:
    """Represents a celestial body in the orbit map."""
    name: str
    parent: Optional['CelestialBody'] = None
    children: Set['CelestialBody'] = field(default_factory=set)
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if isinstance(other, CelestialBody):
            return self.name == other.name
        return False
    
    def __repr__(self):
        return f"CelestialBody({self.name})"
    
    def add_child(self, child: 'CelestialBody') -> None:
        """Add a child body that orbits this one."""
        self.children.add(child)
        child.parent = self
    
    def get_orbit_count(self) -> int:
        """Get the number of direct and indirect orbits for this body."""
        if self.parent is None:
            return 0
        return 1 + self.parent.get_orbit_count()
    
    def get_path_to_root(self) -> List['CelestialBody']:
        """Get the path from this body to the root (center of mass)."""
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path
    
    def get_ancestors(self) -> List['CelestialBody']:
        """Get all ancestors (bodies this one orbits, directly or indirectly)."""
        ancestors = []
        current = self.parent
        while current is not None:
            ancestors.append(current)
            current = current.parent
        return ancestors
    
    def find_common_ancestor(self, other: 'CelestialBody') -> Optional['CelestialBody']:
        """Find the closest common ancestor with another body."""
        self_ancestors = set(self.get_ancestors())
        other_path = other.get_path_to_root()
        
        for body in other_path:
            if body in self_ancestors:
                return body
        
        return None


class OrbitMap:
    """Represents the complete universal orbit map."""
    
    def __init__(self):
        """Initialize empty orbit map."""
        self.bodies: Dict[str, CelestialBody] = {}
        self.root: Optional[CelestialBody] = None
    
    def add_orbit_relationship(self, center: str, orbiter: str) -> None:
        """
        Add an orbit relationship (orbiter orbits center).
        
        Args:
            center: Name of the body being orbited
            orbiter: Name of the body doing the orbiting
        """
        # Create bodies if they don't exist
        if center not in self.bodies:
            self.bodies[center] = CelestialBody(center)
        if orbiter not in self.bodies:
            self.bodies[orbiter] = CelestialBody(orbiter)
        
        center_body = self.bodies[center]
        orbiter_body = self.bodies[orbiter]
        
        center_body.add_child(orbiter_body)
    
    def find_root(self) -> Optional[CelestialBody]:
        """Find the root body (center of mass) - the one with no parent."""
        if self.root is not None:
            return self.root
        
        for body in self.bodies.values():
            if body.parent is None:
                self.root = body
                return body
        
        return None
    
    def get_total_orbits(self) -> int:
        """Calculate the total number of direct and indirect orbits."""
        total = 0
        for body in self.bodies.values():
            total += body.get_orbit_count()
        return total
    
    def calculate_orbital_transfers(self, start: str, end: str) -> int:
        """
        Calculate minimum orbital transfers needed to get from start to end.
        
        Args:
            start: Starting body name
            end: Destination body name
            
        Returns:
            Minimum number of orbital transfers needed
        """
        if start not in self.bodies or end not in self.bodies:
            return -1
        
        start_body = self.bodies[start]
        end_body = self.bodies[end]
        
        # Find common ancestor
        common_ancestor = start_body.find_common_ancestor(end_body)
        if common_ancestor is None:
            return -1
        
        # Calculate transfers: from start to common ancestor + from common ancestor to end
        # We need to go to the parent of start/end, not the bodies themselves
        start_parent = start_body.parent
        end_parent = end_body.parent
        
        if start_parent is None or end_parent is None:
            return -1
        
        # Distance from start's parent to common ancestor
        start_distance = 0
        current = start_parent
        while current != common_ancestor:
            start_distance += 1
            current = current.parent
            if current is None:
                return -1
        
        # Distance from end's parent to common ancestor
        end_distance = 0
        current = end_parent
        while current != common_ancestor:
            end_distance += 1
            current = current.parent
            if current is None:
                return -1
        
        return start_distance + end_distance
    
    def analyze_structure(self) -> Dict:
        """
        Analyze the orbital structure and provide statistics.
        
        Returns:
            Dictionary with orbital map statistics
        """
        root = self.find_root()
        
        # Calculate depth statistics
        depths = []
        max_depth = 0
        bodies_by_depth = defaultdict(list)
        
        for body in self.bodies.values():
            depth = body.get_orbit_count()
            depths.append(depth)
            max_depth = max(max_depth, depth)
            bodies_by_depth[depth].append(body.name)
        
        # Find bodies with most children
        max_children = 0
        bodies_with_most_children = []
        
        for body in self.bodies.values():
            child_count = len(body.children)
            if child_count > max_children:
                max_children = child_count
                bodies_with_most_children = [body.name]
            elif child_count == max_children and child_count > 0:
                bodies_with_most_children.append(body.name)
        
        analysis = {
            'total_bodies': len(self.bodies),
            'root_body': root.name if root else None,
            'max_depth': max_depth,
            'average_depth': sum(depths) / len(depths) if depths else 0,
            'bodies_by_depth': dict(bodies_by_depth),
            'max_children_count': max_children,
            'bodies_with_most_children': bodies_with_most_children,
            'total_orbits': self.get_total_orbits()
        }
        
        return analysis


class OrbitMapBuilder:
    """Builds orbit maps from various input formats."""
    
    @staticmethod
    def from_orbit_specifications(orbit_specs: List[str]) -> OrbitMap:
        """
        Build orbit map from orbit specifications.
        
        Args:
            orbit_specs: List of orbit relationships like "COM)B"
            
        Returns:
            Complete orbit map
        """
        orbit_map = OrbitMap()
        
        for spec in orbit_specs:
            if ')' in spec:
                center, orbiter = spec.strip().split(')')
                orbit_map.add_orbit_relationship(center, orbiter)
        
        return orbit_map
    
    @staticmethod
    def from_input_data(input_data: str) -> OrbitMap:
        """
        Build orbit map from input data string.
        
        Args:
            input_data: Multi-line string with orbit specifications
            
        Returns:
            Complete orbit map
        """
        lines = input_data.strip().split('\n')
        return OrbitMapBuilder.from_orbit_specifications(lines)


class OrbitPathFinder:
    """Finds optimal paths through the orbital system."""
    
    def __init__(self, orbit_map: OrbitMap):
        """Initialize with an orbit map."""
        self.orbit_map = orbit_map
    
    def find_shortest_path(self, start: str, end: str) -> Optional[List[str]]:
        """
        Find the shortest path between two bodies.
        
        Args:
            start: Starting body name
            end: Destination body name
            
        Returns:
            List of body names representing the shortest path, or None if no path exists
        """
        if start not in self.orbit_map.bodies or end not in self.orbit_map.bodies:
            return None
        
        # Use BFS to find shortest path
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if current == end:
                return path
            
            current_body = self.orbit_map.bodies[current]
            
            # Add neighbors (parent and children)
            neighbors = []
            if current_body.parent:
                neighbors.append(current_body.parent.name)
            neighbors.extend(child.name for child in current_body.children)
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def analyze_path(self, start: str, end: str) -> Dict:
        """
        Analyze the path between two bodies.
        
        Args:
            start: Starting body name
            end: Destination body name
            
        Returns:
            Dictionary with path analysis
        """
        path = self.find_shortest_path(start, end)
        if path is None:
            return {'path_found': False}
        
        # Calculate orbital transfers (excluding start and end points)
        transfers = len(path) - 2 if len(path) > 2 else 0
        
        analysis = {
            'path_found': True,
            'path': path,
            'path_length': len(path),
            'orbital_transfers': transfers,
            'bodies_traversed': len(path) - 2  # Excluding start and end
        }
        
        return analysis


class Day6Solution(AdventSolution):
    """Enhanced solution for Day 6: Universal Orbit Map."""
    
    def __init__(self):
        super().__init__(year=2019, day=6, title="Universal Orbit Map")
    
    def part1(self, input_data: str) -> int:
        """
        Calculate the total number of direct and indirect orbits.
        
        Args:
            input_data: Multi-line string with orbit specifications
            
        Returns:
            Total number of orbits in the system
        """
        orbit_map = OrbitMapBuilder.from_input_data(input_data)
        return orbit_map.get_total_orbits()
    
    def part2(self, input_data: str) -> int:
        """
        Calculate minimum orbital transfers from YOU to SAN.
        
        Args:
            input_data: Multi-line string with orbit specifications
            
        Returns:
            Minimum number of orbital transfers needed
        """
        orbit_map = OrbitMapBuilder.from_input_data(input_data)
        return orbit_map.calculate_orbital_transfers("YOU", "SAN")
    
    def analyze_orbit_system(self, input_data: str) -> None:
        """
        Provide comprehensive analysis of the orbital system.
        
        Args:
            input_data: Multi-line string with orbit specifications
        """
        orbit_map = OrbitMapBuilder.from_input_data(input_data)
        path_finder = OrbitPathFinder(orbit_map)
        
        # Basic analysis
        analysis = orbit_map.analyze_structure()
        
        print("=== Universal Orbit Map Analysis ===")
        print(f"Total celestial bodies: {analysis['total_bodies']}")
        print(f"Center of mass: {analysis['root_body']}")
        print(f"Maximum orbital depth: {analysis['max_depth']}")
        print(f"Average orbital depth: {analysis['average_depth']:.2f}")
        print(f"Total orbits: {analysis['total_orbits']}")
        
        # Depth distribution
        print(f"\nBodies by orbital depth:")
        for depth in sorted(analysis['bodies_by_depth'].keys()):
            bodies = analysis['bodies_by_depth'][depth]
            print(f"  Depth {depth}: {len(bodies)} bodies")
            if len(bodies) <= 10:  # Show details for small groups
                print(f"    {', '.join(bodies)}")
        
        # Bodies with most satellites
        print(f"\nBodies with most satellites:")
        print(f"  Maximum satellites: {analysis['max_children_count']}")
        if analysis['bodies_with_most_children']:
            print(f"  Bodies: {', '.join(analysis['bodies_with_most_children'])}")
        
        # YOU and SAN analysis
        if "YOU" in orbit_map.bodies and "SAN" in orbit_map.bodies:
            you_analysis = path_finder.analyze_path("YOU", "SAN")
            transfers = orbit_map.calculate_orbital_transfers("YOU", "SAN")
            
            print(f"\n=== YOU to SAN Transfer Analysis ===")
            print(f"Minimum orbital transfers: {transfers}")
            
            if you_analysis['path_found']:
                print(f"Path length: {you_analysis['path_length']} bodies")
                print(f"Bodies traversed: {you_analysis['bodies_traversed']}")
                print(f"Transfer path: {' -> '.join(you_analysis['path'])}")
            
            # Show YOU and SAN details
            you_body = orbit_map.bodies["YOU"]
            san_body = orbit_map.bodies["SAN"]
            
            print(f"\nYOU orbital details:")
            print(f"  Orbits: {you_body.parent.name if you_body.parent else 'None'}")
            print(f"  Orbital depth: {you_body.get_orbit_count()}")
            
            print(f"\nSAN orbital details:")
            print(f"  Orbits: {san_body.parent.name if san_body.parent else 'None'}")
            print(f"  Orbital depth: {san_body.get_orbit_count()}")
            
            # Find common ancestor
            common = you_body.find_common_ancestor(san_body)
            if common:
                print(f"\nCommon ancestor: {common.name}")
        
        # Part 1 and Part 2 results
        print(f"\n=== Final Results ===")
        print(f"Part 1 - Total orbits: {self.part1(input_data)}")
        print(f"Part 2 - Orbital transfers: {self.part2(input_data)}")


def main():
    """Main execution function."""
    solution = Day6Solution()
    
    # If run with analyze flag, show comprehensive analysis
    if len(sys.argv) > 1 and sys.argv[1] == 'analyze':
        input_data = solution._load_input()
        solution.analyze_orbit_system(input_data)
    else:
        solution.main()


if __name__ == "__main__":
    main()