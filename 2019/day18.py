import heapq
from collections import deque
from functools import lru_cache
import sys
from typing import Dict, Set, Tuple, FrozenSet
import time


def parse_maze(input_file):
    """Parse maze from input file and return grid, start positions, keys, and doors."""
    with open(input_file, 'r') as f:
        grid = [list(line.strip()) for line in f]
    
    starts = []
    keys = {}
    doors = {}
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            cell = grid[y][x]
            if cell == '@':
                starts.append((y, x))
            elif cell.isalpha():
                if cell.islower():
                    keys[cell] = (y, x)
                else:
                    doors[cell] = (y, x)
    
    return grid, starts, keys, doors


def bfs_distances(grid, start):
    """BFS to find distances from start to all reachable positions."""
    distances = {}
    queue = deque([(start, 0)])
    visited = {start}
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        (y, x), dist = queue.popleft()
        distances[(y, x)] = dist
        
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if (0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and 
                (ny, nx) not in visited and grid[ny][nx] != '#'):
                visited.add((ny, nx))
                queue.append(((ny, nx), dist + 1))
    
    return distances


def build_key_graph(grid, starts, keys, doors):
    """Build a graph of distances between important positions (starts, keys)."""
    important_positions = {'@' + str(i): pos for i, pos in enumerate(starts)}
    important_positions.update(keys)
    
    graph = {}
    
    for name, pos in important_positions.items():
        distances = bfs_distances(grid, pos)
        graph[name] = {}
        
        for other_name, other_pos in important_positions.items():
            if other_name != name and other_pos in distances:
                # Check if path is blocked by doors
                path_doors = set()
                queue = deque([pos])
                visited = {pos}
                parent = {pos: None}
                
                # BFS to find path and collect doors along the way
                found_target = False
                while queue and not found_target:
                    curr = queue.popleft()
                    if curr == other_pos:
                        found_target = True
                        break
                    
                    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        ny, nx = curr[0] + dy, curr[1] + dx
                        if (0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and 
                            (ny, nx) not in visited and grid[ny][nx] != '#'):
                            visited.add((ny, nx))
                            parent[(ny, nx)] = curr
                            queue.append((ny, nx))
                
                # Reconstruct path and find doors
                if found_target:
                    path = []
                    curr = other_pos
                    while curr is not None:
                        path.append(curr)
                        curr = parent.get(curr)
                    path.reverse()
                    
                    for py, px in path:
                        if grid[py][px].isupper():
                            path_doors.add(grid[py][px].lower())
                
                if found_target:
                    graph[name][other_name] = (distances[other_pos], frozenset(path_doors))
    
    return graph


def solve_part1(input_file):
    """Solve part 1 using A* search with heuristics."""
    grid, starts, keys, doors = parse_maze(input_file)
    graph = build_key_graph(grid, starts, keys, doors)
    
    all_keys = frozenset(keys.keys())
    start_pos = '@0'
    
    # Precompute minimum distances between all keys for heuristic
    min_distances = {}
    for key1 in all_keys:
        min_distances[key1] = {}
        for key2 in all_keys:
            if key1 != key2 and key2 in graph[key1]:
                dist, _ = graph[key1][key2]
                min_distances[key1][key2] = dist
            else:
                min_distances[key1][key2] = float('inf')
    
    def heuristic(pos, collected_keys):
        """Estimate minimum cost to collect all remaining keys."""
        remaining = all_keys - collected_keys
        if not remaining:
            return 0
        
        # Find minimum spanning tree of remaining keys
        if len(remaining) == 1:
            key = next(iter(remaining))
            if key in graph[pos]:
                dist, req_keys = graph[pos][key]
                return dist if req_keys.issubset(collected_keys) else float('inf')
            return float('inf')
        
        # Simple heuristic: sum of minimum distances to each remaining key
        total = 0
        for key in remaining:
            min_dist = float('inf')
            if key in graph[pos]:
                dist, req_keys = graph[pos][key]
                if req_keys.issubset(collected_keys):
                    min_dist = min(min_dist, dist)
            for other_key in collected_keys:
                if other_key in min_distances and key in min_distances[other_key]:
                    min_dist = min(min_dist, min_distances[other_key][key])
            total += min_dist if min_dist < float('inf') else 0
        
        return total // 2  # Divide by 2 as heuristic overestimates
    
    # Convert to bit masks for faster operations
    key_to_bit = {key: 1 << i for i, key in enumerate(sorted(all_keys))}
    all_keys_mask = (1 << len(all_keys)) - 1
    
    # Convert required keys to bit masks
    graph_bits = {}
    for pos in graph:
        graph_bits[pos] = {}
        for key in graph[pos]:
            dist, req_keys = graph[pos][key]
            req_mask = 0
            for req_key in req_keys:
                if req_key in key_to_bit:
                    req_mask |= key_to_bit[req_key]
            graph_bits[pos][key] = (dist, req_mask)
    
    # A* search with bit operations
    heap = [(0, 0, start_pos, 0)]
    best_distance = {}
    
    while heap:
        f_score, g_score, pos, keys_mask = heapq.heappop(heap)
        
        state = (pos, keys_mask)
        if state in best_distance and best_distance[state] <= g_score:
            continue
        best_distance[state] = g_score
        
        if keys_mask == all_keys_mask:
            return g_score
        
        for key in all_keys:
            key_bit = key_to_bit[key]
            if not (keys_mask & key_bit) and key in graph_bits[pos]:  # Key not collected
                dist, req_mask = graph_bits[pos][key]
                if (keys_mask & req_mask) == req_mask:  # All required keys collected
                    new_g = g_score + dist
                    new_keys_mask = keys_mask | key_bit
                    new_state = (key, new_keys_mask)
                    
                    if new_state not in best_distance or best_distance[new_state] > new_g:
                        h_score = heuristic(key, frozenset(k for k, b in key_to_bit.items() if new_keys_mask & b))
                        f_score = new_g + h_score
                        heapq.heappush(heap, (f_score, new_g, key, new_keys_mask))
    
    return float('inf')


