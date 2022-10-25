class CodeGenerator:
    '''Naive code generator for common BF operations.'''

    def __init__(self):
        self.sp = 0

    def add(self, amount: int) -> str:
        '''Generate BF code to add an integer to the current cell.'''
        return "+" * amount

    def sub(self, amount: int) -> str:
        '''Generate BF code to subtract an integer from the current cell.'''
        return "-" * amount

    def set_cur(self, integer: int) -> str:
        '''Generate BF code to set current cell to an integer.'''
        return "[-]" + self.add(integer)

    def goto_relative(self, amount: int) -> str:
        '''Generate BF code to goto a cell, relative to the current cell.'''
        if 0 < amount:
            self.sp += amount
            return ">" * amount
        else:
            self.sp - amount
            if self.sp < 0:
                self.sp = 0

            return "<" * abs(amount)

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
            looped = ""
            for i in code:
                looped += i
            return f"[{looped}]"


def remove_redundant_code(code: str) -> str:
    '''Removes some redundant code from BF code.'''
    code = code.replace("+-", "")
    code = code.replace("<>", "")
    code = code.replace("-+", "")
    code = code.replace("><", "")
    code = code.replace("][-]", "]")
    code = code.replace("[]", "")
    return code


def optimize(code: str) -> str:
    '''Perform basic optimizations to BF code.'''
    code = remove_redundant_code(code)
    return code


def main():
    cg = CodeGenerator()
    code = ""
    code += cg.add(2)
    code += cg.goto(5)
    code += cg.sub(2)
    code += cg.goto(0)
    code += cg.sub(2)
    code += cg.goto(10)
    print(cg.loop(code))
    print(cg.sp)

    print(optimize(code))


if __name__ == "__main__":
    main()
