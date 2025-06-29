"""
Advent of Code 2020 Day 7: Handy Haversacks
Clean, efficient solution using graph algorithms.
"""
import re
from collections import defaultdict, deque


def parse_input(filename: str) -> tuple[dict, dict]:
    """Parse bag rules into forward and reverse graphs."""
    contains = defaultdict(list)  # bag -> [(count, contained_bag), ...]
    contained_by = defaultdict(set)  # bag -> {containers}
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            # Parse "light red bags contain 1 bright white bag, 2 muted yellow bags."
            container = re.match(r'(\w+ \w+) bags contain', line).group(1)
            
            # Find all contained bags
            contained_matches = re.findall(r'(\d+) (\w+ \w+) bags?', line)
            
            for count_str, contained in contained_matches:
                count = int(count_str)
                contains[container].append((count, contained))
                contained_by[contained].add(container)
    
    return contains, contained_by


def count_containers(contained_by: dict, target: str) -> int:
    """Count how many bag colors can eventually contain the target bag."""
    visited = set()
    queue = deque([target])
    
    while queue:
        current = queue.popleft()
        for container in contained_by[current]:
            if container not in visited:
                visited.add(container)
                queue.append(container)
    
    return len(visited)


def count_contained_bags(contains: dict, bag: str) -> int:
    """Count total bags contained within the given bag (excluding the bag itself)."""
    total = 0
    
    for count, contained_bag in contains[bag]:
        # Add the bags directly contained
        total += count
        # Add the bags contained within those bags (recursive)
        total += count * count_contained_bags(contains, contained_bag)
    
    return total


def solve_day7(filename: str = "day7_input.txt") -> tuple[int, int]:
    """Solve both parts of day 7."""
    contains, contained_by = parse_input(filename)
    
    # Part 1: How many bag colors can eventually contain at least one shiny gold bag?
    part1 = count_containers(contained_by, "shiny gold")
    
    # Part 2: How many individual bags are required inside your single shiny gold bag?
    part2 = count_contained_bags(contains, "shiny gold")
    
    return part1, part2


if __name__ == "__main__":
    part1, part2 = solve_day7()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")