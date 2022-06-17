filename = "input13.txt"
#filename = "input13_ex1.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

for l in lines:
    temp = l.strip()
    print(temp)

time = int(lines[0])
buses = lines[1].split(',')


def bus_dept(ts,bus):
    if ts%int(bus) == 0:
        return True
    else:
        return False

t = time
found = False
while found == False:
    for b in buses:
        if b != 'x':
            if bus_dept(t,b):
                print(t,b,time%int(b))
                print("wait",t-time,'minutes')
                print(int(b)*(t-time))
                found = True
    t = t + 1

def part2(buses):
    available = list(map(lambda x: x if x=='x' else int(x), buses))
    idmap = {key:val for val, key in filter(lambda x: x[1]!='x', enumerate(available))}
    idlist = [id for id in idmap]

    #print(available)
    #print(idmap)
    #print(idlist)

    start, step = 0, 1
    for id, delta in idmap.items():
        #print("starting at ",start)
        for time in range(start, step * id, step):
            if (time + delta) % id == 0:
                step *= id
                #print("step now",step)
                start = time
    return start


temp = lines[1].split(',')
buses = []
for t in temp:
    if t != 'x':
        buses.append(int(t))
    else:
        buses.append(t)

x = 'x'
print('---')
print(part2([17,x,13,19])) #3417

print(part2([67,7,59,61])) #754018

print(part2([67,x,7,59,61])) #779210

print(part2([67,7,x,59,61])) #1261476

print(part2([1789,37,47,1889])) #1202161486

print(part2([13,x,x,41,x,x,x,x,x,x,x,x,x,641,x,x,x,x,x,x,x,x,x,x,x,19,x,x,x,x,17,x,x,x,x,x,x,x,x,x,x,x,29,x,661,x,x,x,x,x,37,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,23]))
