import re

def parse_input(filename):
    try:
        with open(filename, 'r') as file1:
            lines = file1.readlines()
    except FileNotFoundError:
        # Try alternative filenames
        try:
            with open("day19_input.txt", 'r') as file1:
                lines = file1.readlines()
        except FileNotFoundError:
            return {}, []
    
    rules = {}
    messages = []
    for l in lines:
        temp = l.strip()
        if ':' in temp:
            rules[int(temp.split(':')[0])] = temp.split(':')[1].strip()
        elif len(temp) > 1:
            messages.append(temp)
    return rules, messages

def contains_digit(rule):
    temp = rule.split(' ')
    for t in temp:
        if t.isdigit():
            return True
    return False

def substitute_rule(rule, rules):
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


def solve_part1(rules, messages):
    if not rules:
        return 0
        
    temp = rules[0]
    depth = 0
    while contains_digit(temp) and depth < 100:
        temp = substitute_rule(temp, rules)
        depth = depth + 1
        
    temp = temp.replace(' ','')
    count = 0
    
    for m in messages:
        matchObj = re.search(temp,m)
        if matchObj:
            if len(m) == len(matchObj.group(0)):
                count = count + 1
    
    return count

def part1(filename):
    rules, messages = parse_input(filename)
    return solve_part1(rules, messages)

def part2(filename):
    return "Not implemented"

if __name__ == "__main__":
    rules, messages = parse_input("day19_input.txt")
    result = solve_part1(rules, messages)
    print(result, "valid")