import networkx as nx
import matplotlib.pyplot as plt
import sys
from functools import lru_cache
import time
import random

maze = []

@lru_cache(maxsize=None)
def findLocation(k):
    ysize = len(maze)
    for y in range(0,ysize):
        for x in range(0,len(maze[y])-1):
            if maze[y][x] not in [' ','#']:
                temp = G.nodes[(y,x)]["val"]
                if temp == k and portalEntrance(maze,y,x):
                    return((y,x))            
    return None

@lru_cache(maxsize=None)
def distanceTo(cur,k):
    
    try:
        path = (nx.shortest_path(G2, source=cur,target=k, weight='weight'))
    
        return nx.shortest_path_length(G2, source=cur,target=k, weight='weight')
    except:
        return sys.maxsize


def buildMaze(input):
    maze = []
    
    with open(input) as file:
        lines = file.readlines()
        #lines = [line.rstrip() for line in lines]

    for line in lines:
        #print(line)
        maze.append(list(line))

    ysize = len(maze)
    

    G = nx.Graph()
    for y in range(0,ysize):
        for x in range(0,len(maze[y])-1):
            if maze[y][x] not in [' ','#']:
                G.add_node((y,x),val=maze[y][x])
                

    for y in range(0,ysize):
        #print(len(maze[y]))
        #print(maze[y])
        for x in range(0,len(maze[y])-1):
            if maze[y][x] not in [' ','#']:
                if y > 0:
                    #print(y-1,x)
                    if maze[y-1][x] not in [' ','#']:
                        G.add_edge((y,x),(y-1,x))
                if x > 0:
                    if maze[y][x-1] not in [' ',"#"]:
                        G.add_edge((y,x),(y,x-1))
                if y < ysize-1:
                    if maze[y+1][x] not in [' ',"#"]:
                        G.add_edge((y,x),(y+1,x))
                if x < len(maze[y])-1:
                    if maze[y][x+1] not in [' ',"#"]:
                        G.add_edge((y,x),(y,x+1))

    #nx.draw(G,with_labels=True)
    #plt.show()

    return G, maze

#####################################################  
def portalEntrance(maze,y,x):
    ysize = len(maze)
    try:
        if y+1 < ysize and maze[y+1][x] == '.':
            return True
        if y-1 >= 0 and maze[y-1][x] == '.':
            return True
        if x+1 < len(maze[y]) and maze[y][x+1] == '.':
            return True
        if x-1 >= 0 and maze[y][x-1] == '.':
            return True
        return False
    except:
        return False

def findPortals(maze):
    portals = []
    ysize = len(maze)
    for y in range(0,ysize):
        for x in range(0,len(maze[y])-1):    
            if maze[y][x] not in [' ', '.', '#']:
                if portalEntrance(maze,y,x):                
                    portals.append(maze[y][x])
    return portals

#####################################################  
def findPortalPairs():
    portalPairs = []
    ysize = len(maze)
    for y in range(0,ysize):
        for x in range(0,len(maze[y])-1):    
            try:
                if maze[y][x] not in [' ', '.', '#']:
                    temp = maze[y][x]
                    if y+1 < ysize and maze[y+1][x] not in [' ', '.', '#']:
                        temp = temp + maze[y+1][x]
                    if y-1 >= 0 and maze[y-1][x] not in [' ', '.', '#']:
                        temp = temp + maze[y-1][x]
                    if x+1 < len(maze[y]) and maze[y][x+1] not in [' ', '.', '#']:
                        temp = temp + maze[y][x+1]
                    if x-1 >= 0 and maze[y][x-1] not in [' ', '.', '#']:
                        temp = temp + maze[y][x-1]
                    if len(temp) == 2:
                        if temp not in portalPairs:
                            portalPairs.append(temp)
            except:
                continue

    return portalPairs

def buildGraph(location):
    G2 = nx.Graph()

    for k,v in location.items():
        if v != None:
            G2.add_node(k,pos=v)

            for k2,v2 in location.items():
                if v2 != None:
                    try:
                        dist = nx.shortest_path_length(G, source=v,target=v2)
                        path = nx.shortest_path(G, source=v,target=v2)
                        count = 0

                        for p in path:
                            if p in location.values():
                                count = count + 1
                        if count == 2:
                            G2.add_edge(k,k2,weight=dist)

                    except:
                        pass

    portalPairs = findPortalPairs()
    for p in portalPairs:
        print(p)
        pair = list(p)
        G2.add_edge(pair[0],pair[1],weight=1)
    


    pos=nx.get_node_attributes(G2,'pos')
    nx.draw(G2,pos,with_labels=True)
    labels = nx.get_edge_attributes(G2,'weight')
    nx.draw_networkx_edge_labels(G2,pos,edge_labels=labels)    
    plt.show()

    return G2

def day20p1(input_file):
    global maze
    global G
    global G2
    global p1ans

    location = dict()
    
    G, maze = buildMaze(input_file)
    portals = findPortals(maze)
    portals.sort()
    for p in portals:   
        location[p] = findLocation(p)    

    G2 = buildGraph(location)


    p1ans = sys.maxsize

    print(distanceTo('@','Z'))

    start_time = time.time()
    #searchMaze('@', locked, 0)
    print("--- %s seconds ---" % (time.time() - start_time))

day20p1("day20_ex1.txt") #23 #had to reverse GF
#day20p1("day20_ex2.txt")  #doesn't map right
#day20p1("day20_input.txt")