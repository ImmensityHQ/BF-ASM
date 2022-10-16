from dataclasses import dataclass

import error


# class Token:
#     def __init__(self, name, ttype, pos: error.Position) -> None:
#         self.name = name
#         self.ttype = ttype
#         self.pos = pos

#     def get_line(self):
#         return self.pos.get_line

@dataclass
class Token:
    name: str
    ttype: str
    pos: error.Position

    def get_line(self):
        return self.pos.get_line


RESERVED_WORDS = ["push", "pop", "add", "sub"]

TOKENS = [
    (r"[0-9]", "int"),
    (r"(\"[:ascii:]+\"|'[:ascii:]+')", "chr"),
    (r"^\/\/[^\n\r]+(?:[\n\r]|\*\))$", "comment"),
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
