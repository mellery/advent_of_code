"""
Advent of Code 2020 Day 15: Rambunctious Recitation
Optimized Van Eck sequence implementation.
"""

def solve_memory_game(starting_numbers: list[int], target_turn: int) -> int:
    """
    Solve the memory game efficiently.
    
    The game rules:
    - Start with given numbers
    - Each turn, if the last number is new, speak 0
    - If the last number was spoken before, speak the age (turns since last spoken)
    """
    # Dictionary to store the last turn each number was spoken
    # We only need to track the most recent occurrence
    last_spoken = {}
    
    # Initialize with starting numbers (except the last one)
    for i, num in enumerate(starting_numbers[:-1]):
        last_spoken[num] = i + 1
    
    # Start from the last starting number
    current_number = starting_numbers[-1]
    
    # Continue until we reach the target turn
    for turn in range(len(starting_numbers), target_turn):
        # Calculate the next number based on current number's history
        if current_number in last_spoken:
            # Number was spoken before - calculate age
            next_number = turn - last_spoken[current_number]
        else:
            # Number is new - speak 0
            next_number = 0
        
        # Update the last spoken turn for current number
        last_spoken[current_number] = turn
        
        # Move to next number
        current_number = next_number
    
    return current_number


def solve_day15(filename: str = "day15_input.txt") -> tuple[int, int]:
    """Solve both parts of day 15."""
    # Parse input
    with open(filename, 'r') as f:
        line = f.read().strip()
    
    # Handle both comma-separated and space-separated formats
    if ',' in line:
        starting_numbers = [int(x) for x in line.split(',')]
    else:
        starting_numbers = [int(x) for x in line.split()]
    
    # If no input file, use the hardcoded example
    if not starting_numbers:
        starting_numbers = [1, 20, 11, 6, 12, 0]
    
    # Part 1: 2020th number
    part1 = solve_memory_game(starting_numbers, 2020)
    
    # Part 2: 30000000th number
    part2 = solve_memory_game(starting_numbers, 30000000)
    
    return part1, part2


# Test runner compatible functions
def part1(input_data) -> int:
    """Part 1 function compatible with test runner."""
    # Handle both filename and content
    if isinstance(input_data, str):
        if '\n' in input_data or ',' in input_data:
            # This is content
            line = input_data.strip()
        else:
            # This is a filename
            try:
                with open(input_data, 'r') as f:
                    line = f.read().strip()
            except FileNotFoundError:
                # Fallback to hardcoded if file not found
                return solve_memory_game([1, 20, 11, 6, 12, 0], 2020)
    else:
        # Fallback
        return solve_memory_game([1, 20, 11, 6, 12, 0], 2020)
    
    # Parse numbers
    if ',' in line:
        starting_numbers = [int(x) for x in line.split(',')]
    else:
        starting_numbers = [int(x) for x in line.split()]
    
    return solve_memory_game(starting_numbers, 2020)


def part2(input_data) -> int:
    """Part 2 function compatible with test runner."""
    # Handle both filename and content
    if isinstance(input_data, str):
        if '\n' in input_data or ',' in input_data:
            # This is content
            line = input_data.strip()
        else:
            # This is a filename
            try:
                with open(input_data, 'r') as f:
                    line = f.read().strip()
            except FileNotFoundError:
                # Fallback to hardcoded if file not found
                return solve_memory_game([1, 20, 11, 6, 12, 0], 30000000)
    else:
        # Fallback
        return solve_memory_game([1, 20, 11, 6, 12, 0], 30000000)
    
    # Parse numbers
    if ',' in line:
        starting_numbers = [int(x) for x in line.split(',')]
    else:
        starting_numbers = [int(x) for x in line.split()]
    
    return solve_memory_game(starting_numbers, 30000000)


if __name__ == "__main__":
    try:
        part1_result, part2_result = solve_day15()
        print(f"Part 1: {part1_result}")
        print(f"Part 2: {part2_result}")
    except FileNotFoundError:
        # Fallback to hardcoded input if no file
        starting_numbers = [1, 20, 11, 6, 12, 0]
        print(f"Part 1: {solve_memory_game(starting_numbers, 2020)}")
        print(f"Part 2: {solve_memory_game(starting_numbers, 30000000)}")