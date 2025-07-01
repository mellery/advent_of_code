#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 12: Passage Pathing

Finding paths through a cave system with restrictions on revisiting small caves.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    get_lines, setup_day_args, find_input_file, validate_solution, run_solution
)
from typing import Any, Dict, List, Set
from collections import defaultdict


def build_graph(filename: str) -> Dict[str, List[str]]:
    """Build an adjacency list representation of the cave system."""
    graph = defaultdict(list)
    lines = get_lines(filename)
    
    for line in lines:
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


def part1(filename: str) -> Any:
    """
    Count paths from start to end, visiting small caves at most once.
    
    Args:
        filename: Path to the input file
        
    Returns:
        Number of valid paths
    """
    graph = build_graph(filename)
    visited = set()
    if 'start' in graph:
        visited.add('start')
    
    return count_paths_part1(graph, 'start', visited)


def part2(filename: str) -> Any:
    """
    Count paths allowing one small cave to be visited at most twice.
    
    Args:
        filename: Path to the input file
        
    Returns:
        Number of valid paths with relaxed rules
    """
    graph = build_graph(filename)
    visited = {'start': 1}
    
    return count_paths_part2(graph, 'start', visited, False)


def main():
    """Main function to run the solution."""
    day = '12'
    args = setup_day_args(day)
    
    # Determine input file
    if args.use_test:
        input_file = args.test
    else:
        input_file = find_input_file(day) or args.input
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        return
    
    print(f"Advent of Code 2021 - Day {day}")
    print(f"Using input file: {input_file}")
    print("-" * 40)
    
    # Run validation if test file exists
    test_file = args.test
    if os.path.exists(test_file) and not args.use_test:
        print("Running validation tests...")
        validate_solution(part1, part2, test_file, 
                        expected_part1=10, expected_part2=36)
        print("-" * 40)
    
    # Run the actual solution
    run_solution(part1, part2, input_file, args)


if __name__ == "__main__":
    main()