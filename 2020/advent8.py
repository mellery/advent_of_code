
filename = "input8.txt"
#filename = "input8_ex.txt"
file1 = open(filename, 'r') 
lines = file1.readlines() 

pc = 0
acc = 0

visited = []

instructions = []

jmps = []
nops = []

for l in lines:
    temp = l.strip()
    ins = temp.split(' ')[0]
    val = int(temp.split(' ')[1])
    instructions.append([ins,val])

    if (ins == 'jmp'):
        jmps.append(len(instructions)-1)
    if (ins == 'nop'):
        nops.append(len(instructions)-1)

#print("jmps",jmps)
#print("nops",nops)

for x in jmps:
    pc = 0
    acc = 0
    visited = []

    halted = False

    while pc < len(instructions):

        if(pc == x):
            ins = 'nop'
        else:
            ins = instructions[pc][0]
        val = instructions[pc][1]
        #print("[",pc,"]",ins,val,'\t',acc)

        if ins == 'acc':
            acc = acc + val
            pc = pc + 1
        elif ins == 'jmp':
            pc = pc + val
        elif ins == 'nop':
            pc = pc + 1

        if pc not in visited:
            visited.append(pc)
        else:
            #print('replacing jmp at',x,'causes infinite loop!')
            halted = True
            break

    if halted == False:        
        print(acc)

for x in nops:
    pc = 0
    acc = 0
    visited = []

    halted = False

    #print('replacing nop at',x)
    while pc < len(instructions):

        if(pc == x):
            ins = 'jmp'
        else:
            ins = instructions[pc][0]
        val = instructions[pc][1]
        #print("[",pc,"]",ins,val,'\t',acc)

        if ins == 'acc':
            acc = acc + val
            pc = pc + 1
        elif ins == 'jmp':
            pc = pc + val
        elif ins == 'nop':
            pc = pc + 1

        if pc not in visited:
            visited.append(pc)
        else:
            #print('replacing nop at',x,'causes infinite loop!')
            halted = True
            break

    if halted == False:        
        print(acc)