filename = "input6.txt"
#filename = "input6_ex.txt"
file1 = open(filename, 'r') 
lines = file1.readlines() 

total = 0
group = []

for l in lines:

    ans = l.strip()
    
    if len(ans) == 0:
        every = []
        
        for x in group[0]:
            numfound = 0
            for y in range(0,len(group)):
                if x in group[y]:
                    numfound = numfound+1
            if numfound == len(group):
                every.append(x)

        total = total + len(every)
        group = []
        
    else:
        p = []
        for c in ans:
            p.append(c)
        group.append(p)

print(total)

