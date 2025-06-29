filename = "day14_input.txt"
#filename = "day14_ex1.txt"
#filename = "day14_ex2.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

registers = {}

def bitmask(mask,val):
    result = []
    newadrs = []
    for i in range(0,len(mask)):
        if mask[i] == 'X':
            result.append(val[i])
        else:
            result.append(mask[i])
    return "".join(result)

def findNthOccur(string , ch, N):
    occur = 0
    for i in range(len(string)):
        if (string[i] == ch):
            occur += 1
        if (occur == N):
            return i
    return -1

def part2(mask,val,mem):
    #result = []
    memstr = bin(int(mem)).split('b')[1]
    
    #print(memstr)
    mem = "0"*(masklen-len(memstr))+memstr
    #print("\naddress:\t",mem,int(mem,2))
    #print("mask:\t\t",mask)
    temp = list(mem)
    newregs = []
    for i in range(0,len(mask)):
        if mask[i] == '1':
            temp[i] = '1'
        elif mask[i] == 'X':
            temp[i] = 'X'
    ans = "".join(temp)
    #print(ans)
    newregs.append(ans)
    for m in newregs:
        floating = list(m).count('X')
        #print("\t\t",m,floating)
        for x in range(0,2**floating):
            combo = list('0'*(floating-len(bin(x).split('b')[1]))+bin(x).split('b')[1])
            #print(m,val)
            newreg = m
            #print(floating)
            tempreg = list(newreg)
            for y in range(0,floating):
                
                pos = findNthOccur(newreg,'X',y+1)
                #print(len(tempreg),y,pos,"set",tempreg[pos],"to",val[y])
                tempreg[pos] = combo[y]
            ans = int("".join(tempreg),2)
            #print("".join(tempreg),ans)
            registers[ans] = val

    #print(newregs)


for l in lines:
    temp = l.strip()
    if 'mask' in temp:
        mask = temp.split('=')[1].strip()
        masklen = len(mask)
        #print("\nmask = ",mask)
    else:
        
        val = bin(int(temp.split('=')[1])).split('b')[1]
        val = "0"*(masklen-len(val))+val
        #print(valt)

        reg = temp.split(']')[0].split('[')[1]
        #print('[',reg,']')
        #print('value:\t',val)
        #print('mask:\t',mask)
        
        part2(mask,val,reg)

        #ans = bitmask(mask,val)
        #registers[reg] = ans
        
        #print('result:\t',ans,int(ans,2))
        
#print(registers)

total = 0
for r,v in registers.items():
    total = total + int(v,2)
    #print("reg",r,"=",int(v,2))

print("total = ",total)
