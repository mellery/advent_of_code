from collections import Counter

def get_list_of_numbers(filename):
    """Parse input file to get initial fish timer values."""
    with open(filename) as f:
        line = f.read().strip()
        return [int(x) for x in line.split(",")]

def simulate_fish(initial_fish, days):
    """
    Efficiently simulate lanternfish population using counter approach.
    
    Instead of tracking individual fish, we track how many fish have each timer value.
    This reduces the problem from exponential to linear time complexity.
    """
    # Count fish by their timer values (0-8)
    fish_count = Counter(initial_fish)
    
    for day in range(days):
        # Fish with timer 0 spawn new fish
        spawning_fish = fish_count[0]
        
        # Shift all timer values down by 1
        new_count = Counter()
        for timer in range(1, 9):
            new_count[timer - 1] = fish_count[timer]
        
        # Fish that spawned reset to timer 6
        new_count[6] += spawning_fish
        
        # New fish start with timer 8
        new_count[8] = spawning_fish
        
        fish_count = new_count
    
    return sum(fish_count.values())

def part1(filename):
    """Part 1: Simulate for 80 days."""
    fish = get_list_of_numbers(filename)
    result = simulate_fish(fish, 80)
    return result

def part2(filename):
    """Part 2: Simulate for 256 days."""
    fish = get_list_of_numbers(filename)
    result = simulate_fish(fish, 256)
    return result
        

def main():
    #print(part1("day6_ex1.txt"))
    #print(part1("day6_input.txt"))

    #print(part2("day6_ex1.txt"))
    print(part2("day6_input.txt"))

if __name__ == "__main__":
    main()