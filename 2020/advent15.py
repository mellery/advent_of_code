def part1(numbers,stop):
    seen = {}
    for x in range(0,len(numbers)):
        seen[numbers[x]] = [x+1]
    
    turn = len(numbers)
    cur = numbers[-1]
    
    while(turn < stop):
        if cur not in seen:
            seen[cur] = [turn]
            cur = 0
        else:
            seen[cur].append(turn)
            if len(seen[cur]) > 2:
                seen[cur] = seen[cur][-2:]
            temp = seen[cur]
            diff = temp[::-1][0] - temp[::-1][1]
            
            cur = diff
        turn = turn + 1
        #if turn%10000 == 0:
            #print(stop-turn,"left")
    return cur

#print(part1([0,3,6],10))
#print(part1([0,3,6],2020))
#print(part1([1,3,2],2020))
#print(part1([2,1,3],2020))
#print(part1([1,2,3],2020))
#print(part1([2,3,1],2020))
#print(part1([3,2,1],2020))
#print(part1([3,1,2],2020))
#print(part1([1,20,11,6,12,0],2020))
print(part1([1,20,11,6,12,0],30000000))