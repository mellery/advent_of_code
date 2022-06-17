import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing import layout
import numpy as np

def makegraph(filename):
    G = nx.DiGraph()

    with open(filename) as f:
        lines = f.readlines()
        r = 0
        grid = {}

        for repeat in range(0,5):        
            for l in lines:
                row = list(l.strip())
                row = [int(r) for r in row]
                #print(repeat,'old',row)
                row = [r+repeat for r in row]
                row = [r%9 if r > 9 else r for r in row]
                newrow = row.copy()
                #print(repeat,'new',row)
                temp = row.copy()
                for y in range(0,4):
                    temp = [t+1 for t in temp]
                    temp = [1 if t > 9 else t for t in temp]
                    newrow += temp
            
                c = 0
                row = newrow.copy()
                for g in row:
                    
                    grid[(r,c)] = int(g)
                    #print((r,c),g)
                    
                    G.add_node((r,c), weight = int(g))
                    c += 1
                r += 1

        for row in range(0,r):
            for col in range(0,c):
                if (row-1,col) in grid:
                    G.add_edge((row,col),(row-1,col), weight=grid[(row-1,col)])
                if (row+1,col) in grid:
                    G.add_edge((row,col),(row+1,col), weight=grid[(row+1,col)])
                if (row,col-1) in grid:
                    G.add_edge((row,col),(row,col-1), weight=grid[(row,col-1)])
                if (row,col+1) in grid:
                    G.add_edge((row,col),(row,col+1), weight=grid[(row,col+1)])

        #print(grid)

    return G, grid, r-1,c-1



def part1(filename):
    G, grid,r,c = makegraph(filename)

    path = nx.dijkstra_path(G,(0,0),(r,c),weight='weight')
    #path = nx.shortest_path(G,(0,0),(2,4),weight='weight')
    risk = 0
    for p in path[1:]:
        risk+= grid[p]
        #print(p,grid[p],G.nodes[p])
    print(risk)

    #labels = nx.get_node_attributes(G,'weight')
    #pos = nx.spring_layout(G, iterations=100, seed=39775)
    #nx.draw(G, pos, with_labels=True, labels=labels)
    #plt.show()

#part1("day15_ex1.txt")
part1("day15_input.txt")