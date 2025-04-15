# import third-party modules
from argparse import ArgumentParser
import os, sys

# import project modules
from tokens import *
from grammar import *
from semantic_analyzer import *


def read_file(file_name):
    file_object = open(file_name, "r")

    return file_object.read()


def print_tokens(lexer):
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


def print_table(table):
    for name, symbol in table.symbols.items():
        print(f"{name}: {symbol}")


def main():
    stdout = sys.stdout
    sys.stdout = open(args.debug, "w")

    lexer = lex.lex()
    lexer.input(data)
    print("Tokens:")
    print_tokens(lexer)

    lexer.lineno = 1
    parser = yacc.yacc(debug=True)
    syntaxParsing = parser.parse(data, lexer=lexer)
    print("AST:")
    print(syntaxParsing)
    dot = syntaxParsing.to_graphviz()
    dot.render("ast", format="png", cleanup=True)

    sys.stdout = stdout
    tables = []
    for functions in syntaxParsing.children[1].children:
        tables.append(build_symbol_table(functions))
        semantic_analysis(functions, tables[-1])

    sys.stdout = open(args.debug, "a")
    print("Symbol Table:")
    for table in tables:
        print_table(table)


if __name__ == "__main__":
    parser = ArgumentParser(description="Compiler for the Por language")
    parser.add_argument("--file", type=str, required=True, help="Input data file")
    parser.add_argument(
        "--debug",
        default=os.devnull,
        action="store_const",
        const="compile.out",
        help="Enable compile.out file",
    )
    args = parser.parse_args()
    data = read_file(args.file)
    main()
