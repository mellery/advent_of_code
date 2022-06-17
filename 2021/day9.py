from functools import lru_cache

def get_grid(filename):
    grid = {}

    with open(filename) as f:
        lines = f.readlines()
        rows = len(lines)
        cols = len(lines[0])
        
        for r in range(0,rows):
            for c in range(0,cols-1):
                grid[(r,c)] = lines[r][c].strip()
        
    return grid,rows,cols-1

def get_low_points(grid,rows,cols):
    points = []
    for r in range(0,rows):

        for c in range(0,cols):
            point = grid[(r,c)]
            low = True
            if r > 0:
                if point >= grid[(r-1,c)]:
                    low = False
            if r < rows-1:
                if point >= grid[(r+1,c)]:
                    low = False         
            if c > 0:
                if point >= grid[(r,c-1)]:
                    low = False
            if c < cols-1:
                if point >= grid[(r,c+1)]:
                    low = False
                
            if low == True:
                #print(f"({r},{c}) : {point}")
                p = (r,c)
                points.append(p)
    return points

def part1(filename):
    grid,rows,cols = get_grid(filename)
    risk = 0
    points = get_low_points(grid,rows,cols)
    for p in points:
        risk += int(grid[p]) + 1   
    return(risk) 

#@lru_cache
def get_lower_point(grid,r,c):
    value = int(grid[r,c])

    k = (r-1,c)
    if k in grid:
        if int(grid[k]) < value:
            return r-1,c

    k = (r+1,c)
    if k in grid:
        if int(grid[k]) < value:
            return r+1,c
    
    k = (r,c-1)
    if k in grid:
        if int(grid[k]) < value:
            return r,c-1
    k = (r,c+1)
    if k in grid:
        if int(grid[k]) < value:
            return r,c+1


def find_drain(grid,r,c,points):
    if grid[(r,c)] == '9':
        return False
    if (r,c) in points:
        return (r,c)
    while (r,c) not in points:
        r,c = get_lower_point(grid,r,c)
    return (r,c)
    

def find_basin(grid,rows,cols,points,p):
    size = 0
    for r in range(0,rows):
        for c in range(0,cols):
            drain = (find_drain(grid,r,c,points))
            if drain == p:
                size += 1

    return size

def part2(filename):
    grid,rows,cols = get_grid(filename)
    risk = 0
    points = get_low_points(grid,rows,cols)
    sizes = []
    for p in points:
        size = find_basin(grid,rows,cols,points,p)    
        print(p,"basin",size)
        sizes.append(size)
    sizes.sort()
    sizes.reverse()
    return sizes[0]*sizes[1]*sizes[2]

def main():
    day = '9'
    #print(part1(f"day{day}_ex1.txt"))
    #print(part1(f"day{day}_input.txt"))

    #print(part2(f"day{day}_ex1.txt"))
    print(part2(f"day{day}_input.txt"))

if __name__ == "__main__":
    main()