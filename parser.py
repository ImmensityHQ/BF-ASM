from ast import literal_eval
from dataclasses import dataclass
import error
import vocab

# ========== AST ==========


class Operation:
    def __init__(self, opcode: str):
        self.opcode = opcode

    def is_op(token: vocab.Token):
        return token.ttype in vocab.RESERVED_WORDS


class Integer:
    def __init__(self, integer: int) -> None:
        self.integer = integer

    def is_int(token: vocab.Token):
        return token.ttype == "int"


class Literal:
    '''Char, Integer, etc.'''

    def __init__(self, value) -> None:
        self.value = value

    def is_literal(token: vocab.Token):
        return token.ttype == "int"


class Operand:
    def __init__(self, operand: Integer):
        self.operand = operand


class Expr:
    pass  # TODO: Implement Expr, BinOP, etc.


class Line:
    def __init__(self, opcode, operand=None):
        self.opcode: Operation = opcode

        if operand:
            self.operand: Operand = operand


class Program:
    def __init__(self, lines) -> None:
        self.lines: list[Line] = lines


# ========== --- ==========


class Parser:
    '''Hand written recursive descent parser'''

    def parse(self, stream):
        self.stream = stream

        self.cur_tok = None
        self.next_tok = None

        self.step()

        program = self.parse_program()

        return program

    def step(self):
        self.cur_tok = self.next_tok
        self.next_tok = next(self.stream, None)

    def next_matches(self, tok_type):
        '''Check if a token matches the type of the next token'''
        if self.next_tok and self.next_tok.ttype == tok_type:
            self.step()
            return True
        else:
            return False

    def expect(self, tok_type):
        '''Raise error if a token does not match the type of the next token'''
        if not self.match(tok_type):
            # TODO: change to bfasm error
            raise SyntaxError('Expected ' + tok_type)

    def parse_program(self):
        program = Program(lines=[])
        self.step()
        while self.next_tok is not None:
            line = self.parse_line()
            program.lines.append(line)
            self.step()
        return program

    def parse_line(self):
        operation = self.parse_operation()
        self.step()

        if self.cur_tok.ttype == "newline":
            return Line(operation)

        while self.cur_tok.ttype != "newline":
            operand = self.parse_operand()
            self.step()

        return Line(operation, operand)

    def parse_operation(self):
        if Operation.is_op(self.cur_tok):
            return Operation(self.cur_tok)
        else:
            pass  # TODO: Return error

    def parse_operand(self):
        if Literal.is_literal(self.cur_tok):
            return Operand(self.parse_literal())

    def parse_literal(self):
        if Integer.is_int(self.cur_tok):
            return Literal(self.parse_integer())

    def parse_integer(self):
        if Integer.is_int(self.cur_tok):
            return Integer(self.cur_tok)
        else:
            pass  # TODO: Return error

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
