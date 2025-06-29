file1 = open('day2_input.txt', 'r') 
lines = file1.readlines() 

valid = 0
valid2 = 0
for l in lines:
    #print(l)
    temp = l.split(' ')
    low = int(temp[0].split('-')[0])
    high = int(temp[0].split('-')[1])
    p1 = low-1
    p2 = high-1
    ch = temp[1].split(':')[0]
    pwd = temp[2].split(':')[0]
    #print(low,high,ch,pwd)

    count = 0
    for c in pwd:
        if c == ch:
            count = count + 1
    if count >= low and count <= high:
        valid = valid + 1

    if pwd[p1] == ch and pwd[p2] != ch:
        valid2 = valid2 + 1
    if pwd[p2] == ch and pwd[p1] != ch:
        valid2 = valid2 + 1
    
print(valid)
print(valid2)