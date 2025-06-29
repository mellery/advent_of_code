import copy 

#filename = "day11_ex1.txt"
filename = "day11_input.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

room = []

def get_occupied(room):
    ocp = 0
    for x in range(0,rows):
        for y in range(0,cols):
            if room[x][y] == '#':
                ocp = ocp + 1
    return ocp


def update_room(room):
    state = copy.deepcopy(room)
    changed = False
    for x in range(0,rows):
        for y in range(0,cols):
            #adj = get_adj(room,x,y) #part 1
            adj = get_visible(room,x,y)
            cur = room[x][y]

            if cur == 'L' and adj == 0:
                state[x][y] = '#'
                changed = True

            #if cur == '#' and adj >= 4: #part 1
            if cur == '#' and adj >= 5: #part 2
                state[x][y] = 'L'
                changed = True

            #print(x*10+y,room[x][y],"has",adj,"adjacent and becomes",state[x][y])

    #update room to new state
    room = copy.deepcopy(state)
    return room, changed

def print_room(room):
    print("="*len(room[0]))
    for s in room:
        print("".join(s))

def get_visible(room, x, y):
    vis = 0
    
    cols = len(room[0])-1
    rows = len(room)-1

    #look up
    y2 = y
    while y2 > 0:
        y2 = y2-1
        if room[x][y2] == '#':
            vis = vis + 1
            break
        if room[x][y2] =='L':
            break

    #look up right
    y2 = y
    x2 = x
    while y2 > 0 and x2 < cols:
        y2 = y2-1
        x2 = x2+1
        if room[x2][y2] == '#':
            vis = vis + 1
            break
        if room[x2][y2] =='L':
            break

    #look right
    x2 = x
    while x2 < cols:
        x2 = x2+1
        if room[x2][y] == '#':
            vis = vis + 1
            break
        if room[x2][y] =='L':
            break

    #look right down
    y2 = y
    x2 = x
    while y2 < rows and x2 < cols:
        y2 = y2+1
        x2 = x2+1
        if room[x2][y2] == '#':
            vis = vis + 1
            break
        if room[x2][y2] =='L':
            break

    #look down
    y2 = y
    while y2 < rows:
        y2 = y2+1
        if room[x][y2] == '#':
            vis = vis + 1
            break
        if room[x][y2] =='L':
            break

    #look left down
    y2 = y
    x2 = x
    while y2 < rows and x2 > 0:
        y2 = y2+1
        x2 = x2-1
        if room[x2][y2] == '#':
            vis = vis + 1
            break
        if room[x2][y2] =='L':
            break

    #look left
    x2 = x
    while x2 > 0:
        x2 = x2-1
        if room[x2][y] == '#':
            vis = vis + 1
            break
        if room[x2][y] =='L':
            break

    #look up left
    y2 = y
    x2 = x
    while y2 > 0 and x2 > 0:
        y2 = y2-1
        x2 = x2-1
        if room[x2][y2] == '#':
            vis = vis + 1
            break
        if room[x2][y2] =='L':
            break

    return vis


def get_adj(room, x, y):
    cols = len(room[0])-1
    rows = len(room)-1
    adj = 0
    
    if (x > 0):
        if (room[x-1][y] == '#'):
            adj = adj + 1
    
    if (x < cols):
        if (room[x+1][y] == '#'):
            adj = adj + 1

    if (y > 0):
        if (room[x][y-1] == '#'):
            adj = adj + 1        

    if (y < rows):    
        if (room[x][y+1] == '#'):
            adj = adj + 1        

    if (x > 0) and (y > 0):
        if (room[x-1][y-1] == '#'):
            adj = adj + 1

    if (x > 0) and (y < rows):
        if (room[x-1][y+1] == '#'):
            adj = adj + 1

    if (x < cols) and (y > 0):
        if (room[x+1][y-1] == '#'):
            adj = adj + 1

    if (x < cols) and (y < rows):
        if (room[x+1][y+1] == '#'):
            adj = adj + 1

    return adj

for l in lines:
    temp = l.strip()
    #print(list(temp))
    room.append(list(temp))

cols = len(room[0])
rows = len(room)
print("room size",cols,rows)

changed = True
count = 0
while(changed == True):
    room, changed = update_room(room)
    count = count + 1
    print(count)

print_room(room)
print(get_occupied(room),"seats")
#print(0,0,room[0][0],"has",get_adj(room,x,y),"adj")
