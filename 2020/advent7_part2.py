#filename = "day7_ex1.txt" #32
#filename = "day7_ex2.txt" #126
filename = "day7_input.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

recipies = []

for l in lines:
    recipie = l.strip().split('contain')
    bag = recipie[0]
    holds = []
    
    temp = recipie[1].split(',')
    #print(temp)
    for t in temp:
        r = t.strip('.')
        r = r.strip('.')
        r = r.strip()
        holds.append(r)
    
    #print((bag,holds))
    recipies.append((bag,holds))


start = 'shiny gold'

def get_contents(name):
    #print("getting contents of ",name)
    holds = []
    for r in recipies:
        #print(r)
        #print(name)
        if name in r[0]:
            #print("found",name)
            for r in r[1]:
                if r.split(' ')[0] == 'no':
                    qty = 0
                else:
                    qty = int(r.split(' ')[0])
                val = r.split(' ')[1] + " " + r.split(' ')[2]
                for x in range(0,qty):
                    holds.append(val)
            #print(name,"holds",holds)
    return(holds)

gold_holds = []

for x in get_contents(start):
    #temp = x.split(' ')[1] + " " + x.split(' ')[2]
    #print(x)
    gold_holds.append(get_contents(x))

temp = gold_holds
for x in temp:
    for y in x:
        gold_holds.append(get_contents(y))
    
    
print("---")
#print(gold_holds)
print(len(gold_holds))
total = 0
for x in gold_holds:
    total = total + len(x)
total = total + len(gold_holds)
#print(total)

