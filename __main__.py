from tokens import *
from grammar import *


def read_file(file_name):
    file_object = open(file_name, "r")

    return file_object.read()


def main():
    lexer = lex.lex()
    parser = yacc.yacc()
    data = read_file("ex1.por")
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    while True:
        result = parser.parse(data, lexer=lexer)
        if not result:
            break
        print(result)


if __name__ == "__main__":
    main()
