import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math
import copy 

import random

import re

filename = "input20.txt"
#filename = "input20_ex1.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

e = ['A','B','C','D']

def match_edges(P1,P2):
    side = "none"
    if (P1.sideA() in P2.sides()):
        side = "A-" + e[P2.sides().index(P1.sideA())]
    elif (P1.sideB() in P2.sides()):
        side = "B-" + e[P2.sides().index(P1.sideB())]
    elif (P1.sideC() in P2.sides()):
        side = "C-" + e[P2.sides().index(P1.sideC())]
    elif (P1.sideD() in P2.sides()):
        side = "D-" + e[P2.sides().index(P1.sideD())]
    elif (P1.sideA()[::-1] in P2.sides()):
        side = "Arev-" + e[P2.sides().index(P1.sideA()[::-1])]
    elif (P1.sideB()[::-1] in P2.sides()):
        side = "Brev-" + e[P2.sides().index(P1.sideB()[::-1])]
    elif (P1.sideC()[::-1] in P2.sides()):
        side = "Crev-" + e[P2.sides().index(P1.sideC()[::-1])]
    elif (P1.sideD()[::-1] in P2.sides()):
        side = "Drev-" + e[P2.sides().index(P1.sideD()[::-1])]
    else:
        side = "none"
    return side

def print_puzzle():
    for y in range(0,edge_len):
        for r in range(0,10):
            line = ""
            for x in range(0,edge_len):
                line = line + Puzzle[int(assembled[(x,y)])].image[r] + '   '
            print(line)
        print('')

def get_puzzle2():
    new_image = []
    for y in range(0,edge_len):
        for r in range(0,8):
            line = ""
            for x in range(0,edge_len):
                line = line + Puzzle[int(assembled[(x,y)])].image2[r] #+ '   '
            print(line)
            new_image.append(line)
    return new_image

def print_assembled_ids(assembled):
    for y in range(0,edge_len):
        line = ""
        for x in range(0,edge_len):
            if (x,y) in assembled:
                line = line + str(assembled[(x,y)]) + ' '
            else:
                line = line + "?\t"
        print(line)
    print('\n')

def look_for_monsters(p):
    monsters = 0
    for l in range(1,len(p.image)-1):
        #todo is this search good enough? - NO
        body = re.search('#....##....##....###',p.image[l])
        if body:
            head = re.search('..................#.',p.image[l-1][body.span()[0]:body.span()[1]])
            tail = re.search('.#..#..#..#..#..#...',p.image[l+1][body.span()[0]:body.span()[1]])
    
            if head and body and tail:
                monsters = monsters + 1
    
    return monsters

class Piece:
    id = 0
    orient = 0
    image = []
    image2 = []

    def removeBorder(self):
        temp = []
        for i in self.image[1:-1]:
            temp.append(i[1:-1])
        self.image2 = copy.deepcopy(temp)

    def rotate90(self):
        temp = []
        temp = zip(*self.image[::-1])
        temp2 = []
        for t in temp:
            temp2.append("".join(t))
        
        self.image = copy.deepcopy(temp2)

    def rotate180(self):
        self.rotate90()
        self.rotate90()

    def rotate270(self):
        self.rotate90()
        self.rotate90()
        self.rotate90()

    def flipX(self):
        temp = []
        for i in self.image:
            temp.append(i[::-1])
        self.image = copy.deepcopy(temp)

    def flipY(self):
        temp = []
        for i in self.image[::-1]:
            temp.append(i)
        self.image = copy.deepcopy(temp)    

    def printImage(self):
        for r in self.image:
            print(r)
        print('\n')

    def printImage2(self):
        for r in self.image2:
            print(r)
        print('\n')

    def sides(self):
        return [self.sideA(),self.sideB(),self.sideC(),self.sideD()]

    def sideA(self):
        return self.image[0]

    def sideB(self):
        temp = ""
        for x in range(0,len(self.image)):
            temp = temp+self.image[x][len(self.image)-1]
        return(temp)

    def sideC(self):
        temp = ""
        for x in range(0,len(self.image)):
            temp = temp+self.image[x][0]
        return(temp)

    def sideD(self):
        return self.image[len(self.image)-1]

Puzzle = {}

id = 0
tile = []

for l in lines:
    temp = l.strip()

    if 'Tile' in temp:
        if id not in Puzzle and id != 0:
            p = Piece()
            p.id = id
            p.image = tile.copy()
            Puzzle[id] = p
            tile = []
        
        id = int(temp.split(' ')[1][:-1])
        
    elif len(temp) > 1:
        tile.append(temp)

#add the last tile
if id not in Puzzle and id != 0:
    p = Piece()
    p.id = id
    p.image = tile.copy()
    Puzzle[id] = p
    tile = []
    print("adding",id)

corners = []

G = nx.Graph()

for k1,v1 in Puzzle.items():
    matches = 0
    for k2,v2 in Puzzle.items():
        if k1 != k2:
            if v1.sideA() in v2.sides():
                G.add_edges_from([(str(k1),str(k2))])
                matches = matches + 1
            if v1.sideB() in v2.sides():
                G.add_edges_from([(str(k1),str(k2))])
                matches = matches + 1
            if v1.sideC() in v2.sides():
                G.add_edges_from([(str(k1),str(k2))])
                matches = matches + 1
            if v1.sideD() in v2.sides():
                G.add_edges_from([(str(k1),str(k2))])
                matches = matches + 1
            if v1.sideA()[::-1] in v2.sides():
                G.add_edges_from([(str(k1),str(k2))])
                matches = matches + 1
            if v1.sideB()[::-1] in v2.sides():
                G.add_edges_from([(str(k1),str(k2))])
                matches = matches + 1
            if v1.sideC()[::-1] in v2.sides():
                G.add_edges_from([(str(k1),str(k2))])
                matches = matches + 1
            if v1.sideD()[::-1] in v2.sides():
                G.add_edges_from([(str(k1),str(k2))])
                matches = matches + 1
    if matches == 2:
        corners.append(k1)

