from os import truncate
import networkx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from intcode import *

N = 1
S = 2
W = 3
E = 4

def draw_maze(walls, maze):

    N = 60
    # make an empty data set
    data = np.ones((N, N)) * np.nan
    # fill in some fake data
    for p in walls:
        data[p[0]+N//2,p[1]+N//2] = 1
    for p in maze:
        data[p[0]+N//2,p[1]+N//2] = 2

    data[15+N//2,-12+N//2] = 3
    data[0+N//2, 0+N//2] = 4

    # make a figure + axes
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    # make color map
    my_cmap = matplotlib.colors.ListedColormap(['k', 'c', 'r', 'g'])
    # set the 'bad' values (nan) to be white and transparent
    my_cmap.set_bad(color='w', alpha=0)
    # draw the grid
    for x in range(N + 1):
        ax.axhline(x, lw=2, color='k', zorder=5)
        ax.axvline(x, lw=2, color='k', zorder=5)
    # draw the boxes
    ax.imshow(data, interpolation='none', cmap=my_cmap, extent=[0, N, 0, N], zorder=0)
    # turn off the axis labels
    ax.axis('off')
    plt.show()
    plt.savefig('maze.jpg')

def getMoves(x,y,walls):
    options = []
    if (x,y+1) not in walls:
        options.append(N)
    if (x,y-1) not in walls:
        options.append(S)
    if (x-1,y) not in walls:
        options.append(W)
    if (x+1,y) not in walls:
        options.append(E)
    return options

def turnRight(hdg):
    if hdg == N: 
        return E 
    if hdg == S: 
        return W 
    if hdg == W: 
        return N 
    if hdg == E: 
        return S 
    else:
        print("ERROR")

def turnLeft(hdg):
    if hdg == N: 
        return W 
    if hdg == S: 
        return E
    if hdg == W: 
        return S
    if hdg == E: 
        return N
    else:
        print("ERROR")

def turnAround(hdg):
    if hdg == N: 
        return S 
    if hdg == S: 
        return N
    if hdg == W: 
        return E
    if hdg == E: 
        return W
    else:
        print("ERROR")

def wallLocation(x,y,heading):
    if heading == N:
        wall_y = y + 1
        wall_x = x
    if heading == S:
        wall_y = y - 1
        wall_x = x                    
    if heading == W:
        wall_x = x - 1
        wall_y = y
    if heading == E:
        wall_x = x + 1
        wall_y = y
    return (wall_x,wall_y)

def movedForward(x,y,heading):
    if heading == N:
        y = y + 1
    if heading == S:
        y = y - 1
    if heading == W:
        x = x - 1
    if heading == E:
        x = x + 1
    return x,y

leak_x = 0
leak_y = 0

def day15():
    instructions = "3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,101,0,1034,1039,101,0,1036,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,102,1,1034,1039,101,0,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1105,1,124,1001,1034,-1,1039,1008,1036,0,1041,1002,1035,1,1040,1002,1038,1,1043,1001,1037,0,1042,1105,1,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,101,0,1038,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,35,1032,1006,1032,165,1008,1040,33,1032,1006,1032,165,1102,2,1,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1101,1,0,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,27,1044,1105,1,224,1101,0,0,1044,1105,1,224,1006,1044,247,101,0,1039,1034,1002,1040,1,1035,101,0,1041,1036,1001,1043,0,1038,101,0,1042,1037,4,1044,1106,0,0,8,86,20,11,8,18,84,20,96,25,15,28,96,20,74,24,7,5,77,6,77,6,23,74,3,23,93,21,72,23,1,57,87,10,17,9,23,48,16,9,32,11,62,73,5,70,2,10,77,23,16,76,24,28,13,46,92,26,15,10,87,13,28,54,10,50,4,16,47,75,24,55,4,99,92,17,66,24,7,13,33,43,21,65,24,4,74,40,8,28,25,5,72,25,5,54,19,72,6,44,49,3,65,11,24,85,39,11,5,77,15,6,65,12,66,66,14,8,88,81,2,8,99,7,54,70,2,97,69,9,17,51,47,1,56,88,81,41,10,98,16,23,35,24,82,24,5,99,39,67,8,14,46,56,5,8,59,9,53,9,21,95,6,95,7,12,85,26,79,82,19,21,62,99,5,13,81,19,31,15,29,67,45,22,75,84,14,25,83,33,97,4,85,15,17,25,21,51,55,11,76,32,15,43,60,13,13,11,65,65,16,9,96,26,17,10,94,23,12,37,16,49,2,81,17,11,20,17,16,37,87,16,12,96,23,10,68,22,75,34,4,22,14,34,14,62,8,34,12,72,7,40,5,54,10,89,7,96,1,14,72,7,11,60,93,68,51,21,86,25,34,26,20,38,7,21,94,78,10,8,46,4,81,12,84,30,11,9,48,12,83,73,42,83,26,26,40,22,91,6,38,99,2,40,24,93,10,22,84,22,19,94,8,6,42,33,11,15,31,66,33,2,65,39,67,26,5,67,19,86,1,12,20,28,54,80,84,3,17,32,26,51,8,6,20,67,15,54,30,5,31,97,9,10,29,18,45,8,23,69,18,61,11,4,73,5,46,13,96,16,80,66,17,1,11,50,37,4,34,94,15,32,77,5,93,69,12,66,6,24,18,84,26,42,5,78,74,22,82,15,23,60,11,64,61,59,48,11,99,49,3,68,2,16,14,99,7,94,9,22,75,20,30,21,17,91,20,41,21,26,42,44,19,18,85,17,96,21,2,88,62,69,8,39,3,11,62,12,25,29,69,79,52,56,6,52,22,78,42,8,18,22,59,91,13,94,89,10,16,73,11,17,80,81,26,36,26,55,16,13,30,6,6,43,1,43,83,21,69,11,42,8,77,21,31,25,24,99,26,56,85,15,74,1,88,13,3,18,42,14,54,13,6,91,49,7,36,42,2,8,67,55,14,35,5,33,6,96,24,94,24,59,46,18,4,61,95,2,33,33,2,31,24,97,1,91,15,52,15,53,44,10,20,47,93,8,1,48,80,22,80,23,15,92,18,18,59,19,69,17,8,55,38,26,9,68,23,85,2,12,23,77,4,21,16,6,90,45,17,61,16,28,22,24,58,30,26,2,85,1,53,29,18,37,30,38,4,12,92,60,19,13,56,19,85,7,66,19,73,39,9,90,81,3,8,9,72,25,37,24,5,96,25,13,81,92,34,19,95,3,26,36,25,25,25,15,95,6,35,43,92,10,79,70,8,30,18,96,75,1,5,76,17,86,3,46,22,11,50,96,1,56,43,2,23,53,7,71,20,61,73,34,31,57,24,69,4,24,6,25,98,50,21,63,12,97,11,9,72,19,40,21,7,2,18,77,83,16,1,82,24,25,57,72,25,9,15,76,21,14,71,16,94,7,64,21,69,87,18,65,1,21,20,61,91,10,86,7,55,36,1,40,99,39,8,41,5,92,76,33,20,40,15,81,76,48,5,35,64,59,6,30,13,52,19,84,21,58,1,89,29,53,10,76,22,33,26,65,3,96,0,0,21,21,1,10,1,0,0,0,0,0,0"
    ProgramA = Intcode(instructions)
    ProgramA.start()

    maze = []
    walls = []
    heading = N
    cur_x = 0
    cur_y = 0
    moves = 0

    G = networkx.Graph()
    G.add_node((0,0))

    ProgramA.add_input(heading) 
    ProgramA.wait_for_output()

    while ProgramA.halted == False:
        
        result = ProgramA.outputs[-1]
        ProgramA.outputs = []
        if result == 0: #hit wall
            wall = wallLocation(cur_x,cur_y,heading)
            if wall not in walls:    
                #print("wall",wall)
                walls.append(wall)
        
        if result == 1: #no wall
            orig_y = cur_y
            orig_x = cur_x

            cur_x, cur_y = movedForward(cur_x,cur_y,heading)
            moves = moves + 1
            #print(moves)

            if (cur_x,cur_y) not in maze:
                #print(cur_x,cur_y)
                maze.append((cur_x,cur_y))
                G.add_node((cur_x,cur_y))
                G.add_edge((cur_x,cur_y), (orig_x,orig_y))

        if result == 2:
            ProgramA.halted = True
            leak_x = cur_x
            leak_y = cur_y
            #print(leak_x,leak_y)
            break

        mvforward = wallLocation(cur_x,cur_y,heading)
        mvleft = wallLocation(cur_x,cur_y,turnLeft(heading))
        mvright = wallLocation(cur_x,cur_y,turnRight(heading))

        if mvright not in walls and mvright not in maze:
            heading = turnRight(heading)
        elif mvforward not in walls and mvforward not in maze:
            heading = heading
        elif mvleft not in walls and mvleft not in maze:
            heading = turnLeft(heading)

        elif mvright not in walls:
            heading = turnRight(heading)
        elif mvforward not in walls:
            heading = heading
        elif mvleft not in walls:
            heading = turnLeft(heading)
        else:
            heading = turnAround(heading)

        ProgramA.add_input(heading)
        ProgramA.wait_for_output()

    return G, leak_x, leak_y


def day15p1():    
    G, leak_x, leak_y = day15()
    return  (len(networkx.shortest_path(G, source=(leak_x,leak_y), target=(0,0))))


def day15p2():
    G, leak_x, leak_y = day15()
    node_list = G.nodes()
    maxdistance = 0
    for n in node_list:
        distance = len(networkx.shortest_path(G, source=(leak_x,leak_y), target=n))
        if distance > maxdistance:
            maxdistance = distance
    return maxdistance

print(day15p1()) #15 -12
print(day15p2())