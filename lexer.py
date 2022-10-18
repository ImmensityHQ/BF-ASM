import re

import error as err
from vocab import RESERVED_WORDS, TOKENS, IGNORE, Token


class LexingFile():
    def __init__(self, filename):
        self.filename = filename

        with open(self.filename, "r") as file:
            self.string = file.read()


class Lexer:
    def __init__(self, file: LexingFile):
        self.filename = file.filename
        self.string = file.string
        self.idx = 0
        self.cur_chr = self.string[self.idx]
        self.tokens: list[Token] = []  # list of token objects

        self.lineno = 0
        self.lidx = 0

    def get_pos(self):
        '''Get current position'''
        return err.Position(self.filename, self.lineno, self.lidx, self.lidx)

    def step(self, amount=1):
        '''Step one chr through string. Keeps track of lineno and lidx.'''
        if self.cur_chr == '\n':
            self.lineno += 1
            self.lidx = -1+amount
        else:
            self.lidx += amount

        self.idx += amount

        if self.idx > len(self.string) - 1:
            self.cur_chr = None
        else:
            self.cur_chr = self.string[self.idx]

    def save(self, token: Token):
        self.tokens.append(token)

    def scan_ahead(self, relative_idx):
        return self.string[self.idx+relative_idx]

    def scan_while_reg(self, pattern):
        token = self.cur_chr
        self.step()

        if self.cur_chr == None:
            return token

        while re.match(pattern, self.cur_chr) or re.fullmatch(pattern, token+self.cur_chr):
            token += self.cur_chr
            self.step()

            if self.cur_chr == None:
                return token
        return token

    def skip_ignored(self):
        '''Skips anything that should be ignore by stepping to the next character.'''
        for rule in IGNORE:
            if re.match(rule, self.cur_chr):
                self.step()

                if self.cur_chr == None:
                    return True

                break
        # return None

    def eval_reserved_word(self):
        '''Steps through and saves reserved words'''
        for word in RESERVED_WORDS:
            if not self.cur_chr.isalpha():
                break

            if self.cur_chr != word[0]:
                continue

            is_word = True

            for i in range(len(word)):
                if self.scan_ahead(i) == word[i]:
                    continue
                else:
                    is_word = False

            if is_word == True:
                self.save(Token(word, word, self.get_pos()))
                self.step(len(word))
                return True  # A reserved word was found and saved
            else:
                continue
        # cur_chr didn't match any reserved words
        return False

    def eval_tokens(self):
        '''Step through and saves tokens based on regex patterns'''
        for token in TOKENS:
            tok_def = token[0]  # regex pattern defining the token
            tok_name = token[1]

            if re.match(tok_def, self.cur_chr) or re.match(tok_def, self.cur_chr+self.string[self.idx+1]):
                token = self.scan_while_reg(tok_def)
                self.save(Token(token, tok_name, self.get_pos()))
                return True  # a matching token was found
        return False  # matching token was not found

    def lex(self):
        while self.cur_chr is not None:
            if self.skip_ignored():
                continue

            if self.eval_reserved_word():
                continue

            if self.eval_tokens():
                continue

            pos = err.Position(
                self.filename, self.lineno, self.lidx, self.lidx)
            err.throw("LexingError", f"Illegal Token.", pos)

        # TODO: have eval functions return token, yield token in while loop
        for token in self.tokens:
            yield token


if __name__ == "__main__":
    program = LexingFile("test.asm")
    lexer = Lexer(program)
    stream = lexer.lex()

    for token in stream:
        print(token)
