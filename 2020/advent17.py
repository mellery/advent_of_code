import copy 

#filename = "input17_ex1.txt"
filename = "input17.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

#room = []
world = {}

def get_active(world):
    active = 0
    
    for loc,v in world.items():
        if v == '#':
            active = active + 1
    
    return active


def expand_world(world):
    state = copy.deepcopy(world)
    for loc, v in world.items():
        x = loc[0]
        y = loc[1]
        z = loc[2]
        w = loc[3]
        for wi in [w-1,w,w+1]:
            for zi in [z-1,z,z+1]:
                for yi in [y-1,y,y+1]:
                    for xi in [x-1,x,x+1]:
                        if (xi,yi,zi,wi) not in state:
                            #print("adding",xi,yi,zi,wi)
                            state[(xi,yi,zi,wi)] = '.'
    world = copy.deepcopy(state)
    return world

def update_world(world):
    state = copy.deepcopy(world)
    changed = False

    for loc, v in world.items():
        cur = world[loc]
        adj = get_adj(world,loc)
        #print(loc,cur,"adj",adj)
        if cur == '#' and (adj == 2 or adj == 3):
            cur == '#'
        elif cur == '#':
            cur = '.'
            changed = True
        elif cur == '.' and adj == 3:
            cur = '#'
            changed = True
        state[loc] = cur
        
    world = copy.deepcopy(state)
    return world, changed

def print_world(world):
    #get levels
    hypers = []
    levels = []
    rows = []
    cols = []

    for loc in world:
        if loc[0] not in rows:
            rows.append(loc[0])
        if loc[1] not in cols:
            cols.append(loc[1])
        if loc[2] not in levels:
            levels.append(loc[2])
        if loc[3] not in hypers:
            hypers.append(loc[3])
    levels.sort()
    rows.sort()
    cols.sort()
    hypers.sort()

    print(hypers,levels,rows,cols)

    active = 0

    for w in hypers:
        
        for z in levels:
            print("\nz =",z,"w =",w)
            #for y in range(0,3):
            for y in cols:
                temp = ""
                #for x in range(0,3):
                for x in rows:
                    if (x,y,z,w) in world:
                        temp = temp + world[(x,y,z,w)]
                        if world[(x,y,z,w)] == '#':
                            active = active + 1
                print(temp)
    #print("active =",active)

def get_adj(world, loc):
    x = loc[0]
    y = loc[1]
    z = loc[2]
    w = loc[3]
        
    adj = 0
    for wi in [w-1,w,w+1]:
        for zi in [z-1,z,z+1]:
            for yi in [y-1,y,y+1]:
                for xi in [x-1,x,x+1]:
                    if (xi,yi,zi,wi) != (x,y,z,w):
                        if (xi,yi,zi,wi) in world and world[(xi,yi,zi,wi)] == '#':
                            adj = adj + 1
                       
    return adj

y = 0
for l in lines:
    z = 0
    temp = list(l.strip())
    print(list(temp))
    x = 0
    for t in temp:
        world[(x,y,z,0)] = t
        x = x + 1
    y = y + 1
    

print("initial_state")
print_world(world)

runs = 6

for cycles in range(0,runs):

    world = expand_world(world)
    world, changed = update_world(world)
    print("cycle:",cycles+1)
    #print_world(world)
    print("active =",get_active(world))

