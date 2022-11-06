import error as err
import vocab


class Atom:
    '''Contains a Token, and some methods to interact with the token'''

    def __init__(self, token: vocab.Token) -> None:
        self.token = token

    def get_value(self):
        return self.token.value

    def __str__(self) -> str:
        return self.token.value


class Opcode(Atom):
    def is_op(token: vocab.Token):
        return token.ttype in vocab.RESERVED_WORDS


class Integer(Atom):
    def is_int(token: vocab.Token):
        return token.ttype == "int"


class Literal():
    '''Char, Integer, etc.'''

    def __init__(self, value: Integer) -> None:
        self.value = value

    def is_literal(token: vocab.Token):
        return Integer.is_int(token)

    def __str__(self) -> str:
        return self.value.__str__()


class Address(Atom):
    def is_address(token: vocab.Token):
        return token.ttype == "address"


class Operand:
    def __init__(self, value):
        self.value = value

    def is_operand(token: vocab.Token):
        return Integer.is_int(token) or Literal.is_literal(token) or Address.is_address(token)

    def __str__(self) -> str:
        return self.value.__str__()


# class Expr:
#     pass  # TODO: Implement Expr, BinOP, etc.


class Line:
    def __init__(self, opcode, operands=[]):
        self.opcode: Opcode = opcode
        self.operands: list[Operand] = operands

    def __str__(self) -> str:
        res = self.opcode.__str__()

        # If the operation has 1 operand ("reset $1")
        if len(self.operands) == 1:
            # Add the operand
            res += f" {self.operands[0].__str__()}"
        # Else if the operation has more than 1 operand ("set $5, 1")
        elif len(self.operands) > 1:
            # Add the first operand
            res += f" {self.operands[0].__str__()}"

            for operand in self.operands[1:]:
                res += f", {operand.__str__()}"

        # Otherwise the operation has no operands ("reset")
        return res


class Program:
    def __init__(self, lines) -> None:
        self.lines: list[Line] = lines

    def __str__(self) -> str:
        res = ""
        for i, line in enumerate(self.lines):
            if i < len(self.lines) - 1:
                res += line.__str__() + "\n"
            else:
                res += line.__str__()
        return res

    # TODO: Add __repr__


class Parser:
    '''Hand written recursive descent parser'''

    def parse(self, stream):
        self.stream = stream

        self.cur_tok = None
        self.next_tok = None

        self.step()

        program = self.parse_program()

        return program

    def step(self, amount=1):
        for _ in range(amount):
            self.cur_tok = self.next_tok
            self.next_tok = next(self.stream, None)

            # skip comments
            # TODO: add parse_comment()
            if self.next_matches("comment"):
                self.next_tok = next(self.stream, None)

    def throw_err(self, msg):
        pos = self.cur_tok.pos
        err.throw("SyntaxError", msg, pos)

    def next_matches(self, tok_type):
        '''Check if a token matches the type of the next token'''
        if self.next_tok and self.next_tok.ttype == tok_type:
            return True
        else:
            return False

    def expect_next(self, tok_type):
        '''Raise error if a token does not match the type of the next token'''
        if not self.next_matches(tok_type):
            self.throw_err(f"Expected {tok_type}")
        else:
            return True

    def parse_program(self):
        program = Program(lines=[])
        self.step()
        while self.next_tok is not None:
            line = self.parse_line()
            program.lines.append(line)
            self.step(2)
        return program

    def parse_line(self):
        while self.cur_tok.ttype == "newline":
            self.step()
            if self.next_tok is None:
                return Line(None, [])

        operation = self.parse_opcode()
        operands = []

        if self.next_matches("newline"):
            return Line(operation, operands)
        else:
            self.step()

        if Operand.is_operand(self.cur_tok):
            operands.append(self.parse_operand())
        else:
            self.throw_err(f"Expected an operand, got '{self.cur_tok.name}'")

        if self.next_matches("newline") or self.next_tok is None:
            return Line(operation, operands)
        elif self.expect_next(","):
            self.step(2)
            operands.append(self.parse_operand())
            return Line(operation, operands)

        self.throw_err("Unexpected syntax error.")

    def parse_opcode(self):
        if Opcode.is_op(self.cur_tok):
            return Opcode(self.cur_tok)
        else:
            self.throw_err(
                f"Expected an operation, got '{self.cur_tok}'")

    def parse_operand(self):
        if Literal.is_literal(self.cur_tok):
            return Operand(self.parse_literal())
        elif Address.is_address(self.cur_tok):
            return Operand(self.parse_address())
        else:
            self.throw_err(f"Expected an operand, got '{self.cur_tok}'")

    def parse_address(self):
        if Address.is_address(self.cur_tok):
            return Address(self.cur_tok)
        else:
            self.throw_err(f"Expected an Address, got '{self.cur_tok}'")

    def parse_literal(self):
        if Literal.is_literal(self.cur_tok):
            # This integer check is not needed right now, since the only literal is int
            if Integer.is_int(self.cur_tok):
                return Literal(self.parse_integer())

    def parse_integer(self):
        if Integer.is_int(self.cur_tok):
            return Integer(self.cur_tok)
        else:
            self.throw_err(f"Expected an Integer, got '{self.cur_tok}'")

    # def parse_char(self):
    #     pass


def main():
    import lexer

    file = lexer.LexingFile("test.asm")
    lex = lexer.Lexer(file)
    tokens = lex.lex()
    parser = Parser()
    ast = parser.parse(tokens)
    print(ast)


if __name__ == "__main__":
    main()
