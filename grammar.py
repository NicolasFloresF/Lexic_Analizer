import ply.yacc as yacc


def p_binary_expression(p):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression
    | expression DIFFERENT expression"""
    if p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]
    elif p[2] == "*":
        p[0] = p[1] * p[3]
    elif p[2] == "/":
        p[0] = p[1] / p[3]
    elif p[2] == "!=":
        if p[1] != p[3]:
            p[0] = True
        else:
            p[0] = False


def p_expression(p):
    """expression : LPAREN expression RPAREN
    | ID
    | NUMBER"""
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1][1:-1]
    elif len(p) == 1:
        p[0] = p[1]


def p_error(p):
    print(f"Syntax error at '{p.value}'")
