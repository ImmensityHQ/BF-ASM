from dataclasses import dataclass

import error


@dataclass
class Token:
    value: str
    ttype: str
    pos: error.Position

    def get_line(self):
        return self.pos.get_line

    def __str__(self) -> str:
        if self.ttype == "newline":
            return self.ttype
        return self.value

    def __repr__(self) -> str:
        if self.ttype == "newline":
            return f"Token('\\n', {self.ttype})"
        else:
            return f"Token('{self.value}', {self.ttype})"


RESERVED_WORDS = ["set", "add", "sub", "input", "dump"]

TOKENS = [
    (r"[0-9]", "int"),
    (r"(\"[:ascii:]+\"|'[:ascii:]+')", "chr"),
    (r",", ","),
    (r"\$[0-9]+", "address"),
    (r";.+", "comment"),
    (r"(\r|\n)", "newline")
]

IGNORE = [
    r"[^\S\r\n]"  # matches every whitespace character except newlines
]

PARSING_PRECEDENCE = [
    ("left", ["push", "pop", "add", "sub"]),
    ("left", ["int", "chr", "comment", "newline"])
]


def get_tok_names():
    tok_names = RESERVED_WORDS

    for token in TOKENS:
        tok_names.append(token[1])

    return tok_names
