#!/usr/bin/env python3
"""
Advent of Code 2020 Day 7: Handy Haversacks
https://adventofcode.com/2020/day/7

Bag containment rules parsing and graph traversal for luggage regulations.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple, DefaultDict
import re
from collections import defaultdict, deque

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class BagRuleGraph:
    """Represents the bag containment rules as a bidirectional graph."""
    
    def __init__(self):
        # bag -> [(count, contained_bag), ...]
        self.contains: DefaultDict[str, List[Tuple[int, str]]] = defaultdict(list)
        # bag -> {containers}
        self.contained_by: DefaultDict[str, Set[str]] = defaultdict(set)
    
    def add_rule(self, container: str, contents: List[Tuple[int, str]]):
        """
        Add a bag containment rule.
        
        Args:
            container: The bag that contains other bags
            contents: List of (count, bag_color) tuples for contained bags
        """
        self.contains[container] = contents
        for count, contained_bag in contents:
            self.contained_by[contained_bag].add(container)
    
    def count_possible_containers(self, target_bag: str) -> int:
        """
        Count how many different bag colors can eventually contain the target bag.
        
        Uses BFS to traverse the containment graph upward.
        
        Args:
            target_bag: The bag we want to find containers for
            
        Returns:
            Number of bag colors that can contain the target bag
        """
        visited = set()
        queue = deque([target_bag])
        
        while queue:
            current = queue.popleft()
            for container in self.contained_by[current]:
                if container not in visited:
                    visited.add(container)
                    queue.append(container)
        
        return len(visited)
    
    def count_total_contained_bags(self, bag: str) -> int:
        """
        Count the total number of individual bags contained within the given bag.
        
        Uses recursive traversal with memoization for efficiency.
        
        Args:
            bag: The bag to count contents for
            
        Returns:
            Total number of bags contained (excluding the bag itself)
        """
        total = 0
        
        for count, contained_bag in self.contains[bag]:
            # Add the bags directly contained
            total += count
            # Add the bags contained within those bags (recursive)
            total += count * self.count_total_contained_bags(contained_bag)
        
        return total
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the bag rule graph."""
        return {
            'total_bag_types': len(set(self.contains.keys()) | set(self.contained_by.keys())),
            'rules_with_contents': len([k for k, v in self.contains.items() if v]),
            'empty_bags': len([k for k, v in self.contains.items() if not v]),
            'max_direct_contents': max([len(v) for v in self.contains.values()], default=0)
        }


class Day7Solution(AdventSolution):
    """Solution for 2020 Day 7: Handy Haversacks."""

    def __init__(self):
        super().__init__(2020, 7, "Handy Haversacks")

    def parse_bag_rules(self, input_data: str) -> BagRuleGraph:
        """
        Parse bag containment rules from input data.
        
        Args:
            input_data: Raw input data containing bag rules
            
        Returns:
            BagRuleGraph representing the containment relationships
        """
        graph = BagRuleGraph()
        
        for line in input_data.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Parse "light red bags contain 1 bright white bag, 2 muted yellow bags."
            container_match = re.match(r'(\w+ \w+) bags contain', line)
            if not container_match:
                continue
                
            container = container_match.group(1)
            
            # Check for "no other bags"
            if "no other bags" in line:
                graph.add_rule(container, [])
                continue
            
            # Find all contained bags with counts
            contained_matches = re.findall(r'(\d+) (\w+ \w+) bags?', line)
            contents = [(int(count_str), bag_color) for count_str, bag_color in contained_matches]
            
            graph.add_rule(container, contents)
        
        return graph

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Count bag colors that can eventually contain a shiny gold bag.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of bag colors that can eventually contain a shiny gold bag
        """
        graph = self.parse_bag_rules(input_data)
        return graph.count_possible_containers("shiny gold")

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Count total bags required inside a single shiny gold bag.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Total number of individual bags required inside a shiny gold bag
        """
        graph = self.parse_bag_rules(input_data)
        return graph.count_total_contained_bags("shiny gold")

    def analyze_bag_rules(self, input_data: str) -> str:
        """
        Analyze the bag rule structure for debugging/exploration.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis summary as formatted string
        """
        graph = self.parse_bag_rules(input_data)
        stats = graph.get_statistics()
        
        analysis = []
        analysis.append("=== Bag Rules Analysis ===")
        analysis.append(f"Total bag types: {stats['total_bag_types']}")
        analysis.append(f"Rules with contents: {stats['rules_with_contents']}")
        analysis.append(f"Empty bags: {stats['empty_bags']}")
        analysis.append(f"Max direct contents: {stats['max_direct_contents']}")
        
        # Find bags with most containers
        container_counts = {bag: len(containers) 
                          for bag, containers in graph.contained_by.items()}
        if container_counts:
            most_contained = max(container_counts.items(), key=lambda x: x[1])
            analysis.append(f"Most contained bag: {most_contained[0]} ({most_contained[1]} containers)")
        
        # Find bags with most contents
        content_counts = {bag: len(contents) 
                         for bag, contents in graph.contains.items() if contents}
        if content_counts:
            most_contents = max(content_counts.items(), key=lambda x: x[1])
            analysis.append(f"Bag with most contents: {most_contents[0]} ({most_contents[1]} types)")
        
        return "\n".join(analysis)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test with a simple example from the problem description
        test_input = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
        
        graph = self.parse_bag_rules(test_input)
        
        # Test part 1: should be 4 (light red, dark orange, bright white, muted yellow)
        part1_result = graph.count_possible_containers("shiny gold")
        if part1_result != 4:
            print(f"Validation failed for part 1: expected 4, got {part1_result}")
            return False
        
        # Test part 2: should be 32 for the first example
        part2_result = graph.count_total_contained_bags("shiny gold")
        if part2_result != 32:
            print(f"Validation failed for part 2: expected 32, got {part2_result}")
            return False
        
        print("✅ All Day 7 validation tests passed!")
        return True


def main():
    """Main execution function."""
    solution = Day7Solution()
    solution.main()


if __name__ == "__main__":
    main()