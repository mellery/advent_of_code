import re

#filename = "day19_input.txt"
filename = "input19p2.txt"
#filename = "day19_ex1.txt"
#filename = "day19_ex2.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

rules = {}
messages = []
for l in lines:
    temp = l.strip()
    #print(temp)
    if ':' in temp:
        rules[int(temp.split(':')[0])] = temp.split(':')[1].strip()
    elif len(temp) > 1:
        messages.append(temp)

def contains_digit(rule):
    temp = rule.split(' ')
    for t in temp:
        if t.isdigit():
            return True
    return False

def substitute_rule(rule):
    temp = rule.split(' ')
    newrule = ""

    for t in temp:
        if t.isdigit():
            newrule = newrule + ' ( ' + rules[int(t)] + " ) "
        else:
            newrule = newrule + t
    newrule = newrule.replace('"','')
    newrule = newrule.replace("(a)",'a')
    newrule = newrule.replace("(b)",'b')
    newrule = newrule.replace("( a )",'a')
    newrule = newrule.replace("( b )",'b')
    newrule = newrule.replace("( b )",'b')
    return newrule


temp = rules[0]

#print(temp)

depth = 0
while contains_digit(temp) and depth < 100:
    temp = substitute_rule(temp)
    depth = depth + 1
    
temp = temp.replace(' ','')

print(temp)

count = 0

for m in messages:
    matchObj = re.search(temp,m)
    if matchObj:
        if len(m) == len(matchObj.group(0)):
            count = count + 1
            print(m)

print(count,"valid")