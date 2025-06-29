
filename = "day21_input.txt"
#filename = "day21_ex1.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

def count_safe(safe):
    total = 0

    for f in food_label:
        for s in safe:
            zk_line = f.split(' ')
            zk_line.sort()
            if s in zk_line:
                total = total + 1
         
    return total

ingrediants = {}
recipies = []
all_allergens = []
food_label = {}

for l in lines:
    temp = l.strip()
    foods = temp.split('(')[0].strip().split(" ")
    recipies.append(foods)
    allergens = temp.split('(contains ')[1][0:-1].split(',')

    food_label[temp.split('(')[0].strip()] = allergens

    for f in foods:
        ingrediants[f] = []
        for a in allergens:
            temp = a.strip()
            if temp not in all_allergens:
                all_allergens.append(temp)
            ingrediants[f].append(temp)

for k in ingrediants:
    ingrediants[k] = all_allergens.copy()
    #print("ingrediant",k,"might contain",ingrediants[k])

for k in ingrediants:
    for f in food_label:
        parts = f.split()
        if k not in parts:# and len(food_label[f]) == 1:
            for i in food_label[f]:
                temp = i.strip()
                if temp in ingrediants[k]:
                    ingrediants[k].remove(temp)
    
#print("")
safe = []
for k in ingrediants:
    #print(k,ingrediants[k])
    if len(ingrediants[k]) == 0:
        safe.append(k)

#print("SAFE")
#print(safe)



allergens = []

#print all recipies after removing safe ingrediants
print("")
#safe = []
for k in ingrediants:
    if len(ingrediants[k]) > 0:
        print(k,ingrediants[k])
    if len(ingrediants[k]) == 1:
        allergens.append((k,ingrediants[k][0]))
    

safe.sort()
#print("\nSAFE",safe)
print("\nNOT SAFE",allergens)

#figured out remaining allergans manually for part 2
#nfnfk	'dairy'
#nbgklf	'eggs'
#clvr 	'fish'
#fttbhdr	'nuts'
#qjxxpr 	'peanuts'
#hdsm 	'sesame'
#sjhds 	'soy'
#xchzh 	'wheat'

print(count_safe(safe))
print('nfnfk,nbgklf,clvr,fttbhdr,qjxxpr,hdsm,sjhds,xchzh')