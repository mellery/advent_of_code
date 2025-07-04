#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 12: Passage Pathing

Finding paths through a cave system with restrictions on revisiting small caves.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import Any, Dict, List, Set
from collections import defaultdict


def build_graph_from_data(input_data: str) -> Dict[str, List[str]]:
    """Build an adjacency list representation of the cave system."""
    graph = defaultdict(list)
    lines = input_data.strip().split('\n')
    
    for line in lines:
        if line.strip():
            cave1, cave2 = line.strip().split('-')
            graph[cave1].append(cave2)
            graph[cave2].append(cave1)
    
    return graph


def count_paths_part1(graph: Dict[str, List[str]], current: str, visited: Set[str]) -> int:
    """Count paths from current to 'end' without revisiting small caves."""
    if current == 'end':
        return 1
    
    total_paths = 0
    for neighbor in graph[current]:
        if neighbor == 'start':
            continue
        
        # Small caves (lowercase) can only be visited once
        if neighbor.islower() and neighbor in visited:
            continue
        
        new_visited = visited.copy()
        if neighbor.islower():
            new_visited.add(neighbor)
        
        total_paths += count_paths_part1(graph, neighbor, new_visited)
    
    return total_paths


def count_paths_part2(graph: Dict[str, List[str]], current: str, visited: Dict[str, int], used_twice: bool) -> int:
    """Count paths allowing one small cave to be visited twice."""
    if current == 'end':
        return 1
    
    total_paths = 0
    for neighbor in graph[current]:
        if neighbor == 'start':
            continue
        
        new_visited = visited.copy()
        new_used_twice = used_twice
        
        if neighbor.islower():
            if neighbor in visited:
                if used_twice:  # Already used our "twice" visit
                    continue
                new_used_twice = True
                new_visited[neighbor] = 2
            else:
                new_visited[neighbor] = 1
        
        total_paths += count_paths_part2(graph, neighbor, new_visited, new_used_twice)
    
    return total_paths


class Day12Solution(AdventSolution):
    """Day 12: Passage Pathing"""
    
    def __init__(self):
        super().__init__(2021, 12, "Passage Pathing")
    
    def part1(self, input_data: str) -> Any:
        """
        Count paths from start to end, visiting small caves at most once.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Number of valid paths
        """
        graph = build_graph_from_data(input_data)
        visited = set()
        if 'start' in graph:
            visited.add('start')
        
        return count_paths_part1(graph, 'start', visited)
    
    def part2(self, input_data: str) -> Any:
        """
        Count paths allowing one small cave to be visited at most twice.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Number of valid paths with relaxed rules
        """
        graph = build_graph_from_data(input_data)
        visited = {'start': 1}
        
        return count_paths_part2(graph, 'start', visited, False)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
        expected_part1 = 226
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        expected_part2 = 3509
        
        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False
        
        print("✅ All Day 12 validation tests passed!")
        return True
    

def main():
    """Main execution function."""
    solution = Day12Solution()
    solution.main()


if __name__ == "__main__":
    main()