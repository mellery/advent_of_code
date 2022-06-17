import threading

def get_digit(number, n):
        return number // 10**n % 10

class Intcode(threading.Thread):
    
    def __init__(self, commandstr):
        threading.Thread.__init__(self)
        self.commands = [int(i) for i in commandstr.split(',')]

        #add extra program memory
        for n in range(25000):
            self.commands.append(0)

        self.inputs = []
        self.outputs = []
        self.halted = False
        self.needInput = False

    def add_input(self, val):
        self.inputs.append(val)

    def wait_for_output(self):
        while len(self.outputs) == 0:
            wait = 0

    def run(self):
        
        rel_base = 0

        pc = 0
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
