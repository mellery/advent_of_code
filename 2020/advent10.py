import itertools
import math

filename = "input10.txt"
#filename = "input10_ex1.txt"
#filename = "input10_ex2.txt"
file1 = open(filename, 'r') 
lines = file1.readlines() 

nums = []
for l in lines:
    nums.append(int(l))

nums.sort()
nums.append(max(nums)+3)
#print(nums)


ones = 0
twos = 0
threes = 0
musts = []
opts = []

diff  = nums[0]
if diff == 1:
    ones = ones + 1
if diff == 2:
    twos = twos + 1
if diff == 3:
    threes = threes + 1

groups = 0

temp = nums.copy()
new_nums = nums.copy()

nums = new_nums.copy()
#print(nums)


for x in range(1,len(nums)):
    diff = nums[x]-nums[x-1]

    if diff == 1:
        ones = ones + 1
    if diff == 2:
        twos = twos + 1
    if diff == 3:
        threes = threes + 1
        musts.append(nums[x])
        #print("must have ",nums[x])

for x in nums:
    if x not in musts:
        opts.append(x)

opts.sort()

temp = opts.copy()

for x in range(0,len(temp)-1):
    if temp[x+1]-temp[x] > 3:
        #print("must have ",temp[x])
        musts.append(temp[x])
        opts.remove(temp[x])

#groups = 0

musts.sort()
opts.sort()

temp = opts.copy()
for x in range(0,len(temp)-3):
    if temp[x] == temp[x+1]-1 == temp[x+2]-2:
        opts.remove(temp[x+1])
        opts.remove(temp[x+2])
        print("removed",temp[x+1],temp[x+2])
        groups = groups + 1

pairs = 0

for m in musts:
    if m+1 in opts and m+2 in opts:
        opts.remove(m+1)
        opts.remove(m+2)
        print("removed",m+1,m+2)
        pairs = pairs + 1



print("ones = ",ones)
#print("twos = ",twos)
print("threes = ",threes)

print("musts",musts)
print("opts",opts)

print(ones*threes)

valid = 0

floor = math.floor(len(nums)/3)
print("len nums = ",len(nums),"floor",floor)

for L in range(0, len(opts)+1):
    
    for subset in itertools.combinations(opts, L):
        temp = list(subset)+musts
        temp.sort()
        works = True
        
        if len(temp) == 0:
            works = False
        elif temp[len(temp)-1] != max(nums):
            works = False
        elif temp[0] > 3:
            works = False
        else:
            for x in range(1,len(temp)):
                if temp[x] - temp[x-1] > 3:
                    works = False
                    break
        if works == True:
            valid = valid + 1           
                
print(valid,"combos")

print(valid*(7**groups)*(4**pairs))
