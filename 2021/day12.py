import networkx as nx
import matplotlib.pyplot as plt

ans = 0

def build_map(filename):
    G = nx.Graph()
    nodes = []
    with open(filename) as f:
        lines = f.readlines()
        for l in lines:
            n1 = l.split('-')[0].strip()
            n2 = l.split('-')[1].strip()
            G.add_node(n1)
            G.add_node(n2)
            G.add_edge(n1,n2)

    return G

def build_path(G,path):
    global ans 
    moves = list(G.adj[path[-1]])
    if 'start' in moves:
        moves.remove('start')

    for m in moves:   
        
        newpath = path.copy()

        if m.islower() and m in newpath: #don't revisit a small room
            pass
        else:
            newpath.append(m)

            if newpath[-1] == 'end':
                ans +=1
            else:
                build_path(G,newpath)

def check_small_ones(path):
    small_count = 0
    valid = True
    for p in path:
        if p.islower() and path.count(p) > 1:
            small_count += 1
    #print(small_count,path)
    if small_count <= 2:
        return True
    return False


def build_path2(G,path):
    global ans 
    moves = list(G.adj[path[-1]])
    if 'start' in moves:
        moves.remove('start')

    for m in moves:   
        
        newpath = path.copy()
        if check_small_ones(newpath) == False:
            pass
        else:
            newpath.append(m)

            if newpath[-1] == 'end':
                ans +=1
            else:
                build_path2(G,newpath)

def part1(filename):
    G = build_map(filename)
    path = ['start']
    build_path(G,path)
    print("DONE",ans)


def part2(filename):
    G = build_map(filename)
    path = ['start']
    build_path2(G,path)
    print("DONE",ans)


#part1('day12_ex1.txt') #10
#part1('day12_ex2.txt') #19
#part1('day12_ex3.txt') #226
#part1('day12_input.txt')

#part2('day12_ex1.txt') #36
#part2('day12_ex2.txt') #103
#part2('day12_ex3.txt') #3509
part2('day12_input.txt')