print(corners)
ans = 1
for c in corners:
    ans = ans * c
print(ans)

#nx.draw(G, with_labels=True)
#plt.show()

assembled = {}
assembled[(0,0)] = Puzzle[corners[0]].id

edge_len = int(math.sqrt(len(Puzzle)))

#find furthest corner
for c in corners[1:]:
    dist = nx.shortest_path_length(G,source=str(corners[0]), target=str(c))
    if dist > edge_len:
        assembled[(edge_len-1,edge_len-1)] = c

#assign other two corners
for c in corners[1:]:
    if c != assembled[edge_len-1,edge_len-1]:
        if (0,edge_len-1) not in assembled:
            assembled[(0,edge_len-1)] = c
        elif (edge_len-1,0) not in assembled:
            assembled[(edge_len-1),0] = c

#assign top edge
path = nx.shortest_path(G,source=str(assembled[(0,0)]),target=str(assembled[(edge_len-1,0)]))
for x in range(0,len(path)):
    assembled[(x,0)] = path[x]

#assign bottom edge
path = nx.shortest_path(G,source=str(assembled[(0,edge_len-1)]),target=str(assembled[(edge_len-1,edge_len-1)]))
for x in range(0,len(path)):
    assembled[(x,edge_len-1)] = path[x]

#assign left edge
path = nx.shortest_path(G,source=str(assembled[(0,0)]),target=str(assembled[(0,edge_len-1)]))
for x in range(0,len(path)):
    assembled[(0,x)] = path[x]

#assign right edge
path = nx.shortest_path(G,source=str(assembled[(edge_len-1,0)]),target=str(assembled[(edge_len-1,edge_len-1)]))
for x in range(0,len(path)):
    assembled[(edge_len-1,x)] = path[x]

#fill rows
for y in range(0,edge_len-1):
    path = nx.shortest_path(G,source=str(assembled[(0,y)]),target=str(assembled[(edge_len-1,y)]))
    for x in range(0,len(path)):
        assembled[(x,y)] = path[x]

print_assembled_ids(assembled)


if filename == "input20_ex1.txt":
    Puzzle[1951].flipY()
    
#setup first piece
if filename == "input20.txt":
    Puzzle[1831].rotate90()
    Puzzle[1831].flipY()
    
#align first column
for y in range(0,edge_len-1):
    result = match_edges(Puzzle[int(assembled[(0,y)])],Puzzle[int(assembled[0,y+1])])
    while result != 'D-A':
        op = random.choice([1,2,3])
        if op == 1:
            Puzzle[int(assembled[0,y+1])].rotate90()
        elif op == 2:
            Puzzle[int(assembled[0,y+1])].flipX()
        elif op == 3:
            Puzzle[int(assembled[0,y+1])].flipY()
        result = match_edges(Puzzle[int(assembled[(0,y)])],Puzzle[int(assembled[0,y+1])])

#align pieces
for y in range(0,edge_len):
    for x in range(0,edge_len-1):
        result = match_edges(Puzzle[int(assembled[(x,y)])],Puzzle[int(assembled[x+1,y])])
        while result != 'B-C':
            op = random.choice([1,2,3])
            if op == 1:
                Puzzle[int(assembled[x+1,y])].rotate90()
            elif op == 2:
                Puzzle[int(assembled[x+1,y])].flipX()
            elif op == 3:
                Puzzle[int(assembled[x+1,y])].flipY()
            result = match_edges(Puzzle[int(assembled[(x,y)])],Puzzle[int(assembled[x+1,y])])


print_puzzle()

for k,v in Puzzle.items():
    Puzzle[k].removeBorder()

new_image = []
new_image = get_puzzle2()

p = Piece()
p.id = 0
p.image = new_image.copy()

max_monsters = 0
for x in [0,90,180,270]:
    monsters = look_for_monsters(p)
    if monsters > max_monsters:
        max_monsters = monsters
        p.printImage()
    print(x,"orig",monsters)
    
    p.flipY()
    monsters = look_for_monsters(p)
    if monsters >= max_monsters:
        max_monsters = monsters
        p.printImage()
    print(x,"flipy",monsters)
    p.flipY()

    p.flipX()
    monsters = look_for_monsters(p)
    if monsters >= max_monsters:
        p.printImage()
        max_monsters = monsters
    print(x,"flipX",monsters)
    p.flipX()

    p.flipY()
    p.flipX()
    monsters = look_for_monsters(p)
    if monsters >= max_monsters:
        p.printImage()
        max_monsters = monsters
    print(x,"flipYX",monsters)
    p.flipX()
    p.flipY()

    p.flipX()
    p.flipY()
    monsters = look_for_monsters(p)
    if monsters >= max_monsters:
        p.printImage()
        max_monsters = monsters
    print(x,"flipXY",monsters)
    p.flipY()
    p.flipX()


    p.rotate90()

#todo - regex doesn't find multiple monsters on a line, manually counted them on regexr.com
max_monsters = 43

pounds = 0
for l in p.image:
    pounds = pounds + l.count('#')
print("pounds:\t",pounds)
print("monsters:\t",max_monsters)
print("ans:\t",pounds - (max_monsters * 15))

#2249 too high

