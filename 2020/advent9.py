filename = "input9.txt"
#filename = "input9_ex.txt"
file1 = open(filename, 'r') 
lines = file1.readlines() 



def is_valid(preamble,val):
    for x in preamble:
        for y in preamble:
            if (x != y):
                #print(x,y,x+y)
                if (x+y == val):
                    return True
    return False


prelen = 25
preamble = []
for x in range(1,prelen+1):
    preamble.append(x)

#for x in preamble:
#    print(x)

#print(is_valid(preamble,26))
#print(is_valid(preamble,49))
#print(is_valid(preamble,100))
#print(is_valid(preamble,50))

stream = []
for l in lines:
    stream.append(int(l))

prelen = 25
#print(stream)

for x in range(prelen,len(stream)):
    val = stream[x]
    preamble = []
    for y in range(0,prelen):
        preamble.append(stream[x+y-prelen])
    
    if is_valid(preamble,stream[x]) == False:
        print(stream[x])
        break

ans = 373803594


for x in range(0,len(stream)):
    temp = 0
    loc = x
    while temp < ans:
        temp = temp + stream[loc]
        loc = loc + 1
    if temp == ans:
        #print(temp==ans,temp, "start",x,"end",loc)
        sol = []
        for y in range(x,loc):
            sol.append(stream[y])
            #print(y,stream[y])
        print(min(sol)+max(sol))
        break

