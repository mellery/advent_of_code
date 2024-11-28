def get_first_digit(line):
    for i, c in enumerate(line):
        if c.isdigit():
            return c


digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def replace_first_word(line, rev=False):
    for x in range(0, len(line)):
        if line[x].isdigit():
            if rev:
                line = line[::-1]
            return line
        temp = line[x:]
        for i, d in enumerate(digits):
            w = d
            if rev:
                w = d[::-1]
            if temp.startswith(w):
                line = line.replace(w, str(i+1))
                if rev:
                    line = line[::-1]
                return line
    if rev:
        line = line[::-1]
    return line


def part1():
    total = 0
    with open(infile, 'r') as file:
        for line in file:
            a = get_first_digit(line)
            b = get_first_digit(line[::-1])
            v = int(a+b)
            # print(v)
            total += v
    print(total)


def part2(infile):
    total = 0
    with open(infile, 'r') as file:
        for line in file:
            temp = line
            line = replace_first_word(line)
            a = get_first_digit(line)

            line = replace_first_word(temp[::-1], rev=True)
            b = get_first_digit(line[::-1])
            v = int(a+b)

            total += v
        print(total)


# infile = 'test.txt'
# infile = 'test2.txt'
infile = 'part1.txt'

# part1(infile)
part2(infile)

# line = '9qb95oneightsf'
# newline = replace_first_word(line[::-1],rev=True)
# print(line, newline)
