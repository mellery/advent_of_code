def get_lines(filename):
    """Read and return all lines from the input file."""
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def remove_pairs(line):
    """Remove complete bracket pairs iteratively until no more can be removed."""
    pairs = ['()', '[]', '{}', '<>']
    prev_length = len(line)
    
    while True:
        for pair in pairs:
            line = line.replace(pair, '')
        
        # If no pairs were removed in this iteration, we're done
        if len(line) == prev_length:
            break
        prev_length = len(line)
    
    return line

def find_first_illegal_char(line):
    """Find the first illegal closing character in a corrupted line."""
    closing_chars = {')', ']', '}', '>'}
    for char in line:
        if char in closing_chars:
            return char
    return None

def part1(filename):
    """Find syntax errors (corrupted lines) and calculate error score."""
    lines = get_lines(filename)
    error_score = 0
    points = {')': 3, ']': 57, '}': 1197, '>': 25137}
    
    for line in lines:
        # Remove all complete pairs
        reduced = remove_pairs(line)
        
        # If there are closing characters left, the line is corrupted
        illegal_char = find_first_illegal_char(reduced)
        if illegal_char:
            error_score += points[illegal_char]
    
    return error_score

def part2(filename):
    """Find incomplete lines and calculate completion scores."""
    lines = get_lines(filename)
    scores = []
    points = {')': 1, ']': 2, '}': 3, '>': 4}
    close_map = {'(': ')', '[': ']', '{': '}', '<': '>'}
    
    for line in lines:
        # Remove all complete pairs
        reduced = remove_pairs(line)
        
        # If there are no closing characters, the line is incomplete
        if not any(char in reduced for char in ')]}>' ):
            # The remaining characters are unmatched opening brackets
            # We need to close them in reverse order
            completion = ''
            for char in reversed(reduced):
                if char in close_map:
                    completion += close_map[char]
            
            # Calculate score for this completion
            score = 0
            for char in completion:
                score = score * 5 + points[char]
            
            scores.append(score)
    
    # Return the middle score
    scores.sort()
    return scores[len(scores) // 2]

def main():
    day = '10'
    #print(part1(f"day{day}_ex1.txt"))
    #print(part1(f"day{day}_input.txt"))

    #print(part2(f"day{day}_ex1.txt"))
    print(part2(f"day{day}_input.txt"))

if __name__ == "__main__":
    main()