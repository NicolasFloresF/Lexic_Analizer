from tokens import *
from grammar import *
from symbol_table import *

# TODO: add semantic analysis
# TODO: add global variables
# TODO: add function parameters


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

    tables = []
    syntaxParsing = parser.parse(data, lexer=lexer)
    for functions in syntaxParsing.children[1].children:
        if functions.nodetype == "function":
            tables.append(build_symbol_table(functions))

    print("Symbol Table:")
    for table in tables:
        for name, symbol in table.symbols.items():
            print(f"{name}: {symbol}")

    print(syntaxParsing)
    dot = syntaxParsing.to_graphviz()
    dot.render("ast", format="png", cleanup=True)


if __name__ == "__main__":
    main()
