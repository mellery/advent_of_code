from collections import deque


def get_grid(filename):
    """Parse grid from file into a 2D list for faster access."""
    with open(filename) as f:
        lines = f.read().strip().split('\n')
    
    grid = []
    for line in lines:
        grid.append([int(c) for c in line])
    
    return grid


def get_low_points(grid):
    """Find all low points in the grid."""
    rows, cols = len(grid), len(grid[0])
    low_points = []
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for r in range(rows):
        for c in range(cols):
            height = grid[r][c]
            is_low = True
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if height >= grid[nr][nc]:
                        is_low = False
                        break
            
            if is_low:
                low_points.append((r, c))
    
    return low_points


def part1(filename):
    """Calculate sum of risk levels for all low points."""
    grid = get_grid(filename)
    low_points = get_low_points(grid)
    
    risk_sum = 0
    for r, c in low_points:
        risk_sum += grid[r][c] + 1
    
    return risk_sum


def find_basin_size(grid, start_r, start_c):
    """Find basin size using BFS flood fill from a low point."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = deque([(start_r, start_c)])
    visited.add((start_r, start_c))
    size = 0
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        r, c = queue.popleft()
        size += 1
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            
            # Skip if already visited
            if (nr, nc) in visited:
                continue
            
            # Skip if height is 9 (basin boundary)
            if grid[nr][nc] == 9:
                continue
            
            # Add to basin if height flows toward current point
            visited.add((nr, nc))
            queue.append((nr, nc))
    
    return size


def part2(filename):
    """Find product of three largest basin sizes."""
    grid = get_grid(filename)
    low_points = get_low_points(grid)
    
    basin_sizes = []
    for r, c in low_points:
        size = find_basin_size(grid, r, c)
        basin_sizes.append(size)
    
    # Sort and get top 3
    basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


def main():
    day = '9'
    
    # Test examples
    # print("Part 1 example:", part1(f"day{day}_ex1.txt"))
    print("Part 1:", part1(f"day{day}_input.txt"))
    
    # print("Part 2 example:", part2(f"day{day}_ex1.txt"))
    print("Part 2:", part2(f"day{day}_input.txt"))


if __name__ == "__main__":
    main()