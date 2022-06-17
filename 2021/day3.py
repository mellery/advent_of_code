def get_binary_numbers(filename):
    with open(filename) as f:
        lines = f.readlines()
        numbers = []
        commands = []
        for l in lines:
            numbers.append(l.strip())

        return numbers

def get_most_common_bit(binary_numbers,index):
    one_count = 0
    zero_count = 0
    for b in binary_numbers:
        if int(b[index]) == 1:
            one_count += 1
        else:
            zero_count += 1
    if one_count >= zero_count:
        return 1
    else:
        return 0

def part1(filename):
    binary_numbers = get_binary_numbers(filename)
    gamma = []
    epsilon = []
    for i in range(0,len(binary_numbers[0])):
        
        if get_most_common_bit(binary_numbers,i):
            gamma.append(str(1))
            epsilon.append(str(0))
        else:
            gamma.append(str(0))
            epsilon.append(str(1))
    
    gamma_int = int("".join(gamma),2)
    epsilon_int = int("".join(epsilon),2)
    print("gamma",gamma_int)
    print("epsilon", epsilon_int)
    return(gamma_int*epsilon_int)
        
        
def part2(filename):
    binary_numbers = get_binary_numbers(filename)
    for i in range(0,len(binary_numbers[0])):
        keep = str(get_most_common_bit(binary_numbers,i))
        new_list = binary_numbers.copy()
        for b in binary_numbers:
            if b[i] != keep:
                new_list.remove(b)
        binary_numbers = new_list.copy()
    oxygen_int = int(binary_numbers[0],2)

    binary_numbers = get_binary_numbers(filename)
    #print(binary_numbers)
    for i in range(0,len(binary_numbers[0])):
        keep = str(get_most_common_bit(binary_numbers,i))
        
        if keep == "1":
            keep = "0"
        elif keep == "0":
            keep = "1"
        #print("---keep",keep)
        new_list = binary_numbers.copy()
        if len(new_list) > 1:
            for b in binary_numbers:
                if str(b[i]) != str(keep):
                    #print("remove",b[i],keep,b)
                    new_list.remove(b)
        binary_numbers = new_list.copy()

    co2_int = int(binary_numbers[0],2)
    print(f"o = {oxygen_int} co2 = {co2_int}")
    return oxygen_int * co2_int


def main():
    #print(part1("day3_ex1.txt"))
    #print(part1("day3_input.txt"))

    #print(part2("day3_ex1.txt"))
    print(part2("day3_input.txt"))

if __name__ == "__main__":
    main()