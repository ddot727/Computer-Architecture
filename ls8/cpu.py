"""CPU functionality."""
'''
Sprint Challenge

 Add the CMP instruction and equal flag to your LS-8.
# 10100111
# Equal flag = 0 unless a == b
 Add the JMP instruction.
# 01010100
 Add the JEQ and JNE instructions.
# 01010101 - JEQ
# 01010110 - JNE
 
 '''


import sys
ADD = 0b10100000
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
SP = 7
E = 0


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.branchtable = {}
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print(f"usage: {sys.argv[0]} filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    num = line.split('#', 1)[0]
                    if num.strip() == '':
                        continue
                    self.ram[address] = int(num, 2)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, address):
        # `ram_read()` should accept the address to read and return the value stored there.
        return (self.ram[address])

    def ram_write(self, value, address):
        # `raw_write()` should accept a value to write, and the address to write it to.

        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
            return self.register[reg_a]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
            return self.register[reg_a]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.register[SP] = 244
        self.running = True
        while self.running:

            IR = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            try:
                self.branchtable[IR](operand_a, operand_b)
            except:
                print(f"unknown intruction {IR}")
                sys.exit(1)

            # if IR == HLT:
            #     running = False
            #     self.pc += 1

            # elif IR == LDI:
            #     self.register[operand_a] = operand_b
            #     self.pc += 3

            # elif IR == PRN:
            #     print(self.register[operand_a])
            #     self.pc += 2

            # elif IR == MUL:
            #     self.alu('MUL', operand_a, operand_b)
            #     self.pc += 3

            # else:
            #     print(f"unknown intruction {IR}")
            #     sys.exit(1)

    def handle_HLT(self, a, b):
        self.running = False
        self.pc += 1

    def handle_LDI(self, a, b):
        self.register[a] = b
        self.pc += 3

    def handle_PRN(self, a, b):
        print(self.register[a])
        self.pc += 2

    def handle_MUL(self, a, b):
        self.alu('MUL', a, b)
        self.pc += 3

    def handle_PUSH(self, a, b):
        self.register[SP] -= 1
        value = self.register[a]
        self.ram[self.register[SP]] = value
        self.pc += 2

    def handle_POP(self, a, b):
        value = self.ram[self.register[SP]]
        self.register[a] = value
        self.register[SP] += 1
        self.pc += 2

    def handle_CALL(self, a, b):
        return_address = self.pc + 2
        self.register[SP] -= 1
        self.ram[self.register[SP]] = return_address
        subroutine_address = self.register[a]
        self.pc = subroutine_address

    def handle_RET(self, a, b):
        return_address = self.ram[self.register[SP]]
        self.register[SP] += 1
        self.pc = return_address

    def handle_ADD(self, a, b):
        self.alu('ADD', a, b)
        self.pc += 3
