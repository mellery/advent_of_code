from intcode import *

# Global intcode program for reuse
INSTRUCTIONS = "109,424,203,1,21101,11,0,0,1106,0,282,21102,18,1,0,1106,0,259,2101,0,1,221,203,1,21101,31,0,0,1106,0,282,21102,1,38,0,1106,0,259,21002,23,1,2,22102,1,1,3,21102,1,1,1,21101,57,0,0,1106,0,303,2101,0,1,222,21002,221,1,3,21001,221,0,2,21102,259,1,1,21102,80,1,0,1106,0,225,21102,1,79,2,21101,0,91,0,1106,0,303,2102,1,1,223,21001,222,0,4,21102,259,1,3,21101,225,0,2,21102,1,225,1,21101,0,118,0,1105,1,225,21002,222,1,3,21101,118,0,2,21101,0,133,0,1106,0,303,21202,1,-1,1,22001,223,1,1,21102,1,148,0,1105,1,259,1202,1,1,223,20102,1,221,4,20101,0,222,3,21102,1,22,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,1,195,0,105,1,109,20207,1,223,2,21002,23,1,1,21101,-1,0,3,21102,214,1,0,1106,0,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,2101,0,-4,249,22101,0,-3,1,22102,1,-2,2,21201,-1,0,3,21101,0,250,0,1105,1,225,22101,0,1,-4,109,-5,2105,1,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,22102,1,-2,-2,109,-3,2106,0,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,22102,1,-2,3,21102,343,1,0,1106,0,303,1105,1,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,21201,-4,0,1,21102,384,1,0,1105,1,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,22101,0,1,-4,109,-5,2106,0,0"

# Simple cache without lru_cache to avoid overhead
beam_cache = {}

def checkPos(x, y):
    """Check if position (x,y) is affected by the tractor beam. Uses simple caching for efficiency."""
    if x < 0 or y < 0:
        return 0
    
    if (x, y) in beam_cache:
        return beam_cache[(x, y)]
    
    program = Intcode(INSTRUCTIONS)
    program.start()
    
    # Wait for first input request
    while not program.halted and not program.needInput:
        pass
    if program.halted:
        beam_cache[(x, y)] = 0
        return 0
        
    program.add_input(x)
    
    # Wait for second input request  
    while not program.halted and not program.needInput:
        pass
    if program.halted:
        beam_cache[(x, y)] = 0
        return 0
        
    program.add_input(y)
    program.wait_for_output()
    
    result = program.outputs[-1] if program.outputs else 0
    beam_cache[(x, y)] = result
    return result


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
    # Much simpler approach: scan y coordinates and use the original algorithm
    # but with smarter starting points
    
    # The beam follows predictable angles, so we can start at a reasonable Y
    y = 99  # Need at least y=99 to fit a 100-tall square
    x = 0
    
    while y < 1500:  # reasonable limit
        # For each y, find where the beam starts (left edge)
        # Start searching from a reasonable x based on previous iterations
        found_beam = False
        start_x = max(0, x - 5)  # start near the last known good x
        
        for test_x in range(start_x, start_x + y):  # beam grows with y
            if checkPos(test_x, y):
                x = test_x
                found_beam = True
                break
        
        if not found_beam:
            y += 1
            continue
        
        # Check if 100x100 square fits at (x, y)
        # Only need to check if top-right and bottom-left corners are in beam
        if checkPos(x + 99, y) and checkPos(x, y + 99):
            return x * 10000 + y
        
        y += 1
    
    return -1  # Not found

def part1(filename):
    return day19p1()

def part2(filename):
    return day19p2()
    
  
if __name__ == "__main__":
    print("Part 1:", day19p1())
    print("Part 2:", day19p2())

