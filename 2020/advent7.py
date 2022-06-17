from collections import deque

filename = "input7.txt"
#filename = "input7_ex.txt" #32
#filename = "input7_ex2.txt" #126

file1 = open(filename, 'r') 
lines = file1.readlines() 

all_bags = 0

class Node:
    def __init__(self, name, qty):
        self.children = []
        self.name = name
        self.qty = qty
        self.depth = 0
        self.total = 0
        self.holds = self.GetHolds()

    def GetDepth(self):
        return self.depth

    def GetHolds(self):
        #print(self.name,"holds",len(self.children),"bags")
        return len(self.children)

    def insert(self, bag):
        bag.depth = self.depth + 1
        #print("adding qty",1,"of",bag.name,"to",self.name)
        self.children.append(bag)
        
    def PrintTree(self):
        print(self.depth*'-',self.name,": qty=",self.qty," holds=",self.GetHolds())
        
        for b in self.children:
            print(b.PrintTree())

    def __repr__(self):
        global all_bags
        #all_bags = all_bags + int(self.qty)*int(self.GetHolds())
        #all_bags = all_bags + int(self.GetHolds()) + 1
        all_bags = all_bags + int(self.qty)*int(self.GetHolds())
        return f"Bag({self.name},{int(self.qty)*int(self.GetHolds())}): {self.children}"

#part 1

holds_gold = []

for l in lines:
    temp = l.strip()
    model = temp.split('contain')[0].strip()
    if model.endswith('s'):
        model = model[:-1]
    
    #print(model)
    holds = temp.split('contain')[1].split(',')
    for b in holds:
        if 'shiny gold' in b and model not in holds_gold:
            holds_gold.append(model)
    #print(model,"holds",holds)

#print(holds_gold)

bags_added = True
while bags_added == True:
    bags_added = False
    for b2 in holds_gold:
        for l in lines:
            temp = l.strip()
            model = temp.split('contain')[0].strip()
            if model.endswith('s'):
                model = model[:-1]

            holds = temp.split('contain')[1].split(',')
        
            holdsstr = "".join(holds)
            if b2 in holdsstr and model not in holds_gold:
                bags_added = True
                holds_gold.append(model)
            

#for b in holds_gold:
    #print(b)
print("part1:",len(holds_gold))


root = Node("shiny gold",1)    
curnode = root


for l in lines:
    temp = l.strip()
    model = temp.split('contain')[0].strip()
    if model.endswith('s'):
        model = model[:-1]
    
    holds = temp.split('contain')[1].split(',')

    if 'shiny gold' in model:
        for b in holds:
            name = b.split(' ')[2]+' '+b.split(' ')[3]
            qty = b.strip().split(' ')[0]
            if qty == 'no':
                qty = 0
            qty = int(qty)
            for q in range(0,qty):
                curnode.insert(Node(name,qty))

print(root)

def add_children(curnode):

    for c in curnode.children:
        #print(c.name)
        tempnode = c

        for l in lines:
            temp = l.strip()
            model = temp.split('contain')[0].strip()
            if model.endswith('s'):
                model = model[:-1]
    
            holds = temp.split('contain')[1].split(',')

            if c.name in model:
                #print(c.name,holds)
                
                for b in holds:
                    
                    name = b.split(' ')[2]+' '+b.split(' ')[3]
                    qty = b.strip().split(' ')[0]
                    if qty == 'no':
                        qty = 0
                    qty = int(qty)

                    #temp = Node(b,qty)

                    for x in range(0,qty):
                        tempnode.insert(Node(name,qty))
                    #val = input("enter to continue")
                    #print(qty,all_bags+1)
                    
                    add_children(tempnode)
                
add_children(curnode)    

root.PrintTree()

print(root)
print(all_bags+1)