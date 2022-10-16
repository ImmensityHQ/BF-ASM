import lexer
import parser


def main():
    file = lexer.LexingFile("test.asm")
    lex = lexer.Lexer(file)
    tokens = lex.lex()
    ast = parser.Parser().parse(tokens)
    print(ast)


if __name__ == "__main__":
    main()
