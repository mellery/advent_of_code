from math import floor
def get_lines(filename):
    with open(filename) as f:
        lines = f.readlines()
        return lines

def remove_chunck(l):
    l = l.replace('()','')
    l = l.replace('[]','')
    l = l.replace('{}','')
    l = l.replace('<>','')
    return l

def remove_openings(l):
    temp = l
    l = l.replace('(','')
    l = l.replace('[','')
    l = l.replace('{','')
    l = l.replace('<','')
    while temp != l:
        temp = l
        l = l.replace('(','')
        l = l.replace('[','')
        l = l.replace('{','')
        l = l.replace('<','')
    return temp

def part1(filename):
    lines = get_lines(filename)
    corrupted = []
    incomplete = []
    for l in lines:
        temp = l.strip()
        temp2 = remove_chunck(temp)
        while temp != temp2:
            temp = temp2
            temp2 = remove_chunck(temp)
        if '}' in temp or ')' in temp or ']' in temp or '>' in temp:
            corrupted.append(temp)
        else:
            incomplete.appen(temp)
    
    ans = []
    for c in corrupted:
        temp = remove_openings(c)
        ans.append(temp[0])
    score = ans.count(')') * 3 + ans.count(']') * 57 + ans.count('}') * 1197 + ans.count('>') * 25137
    return score

def part2(filename):
    lines = get_lines(filename)
    corrupted = []
    incomplete = []
    scores = []
    for l in lines:
        temp = l.strip()
        temp2 = remove_chunck(temp)
        while temp != temp2:
            temp = temp2
            temp2 = remove_chunck(temp)
        if '}' in temp or ')' in temp or ']' in temp or '>' in temp:
            corrupted.append(temp)
        else:
            incomplete.append(temp)
    for i in incomplete:
        score = 0
        i = i[::-1]
        i = i.replace('{','}')
        i = i.replace('[',']')
        i = i.replace('(',')')
        i = i.replace('<','>')

        for x in list(i):
            score *= 5
            if x == ')':
                score += 1
            if x == ']':
                score += 2
            if x == '}':
                score += 3
            if x == '>':
                score += 4
        #print(i,score)
        scores.append(score)
        

    scores.sort()
    mid = floor(len(scores)/2)
    print(scores[mid])

def main():
    day = '10'
    #print(part1(f"day{day}_ex1.txt"))
    #print(part1(f"day{day}_input.txt"))

    #print(part2(f"day{day}_ex1.txt"))
    print(part2(f"day{day}_input.txt"))

if __name__ == "__main__":
    main()