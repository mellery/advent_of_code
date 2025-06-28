import threading
from typing import List, Optional, Union

def get_digit(number: int, n: int) -> int:
    """
    Get the nth digit from the right of a number (0-indexed).
    
    Args:
        number: The number to extract from
        n: Position from right (0 = rightmost)
        
    Returns:
        The digit at position n
    """
    return number // 10**n % 10

class Intcode(threading.Thread):
    """
    Intcode computer implementation with threading support.
    
    This class implements the Intcode computer from Advent of Code 2019,
    supporting all opcodes and parameter modes with threading capabilities
    for concurrent execution.
    """
    
    def __init__(self, commandstr: str):
        """
        Initialize the Intcode computer.
        
        Args:
            commandstr: Comma-separated string of integers representing the program
        """
        threading.Thread.__init__(self)
        self.commands: List[int] = [int(i) for i in commandstr.split(',')]

        # Add extra program memory
        for n in range(25000):
            self.commands.append(0)

        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.halted: bool = False
        self.needInput: bool = False

    def add_input(self, val: int) -> None:
        """
        Add an input value to the input queue.
        
        Args:
            val: Integer value to add to inputs
        """
        self.inputs.append(val)

    def wait_for_output(self) -> None:
        """
        Wait until an output is available.
        
        This method blocks until the computer produces at least one output.
        """
        while len(self.outputs) == 0:
            wait = 0

    def run(self) -> List[int]:
        """
        Execute the Intcode program.
        
        This method runs the Intcode program starting from position 0,
        processing opcodes until a halt instruction is encountered.
        
        Returns:
            List of output values produced by the program
        """
        rel_base: int = 0
        pc: int = 0
        while pc < len(self.commands):
            instr = self.commands[pc]
            op = get_digit(instr,1)*10 + get_digit(instr,0)
            mode1 = get_digit(instr,2)
            mode2 = get_digit(instr,3)
            mode3 = get_digit(instr,4)

            offset = 0
            if mode3 == 2:
                offset = rel_base

            if instr != 99:
                if mode1 == 1:
                    tempA = self.commands[pc+1]
                elif mode1 == 2:
                    tempA = self.commands[rel_base + self.commands[pc+1]]
                else:
                    tempA = self.commands[self.commands[pc+1]]
                
                if mode2 == 1:
                    tempB = self.commands[pc+2]
                elif mode2 == 2:
                    tempB = self.commands[rel_base + self.commands[pc+2]]
                else:
                    tempB = self.commands[self.commands[pc+2]]

            if op == 1: #ADD
                addr = self.commands[pc+3] + offset
                self.commands[addr] = tempA + tempB
                pc = pc + 4
            
            elif op == 2: #MULT
                addr = self.commands[pc+3] + offset
                self.commands[addr] = tempA * tempB
                pc = pc + 4
            
            elif op == 3: #INPUT
                while len(self.inputs) == 0:
                    self.needInput = True
                    wait = 0
                
                if mode1 == 2:
                    self.commands[self.commands[pc+1] + rel_base] = self.inputs[0]
                else:
                    self.commands[self.commands[pc+1]] = self.inputs[0]

                self.inputs.pop(0)
                pc = pc + 2
            
            elif op == 4: #OUTPUT
                self.outputs.append(tempA)
                pc = pc + 2
            
            elif op == 5: #JUMP-IF-TRUE
                if tempA != 0:
                    pc = tempB
                else:
                    pc = pc + 3

            elif op == 6: #JUMP-IF-FALSE
                if tempA == 0:
                    pc = tempB
                else:
                    pc = pc + 3

            elif op == 7: #LESS-THAN
                addr = self.commands[pc+3] + offset
                self.commands[addr] = int(tempA < tempB)
                pc = pc + 4

            elif op == 8: #EQUALS
                addr = self.commands[pc+3] + offset
                self.commands[addr] = int(tempA == tempB)
                pc = pc + 4                

            elif op == 9: #RELATIVE ADDRESS
                rel_base = rel_base + tempA
                pc = pc + 2
                
            elif op == 99: #HALT
                pc = len(self.commands)
                self.halted = True
                return self.outputs
            
            else:
                print("UNKNOWN:", op)
                pc = pc + 1
        
        return self.outputs       
