class CodeGenerator:
    '''Naive code generator for common BF operations.'''

    def __init__(self):
        self.sp = 0

    def generate(self, funcs):
        '''Generate a list of codegen functions.'''
        res = ""
        for func in funcs:
            res += func
        return res

    def op(self, command: str, amount: int) -> str:
        return command * amount

    def add(self, amount: int = 1) -> str:
        '''Generate BF code to add an integer to the current cell.'''
        return self.op("+", amount)

    def sub(self, amount: int = 1) -> str:
        '''Generate BF code to subtract an integer from the current cell.'''
        return self.op("-", amount)

    def set_cur(self, integer: int) -> str:
        '''Generate BF code to set current cell to an integer.'''
        return "[-]" + self.add(integer)

    def goto_relative(self, amount: int) -> str:
        '''Generate BF code to goto a cell, relative to the current cell.'''
        self.sp += amount
        if 0 < amount:
            return self.op(">", amount)
        else:
            if self.sp < 0:
                self.sp = 0

            return self.op("<", abs(amount))

    def goto(self, address: int) -> str:
        '''Generate BF code to goto a cell.'''
        if self.sp < address:
            return self.goto_relative(abs(address - self.sp))
        elif self.sp > address:
            return self.goto_relative(-abs(address - self.sp))
        else:
            return ""

    def add_addr(self, amount: int, address: int) -> str:
        '''Generate BF code to add an integer to an address.'''
        return self.goto(address) + self.add(amount)

    def sub_addr(self, amount: int, address: int) -> str:
        '''Generate BF code to subtract an integer from an address.'''
        return self.goto(address) + self.sub(amount)

    def set_addr(self, integer: int, address: int) -> str:
        '''Generate BF code to set an address to an integer.'''
        return self.goto(address) + self.set_cur(integer)

    def input_addr(self, address: int) -> str:
        return self.goto(address) + ","

    def dump_addr(self, address: int) -> str:
        return self.goto(address) + "."

    def dump_array(self, addrs: list[int]):
        '''Dump all addresses in a list of addresses.'''
        code = ""
        for addr in addrs:
            code += self.goto(addr) + "."
        return code

    def loop(self, code) -> str:
        '''Surround some BF code in a loop.'''
        if isinstance(code, str):
            return f"[{code}]"

        # list of code generator functions [add(), goto(), etc.]
        elif isinstance(code, list):
            return f"[{self.generate(code)}]"


class Optimizer:
    def __init__(self, program) -> None:
        self.program = program

        self.pc = 0
        self.cur_chunk = ""
        self.next_chunk = ""

    def peek_next(self):
        return self.program[self.pc + 1]

    def get_next_chunk(self):
        if self.pc > len(self.program) - 1:
            return None

        next_chunk = ""
        scanning_char = self.program[self.pc]

        while scanning_char == self.program[self.pc]:
            next_chunk += self.program[self.pc]
            self.pc += 1

        return next_chunk

    def step_chunk(self, chunks=1):
        for _ in range(chunks):
            self.cur_chunk = self.next_chunk
            self.next_chunk = self.get_next_chunk()

    def remove_redundant_code(self, code: str) -> str:
        '''Removes some redundant code from BF code.'''
        code = code.replace("+-", "")
        code = code.replace("<>", "")
        code = code.replace("-+", "")
        code = code.replace("><", "")
        code = code.replace("][-]", "]")
        code = code.replace("[]", "")
        return code

    def optimize(self, code: str) -> str:
        '''Perform basic optimizations to BF code.'''
        code = self.remove_redundant_code(code)
        self.step_chunk(10)
        return code


def main():
    cg = CodeGenerator()
    code = ""
    code += cg.add_addr(10, 0)
    code += cg.add_addr(10, 1)
    code += cg.dump_array([0, 1])

    opt = Optimizer(code)

    code = opt.optimize(code)
    print(code)


if __name__ == "__main__":
    main()
