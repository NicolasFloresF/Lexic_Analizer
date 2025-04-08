from tokens import *
from grammar import *


def read_file(file_name):
    file_object = open(file_name, "r")

    return file_object.read()


def main():
    lexer = lex.lex()
    parser = yacc.yacc(debug=True)
    data = read_file("ex1.por")
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    syntaxParsing = parser.parse(data, lexer=lexer)
    print(syntaxParsing)


if __name__ == "__main__":
    main()
