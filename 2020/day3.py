def find_trees(filename, run, rise):

    file1 = open(filename, 'r') 
    lines = file1.readlines() 

    rows = len(lines)

    cur_x = 0
    cur_y = 0
    trees = 0

    for i in range(0,len(lines)):
        lines[i] = lines[i].strip() * run * rows

    while (cur_y < rows-rise):

        cur_x = cur_x + run
        cur_y = cur_y + rise

        if (lines[cur_y][cur_x] == '#'):
            trees = trees + 1

    print("found ",trees," trees")
    return trees


#filename = 'day3_ex.txt'
filename = 'day3_input.txt'

rise = 1
run = 3

a1 = find_trees(filename, 1, 1)
a2 = find_trees(filename, 3, 1)
a3 = find_trees(filename, 5, 1)
a4 = find_trees(filename, 7, 1)
a5 = find_trees(filename, 1, 2)
print(a1*a2*a3*a4*a5)