def solve_part2(input_file):
    """Solve part 2 with multiple robots using A* search."""
    grid, starts, keys, doors = parse_maze(input_file)
    graph = build_key_graph(grid, starts, keys, doors)
    
    all_keys = frozenset(keys.keys())
    start_positions = tuple(f'@{i}' for i in range(len(starts)))
    
    def heuristic(positions, collected_keys):
        """Estimate minimum cost for multiple robots."""
        remaining = all_keys - collected_keys
        if not remaining:
            return 0
        
        # For each remaining key, find the minimum distance from any robot
        total = 0
        for key in remaining:
            min_dist = float('inf')
            for pos in positions:
                if key in graph[pos]:
                    dist, req_keys = graph[pos][key]
                    if req_keys.issubset(collected_keys):
                        min_dist = min(min_dist, dist)
            total += min_dist if min_dist < float('inf') else 0
        
        return total // 2
    
    # Convert to bit masks for faster operations
    key_to_bit = {key: 1 << i for i, key in enumerate(sorted(all_keys))}
    all_keys_mask = (1 << len(all_keys)) - 1
    
    # Convert required keys to bit masks
    graph_bits = {}
    for pos in graph:
        graph_bits[pos] = {}
        for key in graph[pos]:
            dist, req_keys = graph[pos][key]
            req_mask = 0
            for req_key in req_keys:
                if req_key in key_to_bit:
                    req_mask |= key_to_bit[req_key]
            graph_bits[pos][key] = (dist, req_mask)
    
    # A* search with bit operations
    heap = [(0, 0, start_positions, 0)]
    best_distance = {}
    
    while heap:
        f_score, g_score, positions, keys_mask = heapq.heappop(heap)
        
        state = (positions, keys_mask)
        if state in best_distance and best_distance[state] <= g_score:
            continue
        best_distance[state] = g_score
        
        if keys_mask == all_keys_mask:
            return g_score
        
        for key in all_keys:
            key_bit = key_to_bit[key]
            if not (keys_mask & key_bit):  # Key not collected
                for i, pos in enumerate(positions):
                    if key in graph_bits[pos]:
                        dist, req_mask = graph_bits[pos][key]
                        if (keys_mask & req_mask) == req_mask:  # All required keys collected
                            new_g = g_score + dist
                            new_positions = tuple(key if j == i else positions[j] 
                                                for j in range(len(positions)))
                            new_keys_mask = keys_mask | key_bit
                            new_state = (new_positions, new_keys_mask)
                            
                            if new_state not in best_distance or best_distance[new_state] > new_g:
                                collected_set = frozenset(k for k, b in key_to_bit.items() if new_keys_mask & b)
                                h_score = heuristic(new_positions, collected_set)
                                f_score = new_g + h_score
                                heapq.heappush(heap, (f_score, new_g, new_positions, new_keys_mask))
    
    return float('inf')


def day18p1(input_file):
    """Part 1 entry point with timing."""
    print(f"Solving part 1 for {input_file}...")
    start_time = time.time()
    result = solve_part1(input_file)
    elapsed = time.time() - start_time
    print(f"Part 1: {result} (solved in {elapsed:.2f}s)")
    return result


def day18p2(input_file):
    """Part 2 entry point with timing."""
    print(f"Solving part 2 for {input_file}...")
    start_time = time.time()
    result = solve_part2(input_file)
    elapsed = time.time() - start_time
    print(f"Part 2: {result} (solved in {elapsed:.2f}s)")
    return result


if __name__ == "__main__":

    try:
        day18p1("day18_input.txt")
        day18p2("day18_input2.txt")
    except FileNotFoundError as e:
        print(f"Input file not found: {e}")