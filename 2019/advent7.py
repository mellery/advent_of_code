import itertools

from intcode import *

puzzle_input = "3,8,1001,8,10,8,105,1,0,0,21,34,59,68,85,102,183,264,345,426,99999,3,9,101,3,9,9,102,3,9,9,4,9,99,3,9,1002,9,4,9,1001,9,2,9,1002,9,2,9,101,5,9,9,102,5,9,9,4,9,99,3,9,1001,9,4,9,4,9,99,3,9,101,3,9,9,1002,9,2,9,1001,9,5,9,4,9,99,3,9,1002,9,3,9,1001,9,5,9,102,3,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99"

def day7p1():
    phases = list(itertools.permutations([0,1,2,3,4]))
    maxans = 0

    for phase in phases:
        ampA = Intcode(puzzle_input)
        ampB = Intcode(puzzle_input)
        ampC = Intcode(puzzle_input)
        ampD = Intcode(puzzle_input)
        ampE = Intcode(puzzle_input)

        ampA.add_input(phase[0])
        ampB.add_input(phase[1])
        ampC.add_input(phase[2])
        ampD.add_input(phase[3])
        ampE.add_input(phase[4])

        ampA.add_input(0)
        ampA.start()

        ampA.wait_for_output()
        ampB.add_input(ampA.outputs[0])
        ampB.start()

        ampB.wait_for_output()
        ampC.add_input(ampB.outputs[0])
        ampC.start()

        ampC.wait_for_output()
        ampD.add_input(ampC.outputs[0])
        ampD.start()

        ampD.wait_for_output()
        ampE.add_input(ampD.outputs[0])
        ampE.start()

        ampE.wait_for_output()

        if ampE.outputs[0] > maxans:
            maxans = ampE.outputs[0]
        
    return(maxans)

def day7p2():
    phases = list(itertools.permutations([5,6,7,8,9]))
    maxans = 0

    for phase in phases:
        print(phase)
        ampA = Intcode(puzzle_input)
        ampB = Intcode(puzzle_input)
        ampC = Intcode(puzzle_input)
        ampD = Intcode(puzzle_input)
        ampE = Intcode(puzzle_input)

        ampA.add_input(phase[0])
        ampB.add_input(phase[1])
        ampC.add_input(phase[2])
        ampD.add_input(phase[3])
        ampE.add_input(phase[4])

        dictB = {}

        ampA.add_input(0)

        ampA.start()
        ampB.start()
        ampC.start()
        ampD.start()
        ampE.start()

        tempAns = 0

        while(ampE.halted == False):
            
            ampA.wait_for_output()
            ampB.add_input(ampA.outputs[0])
            
            ampB.wait_for_output()
            ampC.add_input(ampB.outputs[0])
            
            ampC.wait_for_output()
            ampD.add_input(ampC.outputs[0])

            ampD.wait_for_output()
            ampE.add_input(ampD.outputs[0])
            
            ampE.wait_for_output()
            ampA.add_input(ampE.outputs[0])
            
            tempAns = ampE.outputs[0]
            
            ampA.outputs.pop()
            ampB.outputs.pop()
            ampC.outputs.pop()
            ampD.outputs.pop()
            ampE.outputs.pop()

        if tempAns > maxans:
            maxans = tempAns
        
    return(maxans)

print(day7p1())
print(day7p2())