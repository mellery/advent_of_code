"""
Advent of Code 2019 Day 10: Monitoring Station
Optimized solution using GCD and angle grouping.
"""
import math
from collections import defaultdict


def gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor."""
    while b:
        a, b = b, a % b
    return a


def get_direction_vector(dx: int, dy: int) -> tuple[int, int]:
    """Get normalized direction vector using GCD."""
    if dx == 0 and dy == 0:
        return (0, 0)
    g = gcd(abs(dx), abs(dy))
    return (dx // g, dy // g)


def get_angle(dx: int, dy: int) -> float:
    """Get angle in degrees, with 0° pointing up and increasing clockwise."""
    angle = math.atan2(dx, -dy) * 180 / math.pi
    return (angle + 360) % 360


def solve_day10(filename: str = "day10_input.txt") -> tuple[int, int]:
    """Solve both parts efficiently."""
    with open(filename, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]
    
    # Find all asteroid positions
    asteroids = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                asteroids.append((x, y))
    
    best_count = 0
    best_pos = None
    
    # Part 1: Find asteroid with most visible asteroids
    for ax, ay in asteroids:
        # Group asteroids by direction vector
        directions = set()
        
        for bx, by in asteroids:
            if (ax, ay) != (bx, by):
                dx, dy = bx - ax, by - ay
                direction = get_direction_vector(dx, dy)
                directions.add(direction)
        
        visible_count = len(directions)
        if visible_count > best_count:
            best_count = visible_count
            best_pos = (ax, ay)
    
    # Part 2: Simulate laser from best position
    station_x, station_y = best_pos
    
    # Group asteroids by angle and sort by distance
    angle_groups = defaultdict(list)
    
    for ax, ay in asteroids:
        if (ax, ay) != best_pos:
            dx, dy = ax - station_x, ay - station_y
            angle = get_angle(dx, dy)
            distance = dx * dx + dy * dy  # No need for sqrt, just for comparison
            angle_groups[angle].append((distance, ax, ay))
    
    # Sort each angle group by distance (closest first)
    for angle in angle_groups:
        angle_groups[angle].sort()
    
    # Get sorted angles (clockwise from north)
    sorted_angles = sorted(angle_groups.keys())
    
    # Simulate laser rotation
    destroyed = []
    angle_idx = 0
    
    while angle_groups:
        # Get current angle
        if angle_idx >= len(sorted_angles):
            angle_idx = 0
            # Remove empty angles
            sorted_angles = [a for a in sorted_angles if angle_groups[a]]
            if not sorted_angles:
                break
        
        current_angle = sorted_angles[angle_idx]
        
        if angle_groups[current_angle]:
            # Destroy closest asteroid at this angle
            _, x, y = angle_groups[current_angle].pop(0)
            destroyed.append((x, y))
        
        angle_idx += 1
    
    # Get 200th destroyed asteroid
    if len(destroyed) >= 200:
        x200, y200 = destroyed[199]  # 0-indexed
        part2_answer = x200 * 100 + y200
    else:
        part2_answer = 0
    
    return best_count, part2_answer


if __name__ == "__main__":
    part1, part2 = solve_day10()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")