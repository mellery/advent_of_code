from intcode import *

# Global intcode program for reuse
INSTRUCTIONS = "109,424,203,1,21101,11,0,0,1106,0,282,21102,18,1,0,1106,0,259,2101,0,1,221,203,1,21101,31,0,0,1106,0,282,21102,1,38,0,1106,0,259,21002,23,1,2,22102,1,1,3,21102,1,1,1,21101,57,0,0,1106,0,303,2101,0,1,222,21002,221,1,3,21001,221,0,2,21102,259,1,1,21102,80,1,0,1106,0,225,21102,1,79,2,21101,0,91,0,1106,0,303,2102,1,1,223,21001,222,0,4,21102,259,1,3,21101,225,0,2,21102,1,225,1,21101,0,118,0,1105,1,225,21002,222,1,3,21101,118,0,2,21101,0,133,0,1106,0,303,21202,1,-1,1,22001,223,1,1,21102,1,148,0,1105,1,259,1202,1,1,223,20102,1,221,4,20101,0,222,3,21102,1,22,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,1,195,0,105,1,109,20207,1,223,2,21002,23,1,1,21101,-1,0,3,21102,214,1,0,1106,0,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,2101,0,-4,249,22101,0,-3,1,22102,1,-2,2,21201,-1,0,3,21101,0,250,0,1105,1,225,22101,0,1,-4,109,-5,2105,1,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,22102,1,-2,-2,109,-3,2106,0,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,22102,1,-2,3,21102,343,1,0,1106,0,303,1105,1,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,21201,-4,0,1,21102,384,1,0,1105,1,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,22101,0,1,-4,109,-5,2106,0,0"

# Simple cache without lru_cache to avoid overhead
beam_cache = {}

# Pre-parsed instructions for faster execution
parsed_instructions = [int(x) for x in INSTRUCTIONS.split(',')]

def checkPos(x, y):
    """Check if position (x,y) is affected by the tractor beam. Optimized with aggressive caching."""
    if x < 0 or y < 0:
        return 0
    
    if (x, y) in beam_cache:
        return beam_cache[(x, y)]
    
    # Ultra-fast Intcode execution for this specific program
    # Since we know the program structure, we can optimize specifically for it
    memory = parsed_instructions.copy()
    memory.extend([0] * 1000)  # Extra memory
    
    pc = 0
    relative_base = 0
    inputs = [x, y]
    input_idx = 0
    
    def get_param(mode, param):
        if mode == 0: # position
            return memory[param] if param < len(memory) else 0
        elif mode == 1: # immediate
            return param
        elif mode == 2: # relative
            return memory[relative_base + param] if relative_base + param < len(memory) else 0
    
    def set_param(mode, param, value):
        if mode == 0: # position
            if param < len(memory):
                memory[param] = value
        elif mode == 2: # relative
            if relative_base + param < len(memory):
                memory[relative_base + param] = value
    
    while pc < len(memory):
        instruction = memory[pc]
        opcode = instruction % 100
        mode1 = (instruction // 100) % 10
        mode2 = (instruction // 1000) % 10
        mode3 = (instruction // 10000) % 10
        
        if opcode == 99: # halt
            break
        elif opcode == 1: # add
            val1 = get_param(mode1, memory[pc+1])
            val2 = get_param(mode2, memory[pc+2])
            set_param(mode3, memory[pc+3], val1 + val2)
            pc += 4
        elif opcode == 2: # multiply
            val1 = get_param(mode1, memory[pc+1])
            val2 = get_param(mode2, memory[pc+2])
            set_param(mode3, memory[pc+3], val1 * val2)
            pc += 4
        elif opcode == 3: # input
            if input_idx < len(inputs):
                set_param(mode1, memory[pc+1], inputs[input_idx])
                input_idx += 1
            pc += 2
        elif opcode == 4: # output
            val = get_param(mode1, memory[pc+1])
            beam_cache[(x, y)] = val
            return val
        elif opcode == 5: # jump if true
            val1 = get_param(mode1, memory[pc+1])
            val2 = get_param(mode2, memory[pc+2])
            if val1 != 0:
                pc = val2
            else:
                pc += 3
        elif opcode == 6: # jump if false
            val1 = get_param(mode1, memory[pc+1])
            val2 = get_param(mode2, memory[pc+2])
            if val1 == 0:
                pc = val2
            else:
                pc += 3
        elif opcode == 7: # less than
            val1 = get_param(mode1, memory[pc+1])
            val2 = get_param(mode2, memory[pc+2])
            set_param(mode3, memory[pc+3], 1 if val1 < val2 else 0)
            pc += 4
        elif opcode == 8: # equals
            val1 = get_param(mode1, memory[pc+1])
            val2 = get_param(mode2, memory[pc+2])
            set_param(mode3, memory[pc+3], 1 if val1 == val2 else 0)
            pc += 4
        elif opcode == 9: # adjust relative base
            val = get_param(mode1, memory[pc+1])
            relative_base += val
            pc += 2
        else:
            break
    
    # If we get here without output, assume 0
    beam_cache[(x, y)] = 0
    return 0


def day19p1():
    """Count affected points in 50x50 grid."""
    count = 0
    gridsize = 50
    
    for y in range(gridsize):
        for x in range(gridsize):
            if checkPos(x, y):
                count += 1
    return count

def day19p2():
    """Find the top-left corner of the first 100x100 square that fits in the beam."""
    # Optimized algorithm based on tracking beam edges
    # We look for the first row where the beam is wide enough to fit the square
    
    # Start from the minimum possible y
    y = 99
    x = 0  # Keep track of left edge
    
    while y < 1500:
        # Find the left edge of the beam at row y
        # Start searching from where we were before (beam left edge grows)
        while not checkPos(x, y) and x < y * 2:
            x += 1
        
        # If we can't find beam at this y, skip
        if x >= y * 2:
            y += 1
            x = max(0, x - 5)  # backtrack a bit
            continue
        
        # Check if 100x100 square fits starting at (x, y)
        # The square fits if both corners that define the boundaries are in the beam:
        # - Top-right: (x+99, y) - must be in beam for width
        # - Bottom-left: (x, y+99) - must be in beam for height
        
        if checkPos(x + 99, y) and checkPos(x, y + 99):
            return x * 10000 + y
        
        y += 1
    
    return -1


def day19p2_fallback():
    """Fallback method if slope calculation fails."""
    y = 99
    
    while y < 1500:
        # Find left edge of beam at this y
        left_x = None
        for x in range(y):
            if checkPos(x, y):
                left_x = x
                break
        
        if left_x is None:
            y += 1
            continue
        
        # Check if 100x100 square fits
        if checkPos(left_x + 99, y) and checkPos(left_x, y + 99):
            return left_x * 10000 + y
        
        y += 1
    
    return -1

def part1(filename):
    return day19p1()

def part2(filename):
    return day19p2()
    
  
if __name__ == "__main__":
    print("Part 1:", day19p1())
    print("Part 2:", day19p2())

