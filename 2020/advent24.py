import numpy as np
import matplotlib.pyplot as plt

import copy
#1 = black
#0 = white (default)

filename = "day24_input.txt"
#filename = "day24_ex1.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 


directions = ['e', 'se', 'sw', 'w', 'nw', 'ne']
floor_map = {}

def expand_floor(floor_map):
    new_floor = copy.deepcopy(floor_map)
    for k,v in floor_map.items():
        
        cur_x = k[0]
        cur_y = k[1]

        if (cur_x+1,cur_y) not in floor_map:
            new_floor[(cur_x+1,cur_y)] = 0
        
        if (cur_x+0.5,cur_y+1) not in floor_map:
            new_floor[(cur_x+0.5,cur_y+1)] = 0

        if (cur_x-0.5,cur_y+1) not in floor_map:
            new_floor[(cur_x-0.5,cur_y+1)] = 0
        
        if (cur_x-1,cur_y) not in floor_map:
            new_floor[(cur_x-1,cur_y)] = 0
        
        if (cur_x-0.5,cur_y-1) not in floor_map:
            new_floor[(cur_x-0.5,cur_y-1)] = 0
        
        if (cur_x+0.5,cur_y-1) not in floor_map:
            new_floor[(cur_x+0.5,cur_y-1)] = 0

    return new_floor


def get_adj_black(pos):
    black = 0

    cur_x = pos[0]
    cur_y = pos[1]

    if (cur_x+1,cur_y) in floor_map and floor_map[(cur_x+1,cur_y)] == 1:
        black += 1

    if (cur_x+0.5,cur_y+1) in floor_map and floor_map[(cur_x+0.5,cur_y+1)] == 1:
        black += 1

    if (cur_x-0.5,cur_y+1) in floor_map and floor_map[(cur_x-0.5,cur_y+1)] == 1:
        black += 1
    
    if (cur_x-1,cur_y) in floor_map and floor_map[(cur_x-1,cur_y)] == 1:
        black += 1
        
    if (cur_x-0.5,cur_y-1) in floor_map and floor_map[(cur_x-0.5,cur_y-1)] == 1:
        black += 1

    if (cur_x+0.5,cur_y-1) in floor_map and floor_map[(cur_x+0.5,cur_y-1)] == 1:
        black += 1

    return black

def split_instructions(line):
    instructions = []
    while len(line) > 0:
        for d in directions:
            if line.startswith(d):
                instructions.append(d)
                line = line.replace(d,'',1)
    
    return instructions

def get_last_tile(path):
    cur_x = 0
    cur_y = 0
    #print("start at",(cur_x,cur_y))
    for p in path:
        if p == 'e':
            cur_x += 1

        elif p == 'se':
            cur_y += 1
            cur_x += 0.5
            
        elif p == 'sw':
            cur_y += 1
            cur_x -= 0.5
            
        elif p == 'w':
            cur_x -= 1

        elif p == 'nw':
            cur_y -= 1
            cur_x -= 0.5
            
        elif p == 'ne':
            cur_y -= 1
            cur_x += 0.5

        #print("now at",(cur_x,cur_y))
    #print("end at",(cur_x,cur_y))
    return (cur_x,cur_y)

#path = split_instructions('esenee')
#print(path)

for l in lines:
    path = split_instructions(l.strip())
    tile = get_last_tile(path)
    if tile not in floor_map:
        floor_map[tile] = 1 #
    else:
        #print("existing tile")
        if floor_map[tile] == 0:
            floor_map[tile] = 1
        else:
            floor_map[tile] = 0

    #print("now at",tile)

#part 1
#black = 0
#white = 0
#for k,v in floor_map.items():
    #print(k,v)
#    if v == 1:
#        black += 1
#    else:
#        white += 1

def update_day(floor_map,day):

    floor_map = expand_floor(floor_map)
    new_floor = copy.deepcopy(floor_map)

    for k,v in floor_map.items():
        adj_black = get_adj_black(k)
        if v == 1: #black
            if adj_black == 0 or adj_black > 2:
                new_floor[k] = 0
        elif v == 0:
            if adj_black == 2:
                new_floor[k] = 1

    black = 0
    for k,v in new_floor.items():
        if v == 1:
            black += 1

    print("Day ",day,":",black)

    floor_map = copy.deepcopy(new_floor)
    return floor_map

for day in range(1,101):
    floor_map = update_day(floor_map,day)

#for k,v in floor_map.items():
#    x = k[0]
#    y = k[1]
#    color = v
#    if v == 1:
#        color = 'black'
#    else:
#        color = 'white'
        
#    plt.scatter(x,y,color=color, marker="h",edgecolors='black', s=10)

#plt.show()