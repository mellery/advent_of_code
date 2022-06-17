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
    xsize = len(maze[0])
    for y in range(0,ysize):
        for x in range(0,xsize):
            if maze[y][x] != '#':
                temp = G.nodes[(y,x)]["val"]
                if temp == k:
                    return((y,x))            
    return None

@lru_cache(maxsize=None)
def distanceTo(cur,k,locked):
    
    try:
        path = (nx.shortest_path(G2, source=cur,target=k, weight='weight'))

        for p in path:
            if p in list(locked): #the path is blocked by a locked door
                return sys.maxsize 
            if p in list(locked.lower()) and p != k: #there's a key we haven't picked up on in this path so this isn't an optimal route
                return sys.maxsize
    
        return nx.shortest_path_length(G2, source=cur,target=k, weight='weight')
    except:
        return sys.maxsize


def buildMaze(input):
    maze = []
    robot = 1
    with open(input) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    for line in lines:
        maze.append(list(line))

    ysize = len(maze)
    xsize = len(maze[0])

    G = nx.Graph()
    for y in range(0,ysize):
        for x in range(0,xsize):
            if maze[y][x] != '#':
                if maze[y][x] == '@':
                    G.add_node((y,x),val=str(robot))
                    robot = robot+1
                else:
                    G.add_node((y,x),val=maze[y][x])
                

    for y in range(0,ysize):
        for x in range(0,xsize):
            if maze[y][x] != '#':
                if y > 0:
                    if maze[y-1][x] != '#':
                        G.add_edge((y,x),(y-1,x))
                if x > 0:
                    if maze[y][x-1] != '#':
                        G.add_edge((y,x),(y,x-1))
                if y < ysize-1:
                    if maze[y+1][x] != '#':
                        G.add_edge((y,x),(y+1,x))
                if x < xsize-1:
                    if maze[y][x+1] != '#':
                        G.add_edge((y,x),(y,x+1))

    #nx.draw(G,with_labels=True)
    #plt.show()

    return G, maze

#####################################################  

def findHighestKey():
    k = 'a'
    ysize = len(maze)
    xsize = len(maze[0])
    for y in range(0,ysize):
        for x in range(0,xsize):    
            if maze[y][x] > k:
                k = maze[y][x]
    return k

#####################################################  

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

        

    #pos=nx.get_node_attributes(G2,'pos')
    #nx.draw(G2,pos,with_labels=True)
    #labels = nx.get_edge_attributes(G2,'weight')
    #nx.draw_networkx_edge_labels(G2,pos,edge_labels=labels)    
    #plt.show()

    return G2

#####################################################  

def searchMaze(door, locked, travel):   
    global p1ans 

    locked = locked.replace(door.upper(),"")
        
    if len(locked) == 0: 
        if travel < p1ans:
            p1ans = travel
            print(travel)

    else:
        for o in list(locked):
            mv = distanceTo(door,o.lower(),locked)
            if mv < sys.maxsize:
                tempt = travel + mv
                if tempt < p1ans:
                    searchMaze(o.lower(), locked,tempt)

#####################################################

def searchMultiMaze(doors, locked, travel):   
    global p2ans 

    bots = list(doors)
    if len(locked) == 0: 
        if travel < p2ans:
            p2ans = travel
        print("done:",travel)

    else:
        for o in list(locked):
            for b in range(0,len(bots)):

                mv = distanceTo(bots[b],o.lower(),locked)

                if mv < sys.maxsize and mv > 0:
                    tempt = travel + mv
                    if tempt < p2ans:
                        bots[b] = o.lower()
                        newbots = "".join(bots)
                        newlocked = locked.replace(o,"")
                        #print(newbots," ",locked,travel,'\tbot',b+1,'picked up',bots[b],'by moving ',mv,newlocked,'total dist',tempt)
                        searchMultiMaze(newbots, newlocked, tempt)

#####################################################

