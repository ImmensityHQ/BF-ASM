# Programmatically controllable BF interpreter

class Interpreter:
    def __init__(self, mem: list, pointer: int) -> None:
        self.mem = mem  # memory
        self.pointer = pointer

        self.output = ""

    def set_cell(self, cell, integer):
        self.mem[cell] = integer

    def add(self, amount=1):
        self.mem[self.pointer] += amount

        while self.mem[self.pointer] > 255:  # TODO: optimize this and verify it is correct
            self.mem[self.pointer] = self.mem[self.pointer] - 256

    def sub(self, amount=1):
        self.mem[self.pointer] -= amount

        while self.mem[self.pointer] < 0:  # TODO: optimize this and verify it is correct
            self.mem[self.pointer] = self.mem[self.pointer] + 256

    def mov(self, amount=1):
        self.pointer += amount

        if self.pointer < 0:
            self.pointer = 0

    def dump(self):
        self.output += chr(self.mem[self.pointer])

    def interp_short(self, program, inputs=[]):
        # program counter is not needed, since loops aren't handled in this class
        in_idx = 0  # keep track of where we are in the input

        for char in program:
            match char:
                case "+":
                    self.add()
                case "-":
                    self.sub()
                case "<":
                    self.mov(-1)
                case ">":
                    self.mov(1)
                case ".":
                    self.dump()
                case ",":
                    # TODO: catch input not being within 0-255 range
                    self.mem[self.pointer] = inputs[in_idx]
                    in_idx += 1


def main():
    interp = Interpreter([0], 0)
    interp.add(60000)
    print(interp.mem)


if __name__ == "__main__":
    main()
