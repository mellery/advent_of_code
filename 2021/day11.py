grid = {}
row = 0
col = 0
flashcount = 0

def load_map(filename):
    global row, col, grid

    with open(filename) as f:
        lines = f.readlines()
        for l in lines:
            temp = list(l.strip())
            col = 0
            for t in temp:
                grid[(row,col)] = int(t)
                col += 1
            row += 1

def flash(x,y):
    for coord in [(x-1,y),(x+1,y),(x,y-1),(x,y+1),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1)]:
        try:
            if grid[coord] <= 9:
                grid[coord] += 1
        except:
            pass
    

def step():
    global flashcount
    #increment by 1
    for x in range(0,row):
        for y in range(0,col):
            grid[(x,y)] += 1

    toflash = []

    for x in range(0,row):
        for y in range(0,col):
            if grid[(x,y)] == 10:
                toflash.append((x,y))
                flashcount += 1
                #flash(x,y)
    
    #for f in toflash:
    #    flash(f[0],f[1])

    flashed = []

    while len(toflash) > 0:
        for f in toflash:
            flash(f[0],f[1])    
            flashed.append(f)
        
        toflash = []
        for x in range(0,row):
            for y in range(0,col):
                if grid[(x,y)] == 10 and (x,y) not in flashed:
                    toflash.append((x,y))
                    flashcount += 1
        #print(toflash)

    for x in range(0,row):
        for y in range(0,col):
            if grid[(x,y)] > 9:
                grid[(x,y)] = 0

def print_map():
    global grid,row,col
    #print("-"*col)
    for x in range(0,row):
        line = ""
        for y in range(0,col):
            line += f"{str(grid[(x,y)])}"
        print(line)

def part1(filename, steps=100):
    global grid, row, col, flashcount
    grid = {}
    row = 0
    col = 0
    flashcount = 0
    
    load_map(filename)
    #print("Before any steps:")
    #print_map()

    for s in range(1,steps+1):
        step()
        #print(f"\nAfter step {s}:")
        #print_map()
    return flashcount        

def part2(filename):
    global grid, row, col, flashcount
    grid = {}
    row = 0
    col = 0
    flashcount = 0
    
    load_map(filename)
    steps = 0

    while(1):
        synced = True
        sync = grid[(0,0)]
        for x in range(0,row):
            for y in range(0,col):
                if grid[(x,y)] != sync:
                    synced = False
        step()
        steps += 1
        #print(steps)
        if synced == True:
            steps -= 1
            break
    return steps
    
    

#part1("day11_ex2.txt", 2)
#part1("day11_ex1.txt", 195)
#part1("day11_input.txt", 100)

#part2("day11_ex1.txt")
part2("day11_input.txt")