def day18p1(input_file):
    global maze
    global G
    global G2
    global p1ans

    G, maze = buildMaze(input_file)
    lastkey = findHighestKey()

    location = dict()
    location['@'] = findLocation('@')
    

    locked = ""

    for i in range(ord('a'), ord(lastkey)+1):
        locked = locked + chr(i).upper()
        location[chr(i)] = findLocation(chr(i))
        location[chr(i).upper()] = findLocation(chr(i).upper())

    G2 = buildGraph(location)

    p1ans = sys.maxsize
    

    start_time = time.time()
    searchMaze('@', locked, 0)
    print("--- %s seconds ---" % (time.time() - start_time))

#####################################################

def day18p2(input_file):
    global maze
    global G
    global G2
    global p2ans

    p2ans = sys.maxsize

    G, maze = buildMaze(input_file)
    lastkey = findHighestKey()

    location = dict()
    
    location['1'] = findLocation('1')
    location['2'] = findLocation('2')
    location['3'] = findLocation('3')
    location['4'] = findLocation('4')

    locked = ""

    for i in range(ord('a'), ord(lastkey)+1):
        locked = locked + chr(i).upper()
        location[chr(i)] = findLocation(chr(i))
        location[chr(i).upper()] = findLocation(chr(i).upper())

    G2 = buildGraph(location)

    #locked = 'ABCDEFGHIJKLMNO'
    #locked = 'EHBCDFGAIJKLMNO'
    
    #print(perms)
    
    start_time = time.time()
    for x in range(0,1000):
        l = list(locked)
        random.shuffle(l)
        locked = ''.join(l)
        #print(locked)
        searchMultiMaze('1234', locked, 0)

    #mv = distanceTo('1','e',locked)
    #print(mv,locked)
    #locked = locked.replace('E','')
    #mv = mv + distanceTo('2','h',locked)
    #print(mv,locked)
    #locked = locked.replace('H',"")
    #mv = mv + distanceTo('4','i',locked)
    #print(mv,locked)
    #locked = locked.replace('I',"")
    #mv = mv + distanceTo('e','a',locked)
    #print(mv,locked)
    #locked = locked.replace('A',"")
    #mv = mv + distanceTo('a','b',locked)
    #print(mv,locked)
    #locked = locked.replace('B',"")
    #mv = mv + distanceTo('h','c',locked)
    #print(mv,locked)
    #locked = locked.replace('C',"")
    #mv = mv + distanceTo('b','d',locked)
    #print(mv,locked)
    #locked = locked.replace('D',"")
    #mv = mv + distanceTo('d','f',locked)
    #print(mv,locked)
    #locked = locked.replace('F',"")
    #mv = mv + distanceTo('f','g',locked)
    #print(mv,locked)
    #locked = locked.replace('G',"")
    #mv = mv + distanceTo('i','k',locked)
    #print(mv,locked)
    #locked = locked.replace('K',"")
    #mv = mv + distanceTo('k','j',locked)
    #print(mv,locked)
    #locked = locked.replace('J',"")
    #mv = mv + distanceTo('c','l',locked)
    #print(mv,locked)
    #locked = locked.replace('L',"")
    #mv = mv + distanceTo('3','n',locked)
    #print(mv,locked)
    #locked = locked.replace('N',"")
    #mv = mv + distanceTo('n','m',locked)
    #print(mv,locked)
    #locked = locked.replace('M',"")
    #mv = mv + distanceTo('m','o',locked)
    #print(mv,locked)
    #locked = locked.replace('O',"")
    #print(mv,locked)
    print("--- %s seconds ---" % (time.time() - start_time))


#day18p1("day18_ex1.txt")
#day18p1("day18_ex2.txt")
#day18p1("day18_ex3.txt")
#day18p1("day18_ex4.txt") #takes 2 hours
#day18p1("day18_ex5.txt")
#day18p1("day18_input.txt") #4544 part 1 solution #takes 15 minutes

#day18p2("day18_ex6.txt") #8 steps
#day18p2("day18_ex7.txt") #24 steps
#day18p2("day18_ex8.txt") #32 steps
#day18p2("day18_ex9.txt") #72 steps #gives wrong answer 74
day18p2("day18_input2.txt") #1692 #gives wrong anser 2202

