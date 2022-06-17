def get_instructions(filename):
    with open(filename) as f:
        lines = f.readlines()
        numbers = []
        commands = []
        for l in lines:
            commands.append(l.split(' ')[0])
            numbers.append(int(l.split(' ')[1].strip()))

        return commands, numbers

def part1(filename):
    horizontal = 0
    depth = 0
    commands, numbers = get_instructions(filename)
    for i in range(0,len(commands)):
        if commands[i] == 'forward':
            horizontal += numbers[i]
        if commands[i] == 'down':
            depth += numbers[i]
        if commands[i] == 'up':
            depth -= numbers[i]
    print(f"horizontal positionn = {horizontal} depth = {depth}")
    return horizontal*depth
        
def part2(filename):
    horizontal = 0
    depth = 0
    aim = 0

    commands, numbers = get_instructions(filename)
    for i in range(0,len(commands)):
        if commands[i] == 'forward':
            horizontal += numbers[i]
            depth += numbers[i]*aim
        if commands[i] == 'down':
            aim += numbers[i]
        if commands[i] == 'up':
            aim -= numbers[i]
    print(f"horizontal positionn = {horizontal} depth = {depth} aim = {aim}")
    return horizontal*depth

def main():
    #print(part1("day2_ex1.txt"))
    #print(part1("day2_input.txt"))

    #print(part2("day2_ex1.txt"))
    print(part2("day2_input.txt"))

if __name__ == "__main__":
    main()