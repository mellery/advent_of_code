from collections import Counter

def get_list_of_numbers(filename):
    with open(filename) as f:
        lines = f.readlines()
        numbers = []
        for l in lines:
            temp = l.split(",")
            for t in temp:
                numbers.append(int(t))
            
    return numbers

def update_fish(fish):
    new_fish = 0
    for i in range(0,len(fish)):
        fish[i] -= 1
        if fish[i] < 0:
            fish[i] = 6
            new_fish +=1
    for i in range(0,new_fish):
        fish.append(8)
    return(fish)



def part1(filename):
        fish = get_list_of_numbers(filename)
        days = 256
        for x in range(0,days):
            print("day",x)
            fish = update_fish(fish)
        print(len(fish))


def part2(filename):
        fish = get_list_of_numbers(filename)

        fish = Counter(fish)

        for i in range(256):
            spawn = fish[0]
            for i in range(8):
                fish[i] = fish[i+1]
            fish[8] = spawn
            fish[6] += spawn

        print(sum(fish.values()))
        

def main():
    #print(part1("day6_ex1.txt"))
    #print(part1("day6_input.txt"))

    #print(part2("day6_ex1.txt"))
    print(part2("day6_input.txt"))

if __name__ == "__main__":
    main()