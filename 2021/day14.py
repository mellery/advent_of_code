def load_pairs(filename):

    with open(filename) as f:
        lines = f.readlines()
        i = 0
        poly = {}
        for l in lines:
            if i == 0:
                template = l.strip()
            else:
                if "->" in l:
                    temp = l.split("->")
                    poly[temp[0].strip()] = temp[1].strip()
            i += 1

    return template, poly

def insert(template, poly):
    result = ""
    for i in range(0,len(template)-1):
        result += template[i]
        result += poly[template[i:i+2]]
        #result += template[i+1]
        #print(template[i:i+2])
    result += template[-1]
    return result

def updatepairs(pairs,poly):
    newpairs = {}
    for p in pairs:
        #print(p,poly[p],p[0])
        n = p[0]+poly[p]
        if n in newpairs:
            newpairs[n] += pairs[p]
        else:
            newpairs[n] = pairs[p]
        n = poly[p]+p[1]
        if n in newpairs:
            newpairs[n] += pairs[p]
        else:
            newpairs[n] = pairs[p]
    return newpairs

def builddict(template):
    pairs = {}
    for i in range(0,len(template)-1):
        p =  template[i:i+2]
        if p in pairs:
            pairs[p] += 1
        else:
            pairs[p] = 1
    return pairs

def part1(filename):
    
    template, poly = load_pairs(filename)
    pairs = builddict(template)
    #print(pairs)

    steps = 40
    for i in range(0,steps):
        pairs = updatepairs(pairs,poly)
        
        letters = []
        counts = {}
        for k,v in pairs.items():
            if k[0] not in letters:
                letters.append(k[0])
            if k[1] not in letters:
                letters.append(k[1])

            for x in letters:
                if x in k[0]:
                    if x in counts:
                        counts[x] += v
                    else:
                        counts[x] = v
        counts[template[-1]] += 1

        max_key = max(counts, key=counts.get)
        min_key = min(counts, key=counts.get)

        print(counts[max_key]-counts[min_key])

        #print(i+1,counts)
  

#part1('day14_ex1.txt')
part1('day14_input.txt')