from os import remove


def get_lines(filename):
    with open(filename) as f:
        lines = f.readlines()
        return lines

def part1(filename):
    """
    Count how many times digits 1, 4, 7, or 8 appear in the output values.
    These digits have unique segment counts: 1=2, 4=4, 7=3, 8=7 segments.
    """
    lines = get_lines(filename)
    count = 0
    
    for line in lines:
        # Split input and output parts
        output_part = line.split('|')[1].strip()
        output_digits = output_part.split()
        
        # Count digits with unique segment counts
        for digit in output_digits:
            segment_count = len(digit)
            # Check if it's digit 1, 4, 7, or 8 based on segment count
            if segment_count in [2, 4, 3, 7]:  # 1, 4, 7, 8 respectively
                count += 1
    
    return count

def part2(filename):
        lines = get_lines(filename)

def main():
    #print(part1("day8_ex1.txt"))
    #print(part1("day8_ex1.txt"))
    print(part1("day8_input.txt"))

    #print(part2("day8_ex1.txt"))
    print(part2("day8_input.txt"))

if __name__ == "__main__":
    main()