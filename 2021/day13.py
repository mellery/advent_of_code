def load_paper(filename):
    grid = {}
    rows = 0
    cols = 0

    with open(filename) as f:
        lines = f.readlines()
        folds = []
        for l in lines:
            if l == "\n":
                break
            temp = l.strip()
            #print(temp)
            x = int(temp.split(',')[0].strip())
            y = int(temp.split(',')[1].strip())
            grid[(x,y)] = '#'
            if y > rows:
                rows = y
            if x > cols:
                cols = x
        for l in lines:
            if l.startswith("fold"):
                folds.append(l.strip())
            
    return grid,rows+1,cols+1, folds

def print_paper(grid,rows,cols):
    #print(rows,cols)
    count = 0
    for y in range(0,rows):
        line = ""
        for x in range(0,cols):
            if (x,y) in grid:
                if grid[(x,y)] == '#':
                    count += 1
                line += grid[(x,y)]
            else:
                grid[(x,y)] = '.'
                line += '.'
        print(line)
    print(count)
    print('\n')

def fold(grid,rows,cols,f):
    f = f.replace("fold along ","")
    
    dir = f.split('=')[0]
    loc = int(f.split('=')[1])
    #print(dir,loc)
    if dir == 'y':
        for x in range(0,cols):
            grid[(x,loc)] = '-'
    
        for y in range(loc+1,rows):
            for x in range(0,cols):
                val = grid[x,(loc-(y-loc))]
                if val == '.':
                    grid[x,(loc-(y-loc))] = grid[(x,y)]
        rows = loc

    if dir == 'x':
        for y in range(0,rows):
            grid[(loc,y)] = '|'
    
        for x in range(loc+1,cols):
            for y in range(0,rows):
                val = grid[(loc-(x-loc),y)]
                if val == '.':
                    grid[(loc-(x-loc),y)] = grid[(x,y)]
        cols = loc

    return grid, rows, cols
    

def part1(filename):
    grid, rows, cols, folds = load_paper(filename)
    print_paper(grid,rows,cols)
    
    for f in folds:
        print(f)
        grid, rows, cols = fold(grid,rows,cols,f)
    print_paper(grid,rows,cols)

    #grid, rows, cols = fold(grid,rows,cols,folds[1])
    #print_paper(grid,rows,cols)

#part1('day13_ex1.txt')
part1('day13_input.txt')