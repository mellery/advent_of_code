
filename = "day18_input.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

def sol_add_first(problem):
    
    while '+' in problem:
        #print(problem)
        values = problem.split(' ')
        #print(values)
        loc = values.index('+')
        #print(loc)
        #print(values[loc-1],values[loc],values[loc+1])
        sub = int(values[loc-1]) + int(values[loc+1])
        #print(sub)
        problem = problem.replace(values[loc-1] + ' ' + values[loc] + ' ' +values[loc+1], str(sub), 1)
        #print(problem)

    return solve_left_to_right(problem)

def solve_left_to_right(problem):
    #print(problem)
    values = problem.split(' ')
    ans = int(values[0])
    #print(ans)
    op = ''
    for v in values:
        if v.isdigit():
            n = int(v)
            if op == '+':
                ans = ans + n
            elif op == '*':
                ans = ans * n
        else:
            op = v
    return ans

def solve_part1(problem):
    while problem.count('(') > 0:
        
        rightpar = problem.find(')')
        inner = problem[:rightpar]
        leftpar = inner.rfind('(')
        inner = inner[leftpar+1:]
        ans = solve_left_to_right(inner)
        problem = problem.replace('('+inner+')',str(ans))
    
    return solve_left_to_right(problem)

def solve_part2(problem):
    while problem.count('(') > 0:
        #print(problem)
        rightpar = problem.find(')')
        inner = problem[:rightpar]
        leftpar = inner.rfind('(')
        inner = inner[leftpar+1:]
        ans = sol_add_first(inner)
        problem = problem.replace('('+inner+')',str(ans))
    
    return sol_add_first(problem)

#print(solve_part1('1 + 2 * 3 + 4 * 5 + 6')) #71
#print(solve_part1('1 + (2 * 3) + (4 * (5 + 6))')) #51
#print(solve_part1('2 * 3 + (4 * 5)')) #26
#print(solve_part1('5 + (8 * 3 + 9 + 3 * 4 * 3)')) #437
#print(solve_part1('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')) #12240
#print(solve_part1('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')) #13632

#print(solve_part2('1 + 2 * 3 + 4 * 5 + 6')) #231
#print(solve_part2('1 + (2 * 3) + (4 * (5 + 6))')) #51
#print(solve_part2('2 * 3 + (4 * 5)')) #46
#print(solve_part2('5 + (8 * 3 + 9 + 3 * 4 * 3)')) #1445
#print(solve_part2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')) #669060
#print(solve_part2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')) #23340

#print(solve_part2('(9 + 5 + 9 + 540) + 3')) #566

total = 0

for l in lines:
    ans = solve_part1(l.strip())
    total = total + ans
print(total)


total = 0

for l in lines:
    ans = solve_part2(l.strip())
    total = total + ans
print(total)

#68852578642795 too high