import random
import math
filename = '/home/mike/src/advent19/input14.txt' #1000000000000 ore

#filename = 'c:\\src\\advent19\\input14_ex1.txt'
#filename = 'c:\\src\\advent19\\input14_ex2.txt'
#filename = 'c:\\src\\advent19\\input14_ex3.txt' #13312 ore
#filename = 'c:\\src\\advent19\\input14_ex4.txt' #180697 ore
#filename = 'c:\\src\\advent19\\input14_ex5.txt' #2210736 ore

def parse_recipies(filename):
    file1 = open(filename, 'r') 
    lines = file1.readlines() 
    recipies = []
    for l in lines:
        inmat = l.split("=>")[0]
        outmat = l.split("=>")[1].strip()
    
        inputs = []
        temp = inmat.split(',')
        for t in temp:
            t2 = t.strip()
            v = int(t2.split(' ')[0])
            k = t2.split(' ')[1]
            inputs.append((v,k))
    
        output = [(int(outmat.split(' ')[0].strip()), outmat.split(' ')[1].strip())]

        recipies.append((inputs,output))

    for r in recipies:
        print(r)
    return recipies


def ore_needed(recipies,fuel_wanted):
    #print("trying to make",fuel_wanted,"fuel\r\n")
    goal = [(fuel_wanted,'FUEL')]
    have = goal
    
    #print("starting with",have)

    swapped = 1
    while swapped == 1:
        swapped = 0
        random.shuffle(have)
        random.shuffle(recipies)
        for h in have:
            for r in recipies:
                r_name = r[1][0][1]
                r_count = r[1][0][0]
                h_name = h[1]
                h_count = h[0]
                #print(h_count,h_name)
                #if r_name == h_name and h_count >= r_count:
                if r_name == h_name and h_count > 0:
                    #print(h_count,r_count,round(h_count/r_count))
                    qnt = math.ceil(h_count/r_count)
                    #print("have",have)
                    #print("spend",r[1][0],"to make",r[0],"qty",qnt)
                    
                    #print(h)
                    have.remove(h)
                    have.append((h_count-r_count*qnt,h_name))
                    #print("remove",r[1][0],"now have",have)
                    for e in r[0]:
                    
                        added = 0
                        for i in range(0,len(have)):
                            
                            if e[1] == have[i][1]:
                                #print(e,have[i])
                                have.append((e[0]*qnt+have[i][0],e[1]))
                                have.remove(have[i])
                                added = 1
                                break
                        if added == 0:
                            have.append((e[0]*qnt,e[1]))
                    
                    for h in have:
                        if h[0] == 0:
                            have.remove(h)

                    #print("now have",have,'\r\n')
                    swapped = 1

    
    for h in have:
        if h[1] == 'ORE':
            return h[0]

    return 0

recipies = parse_recipies(filename)

cargo_hold = 1000000000000
fuel = 1
result = ore_needed(recipies,fuel)
print(result)
#part 2
#print(ore_needed(recipies,3279311),"ore needed")
#print(ore_needed(recipies,3279312),"ore needed")
while result < cargo_hold:
    result = ore_needed(recipies,fuel)
    print(result,"ore needed for ",fuel," fuel")
    fuel = fuel * 2


fuel_low = int(fuel/4)
fuel_hi = int(fuel/2)
print("low",fuel_low)
print("high",fuel_hi)
delta = int((fuel_hi - fuel_low)/2)
fuel = fuel_low + delta
while (delta > 1):
    
    print("delta",delta)
    result = ore_needed(recipies,fuel)
    print(result,"ore needed for ",fuel," fuel")

    if (result < cargo_hold):
        fuel = fuel + delta
    
    if (result > cargo_hold):
        fuel = fuel - delta
    
    delta = int(delta/2)
    
    print("new delta",delta)

print(fuel)

while (result < cargo_hold):
    result = ore_needed(recipies,fuel)
    print(result,"ore needed for ",fuel," fuel")
    fuel = fuel + 1

print(fuel-2)

#3279311    
