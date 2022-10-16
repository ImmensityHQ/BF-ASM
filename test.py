import collections
import re


just_len = 60


NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

master_pattern = re.compile(
    '|'.join((NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS)))
Token = collections.namedtuple('Token', ['type', 'value'])


def generate_tokens(pattern, text):
    scanner = pattern.scanner(text)
    for m in iter(scanner.match, None):
        token = Token(m.lastgroup, m.group())

        if token.type != 'WS':
            yield token


class ExpressionEvaluator:
    '''
    Implementation of a recursive descent parser.

    Each method implement a single grammar rule.
    It walks from left to right over grammar rule.
    It either consume the rule a generate a syntax error

    Use the ._accept() method to test and accept look ahead token.
    Use the ._expect() method to exactly match and discard the next token on the input.
        or raise a SyntaxError if it doesn't match
    '''

    def parse(self, text):
        self.tokens = generate_tokens(master_pattern, text)
        self.current_token = None
        self.next_token = None
        self._advance()

        # expr is the top level grammar. So we invoke that first.
        # it will invoke other function to consume tokens according to grammar rule.
        return self.expr()

    def _advance(self):
        self.current_token, self.next_token = self.next_token, next(
            self.tokens, None)

    def _accept(self, token_type):
        # if there is next token and token type matches
        if self.next_token and self.next_token.type == token_type:
            self._advance()
            return True
        else:
            return False

    def _expect(self, token_type):
        if not self._accept(token_type):
            raise SyntaxError('Expected ' + token_type)

    def expr(self):
        '''
        expression ::= term { ( +|-) term } *
        '''

        # it first expect a term according to grammar rule
        expr_value = self.term()

        # then if it's either + or -, we try to consume the right side
        #
        # If it's not + or -, then it is treated as no right side
        while self._accept('PLUS') or self._accept('MINUS'):
            # get the operation, + or -
            op = self.current_token.type

            right = self.term()
            if op == 'PLUS':
                expr_value += right
            elif op == 'MINUS':
                expr_value -= right
            else:
                raise SyntaxError('Should not arrive here ' + op)

        return expr_value

    def term(self):
        '''
        term    ::= factor { ('*'|'/') factor } *
        '''

        # it first expect a factor
        term_value = self.factor()

        # then if it's either * or /, we try to consume the right side
        #
        # If it's not + or -, then it is treated as no right side
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.current_token.type

            if op == 'TIMES':
                term_value *= self.factor()
            elif op == 'DIVIDE':
                term_value /= self.factor()
            else:
                raise SyntaxError('Should not arrive here ' + op)

        return term_value

    def factor(self):
        '''
        factor  ::= NUM | (expr)

        '''

        # it can be a number
        if self._accept('NUM'):
            return int(self.current_token.value)
        # or (expr)
        elif self._accept('LPAREN'):
            # we consumed ( in previous _accept
            #
            # then we try to evaluate the expr, and store the value
            expr_value = self.expr()

            # then it should be ), otherwise raise an exception
            self._expect('RPAREN')

            # return the previous saved value
            return expr_value
        else:
            raise SyntaxError('Expect NUMBER or LPAREN')


e = ExpressionEvaluator()
print('parse 2'.ljust(just_len),
      e.parse('2'))

print('parse 2 + 3'.ljust(just_len),
      e.parse('2 + 3'))
print('parse 2 + 3 * 4'.ljust(just_len),
      e.parse('2 + 3 * 4'))

print('parse (2 + 3) * 4'.ljust(just_len),
      e.parse('(2 + 3) * 4'))
