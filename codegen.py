import parser


class codegen:
    '''Naive code generator for common BF operations.'''

    def __init__(self):
        self.sp = 0

    def generate_list(self, funcs):
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
        self.cur_char = ""
        self.cur_chunk = ""
        self.next_chunk = ""

    def step(self):
        self.pc += 1

        if self.pc > len(self.program) - 1:
            self.cur_char = None
        else:
            self.cur_char = self.program[self.pc]

    def get_next_chunk(self):
        next_chunk = ""

        # Make sure to step if we are at the beginning of the program string
        if self.cur_char == "":
            self.step()

        scanning_char = self.cur_char

        while self.cur_char == scanning_char and self.cur_char is not None:
            next_chunk += self.cur_char
            self.step()

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

    def remove_non_bf(self, code: str) -> str:
        '''Remove all non-BF characters.'''
        # TODO: there's probably a better way to do this
        res = ""

        for char in code:
            if char in "+-<>,.[]":
                res += char

        return res

    def optimize(self, code: str) -> str:
        '''Perform basic optimizations to BF code.'''
        code = self.remove_redundant_code(code)
        code = self.remove_non_bf(code)
        self.step_chunk(10)
        return code


class CodeGenerator:
    def __init__(self, program: parser.Program) -> None:
        self.program = program
        self.mem = []
        self.cg = codegen()
        self.prg_out = ""

    def gen_add(self, value: int, target: parser.Address) -> str:
        self.prg_out += self.cg.add_addr(value, target.value.address)

    def gen_sub(self, value: int, target: parser.Address) -> str:
        self.prg_out += self.cg.sub_addr(value, target.value.address)

    def gen_set(self, value: int, target: parser.Address) -> str:
        self.prg_out += self.cg.set_addr(value, target.value.address)

    def gen_code(self) -> str:
        for line in self.program.lines:
            match line.opcode.token.value:
                case "add":
                    self.gen_add(line.operands[0], line.operands[1])
                case "sub":
                    self.gen_sub(line.operands[0], line.operands[1])
                case "set":
                    self.gen_set(line.operands[0], line.operands[1])
                case "dump":
                    self.gen_dump()
        return self.prg_out


def main():
    import lexer

    file = lexer.LexingFile("test.asm")
    lex = lexer.Lexer(file)
    tokens = lex.lex()
    _parser = parser.Parser()
    ast = _parser.parse(tokens)
    cg = CodeGenerator(ast)
    print(cg.gen_code())


if __name__ == "__main__":
    main()
