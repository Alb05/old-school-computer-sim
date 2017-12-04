#!/usr/bin/env python3

import sys


class Computer:
    def __init__(self):
        self.a = 0
        self.memory = [""] * 256
        self.overflow = False

    def load(self, program):
        i = 0
        for instruction in program:
            self.memory[i] = instruction
            i += 1

    def argErr(self, line, arg):
        print("Invalid argument {0} on line {1}".format(arg, line))
        input()
        sys.exit()

    def LDA(self, addr):
        self.a = self.memory[addr]

    def ADD(self, addr):
        self.a += self.memory[addr]
        if (self.a > 255):
            self.overflow = True
            self.a = self.a % 256
        else:
            self.overflow = False

    def SUB(self, addr):
        self.a -= self.memory[addr]
        if (self.a < 0):
            self.overflow = True
            self.a = self.a % 256
        else:
            self.overflow = False

    def STA(self, addr):
        self.memory[addr] = self.a

    def OUT(self):
        print(self.a)

    def LDI(self, val):
        self.a = val


if __name__ == "__main__":
    comp = Computer()
    try:
        with open(sys.argv[1], "r") as f:
            comp.load(f.readlines())
            i = 0
            cond = True
            while (cond):
                i = i % 256
                instruction = comp.memory[i].upper().split(" ")

                if (instruction[0][:3] == "NOP"):
                    print("%d NOP" % (i))
                    i += 1

                elif (instruction[0][:3] == "LDA"):
                    comp.LDA(int(instruction[1]))
                    i += 1

                elif (instruction[0][:3] == "ADD"):
                    comp.ADD(int(instruction[1]))
                    i += 1

                elif (instruction[0][:3] == "SUB"):
                    comp.SUB(int(instruction[1]))
                    i += 1

                elif (instruction[0][:3] == "STA"):
                    comp.STA(int(instruction[1]))
                    i += 1

                elif (instruction[0][:3] == "OUT"):
                    comp.OUT()
                    i += 1

                elif (instruction[0][:3] == "JMP"):
                    i = int(instruction[1])

                elif (instruction[0][:3] == "LDI"):
                    comp.LDI(int(instruction[1]))
                    i += 1

                elif (instruction[0][:2] == "JC"):
                    if (comp.overflow):
                        i = int(instruction[1])
                    else:
                        i += 1

                elif (instruction[0][:3] == "HLT"):
                    cond = False
                    input()

                else:
                    print("Error on line {0} invalid command {1}".format(i, instruction[0]))
                    input()
                    sys.exit()

    except FileNotFoundError:
        if (sys.argv[1] is not None):
            print("File {0} not found".format(sys.argv[1]))
        else:
            print("You must enter a program")
        input()

    except ValueError:
        comp.argErr(i, instruction[1])

    except:
        print("There's an error")
        input()
