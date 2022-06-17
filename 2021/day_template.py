def get_list_of_numbers(filename):
    with open(filename) as f:
        lines = f.readlines()
        numbers = []
        for l in lines:
            number = int(l)
            numbers.append(number)
    return numbers

def part1(filename):
        numbers = get_list_of_numbers(filename)
        last_number = numbers[0]
        increases = 0

        for n in numbers[1:]:
            if n > last_number:
                increases += 1
            last_number = n
        return(increases)

def part2(filename):
        numbers = get_list_of_numbers(filename)
        last_number = numbers[0]+numbers[1]+numbers[2]
        increases = 0

        for i in range(1,len(numbers)-2):
            nsum = numbers[i]+numbers[i+1]+numbers[i+2]
            if nsum > last_number:
                increases += 1
            last_number = nsum
        return(increases)

def main():
    day = 'x'
    print(part1(f"day{day}_ex1.txt"))
    #print(part1(f"day{day}_input.txt"))

    #print(part2(f"day{day}_ex1.txt"))
    #print(part2(f"day{day}_input.txt"))

if __name__ == "__main__":
    main()