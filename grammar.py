import ply.yacc as yacc
from ASTnode import ASTnode


# TODO: add symbol table
# TODO: add AST visualization

precedence = (
    ("nonassoc", "EQUAL", "DIFFERENT"),
    ("nonassoc", "LESS_THAN", "LESS_EQUAL", "GREATER_THAN", "GREATER_EQUAL"),
    ("left", "AND", "OR"),
    ("left", "NOT"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("right", "UMINUS"),
)


def p_por_program(p):
    """program : PROGRAM LBRACE function_list RBRACE"""
    p[0] = ASTnode("program", [p[3]], p.lineno(1))


def p_function_list(p):
    """function_list : function
    | function function_list"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_function(p):
    """function : FUNCTION ID LPAREN RPAREN LBRACE commands RBRACE"""
    p[0] = ASTnode("function", [p[2], p[6]], value=p[2], lineno=p.lineno(2))


def p_commands(p):
    """commands : command
    | command commands"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_command(p):
    """command : expression
    | declaration
    | if_statement
    | while_statement
    | for_statement
    | read_statement
    | write_statement"""
    p[0] = p[1]


def p_binary_expression(p):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression"""
    p[0] = ASTnode("binary_expression", [p[1], p[3]], value=p[2], lineno=p.lineno(2))


def p_expr_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = ASTnode("unary_expression", [p[2]], p.lineno(1))


def p_logical_expression(p):
    """expression : expression AND expression
    | expression OR expression"""
    p[0] = ASTnode("logical_expression", [p[1], p[3]], value=p[2], lineno=p.lineno(2))


def p_relational_expression(p):
    """expression : expression LESS_THAN expression
    | expression LESS_EQUAL expression
    | expression GREATER_THAN expression
    | expression GREATER_EQUAL expression
    | expression EQUAL expression
    | expression DIFFERENT expression"""
    p[0] = ASTnode("relational_expression", [p[1], p[3]], value=p[2], lineno=p.lineno(2))


def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_expression_id(p):
    """expression : ID"""
    p[0] = ASTnode("identifier", value=p[1], lineno=p.lineno(1))


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = ASTnode("number", value=p[1], lineno=p.lineno(1))


def p_expression_string(p):
    """expression : STRING"""
    p[0] = ASTnode("string", value=p[1], lineno=p.lineno(1))


def p_declaration(p):
    """declaration : type declaration_list"""
    p[0] = ASTnode("declaration", [p[2]], value=p[1], lineno=p.lineno(1))


def p_type(p):
    """type : INTEGER
    | FLOAT
    | STRING
    | BOOLEAN"""
    p[0] = p[1]


def p_declaration_list(p):
    """declaration_list : ID
    | ID COMMA declaration_list
    | ID ATTRIBUTION expression
    | ID ATTRIBUTION expression COMMA declaration_list"""
    if len(p) == 2:
        p[0] = ASTnode("decl_id", value=p[1], lineno=p.lineno(1))
    elif len(p) == 4 and p[2] == ",":
        p[0] = ASTnode("decl_list", [ASTnode("decl_id", value=p[1]), p[3]])
    elif len(p) == 4 and p[2] == "=":
        p[0] = ASTnode("assignment", [ASTnode("identifier", value=p[1]), p[3]])
    elif len(p) == 6:
        assign = ASTnode("assignment", [ASTnode("identifier", value=p[1]), p[3]])
        p[0] = ASTnode("decl_list", [assign, p[5]])


def p_if_statement(p):
    """if_statement : IF LPAREN expression RPAREN LBRACE commands RBRACE
    | IF LPAREN expression RPAREN LBRACE commands RBRACE ELSE LBRACE commands RBRACE"""
    if len(p) == 8:
        p[0] = ASTnode("if", [p[3], ASTnode("block", p[6])], lineno=p.lineno(1))
    else:
        p[0] = ASTnode("ifelse", [p[3], ASTnode("block", p[6]), ASTnode("block", p[10])], lineno=p.lineno(1))


def p_while_statement(p):
    """while_statement : WHILE LPAREN expression RPAREN LBRACE commands RBRACE"""
    p[0] = ASTnode("while", [p[3], ASTnode("block", p[6])], lineno=p.lineno(1))


def p_for_statement(p):
    """for_statement : FOR LPAREN expression SEMICOLON expression SEMICOLON expression RPAREN LBRACE commands RBRACE"""
    p[0] = ASTnode("for", [p[3], p[5], p[7], ASTnode("block", p[10])], lineno=p.lineno(1))


def p_read_statement(p):
    """read_statement : READ LPAREN ID RPAREN"""
    p[0] = ASTnode("read", value=p[3], lineno=p.lineno(1))


# put STRING so the write statement can be used with strings
# for some reason this put the code in infinite loop
def p_write_statement(p):
    """write_statement : PRINT LPAREN expression RPAREN"""
    p[0] = ASTnode("print", [p[3]], lineno=p.lineno(1))


def p_error(p):
    print(f"Syntax error at '{p.value}'")
