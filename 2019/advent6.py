class Node(object):
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None

    def add_child(self, obj):
        self.children.append(obj)
    
    def add_parent(self, parent_name):
        self.parent = parent_name
    
    def print_children(self):
        print(self.name,"has children")
        for x in self.children:
            print(x.name)

    def __repr__(self):
        return "Node(%s)" % (self.name)
    def __eq__(self, other):
        if isinstance(other, Node):
            return ((self.name == other.name))
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return hash(self.__repr__())


def num_orbits(planet):
    orbits = 0
    temp = planets[planets.index(Node(planet))]
    #print(temp.parent)
    while (temp.parent is not None):
        temp = planets[planets.index(Node(temp.parent))]
        #print(temp.parent)
        orbits = orbits + 1
    return orbits

def get_transfers(planet):
    transfers = []
    temp = planets[planets.index(Node(planet))]
    transfers.append(temp.parent)
    while (temp.parent is not None):
        temp = planets[planets.index(Node(temp.parent))]
        if temp.parent is not None:
            transfers.append(temp.parent)
    return transfers


planets = []

f = open("day6_input.txt")
#f = open("day6_input_ex.txt")
lines = f.read().splitlines()
for l in lines:
    
    bodys = l.split(')')
    #print(bodys[1],"orbits",bodys[0])
    
    if Node(bodys[0]) not in planets:
        planets.append(Node(bodys[0]))
    if Node(bodys[1]) not in planets:
        planets.append(Node(bodys[1]))
    
    planets[planets.index(Node(bodys[0]))].add_child(Node(bodys[1]))
    planets[planets.index(Node(bodys[1]))].add_parent(bodys[0])


total = 0
for p in planets:
    temp = num_orbits(p.name)
    total = total + temp
print("total orbits",total)

dir1 = get_transfers("YOU")
dir2 = get_transfers("SAN")

for d in dir1[::-1]:
    if d in dir2:
        dir2.remove(d)
        dir1.remove(d)
        print("removing ",d)

print(dir1[::-1])
print(dir2[::-1])
print(len(dir1),len(dir2),len(dir1)+len(dir2))
