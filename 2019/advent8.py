image = "123456789012"

temp = open("day8_input.txt").read().splitlines()
image = temp[0]

#image = "0222112222120000"
rows = 2
cols = 2

cols = 25
rows = 6
size = len(image)
lsize = cols*rows
print(size)
layers = []
for p in range(0,size,lsize):
    #print(p)
    layers.append(image[p:p+lsize])
    #print(layers[-1],"zeroes",layers[-1].count('0'), "ones",layers[-1].count('1'), "twos",layers[-1].count('2'))

toplayer = [' ']*lsize

#print(len(layers))
for l in layers:
    #print("layer")
    #print(l,toplayer)
    for x in range(0,lsize):
        #print(x,"l",l[x],"o",toplayer[x])
        if l[x] != '2' and toplayer[x] == ' ':
            print("set pixel ",x," to ", l[x])
            toplayer[x] = l[x]
            #print("".join(toplayer))

print("output")
print(toplayer)
for p in range(0,rows):
        #print(toplayer[p:p+cols])
        temp = "".join(toplayer[p:p+cols])
        print(temp)