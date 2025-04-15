from exceptions import *


class symbol_table:
    def __init__(self):
        self.symbols = {}

    def define(self, name, value):
        if name in self.symbols:
            raise RedeclarationError(
                f"Redeclaration error: Symbol [{name}] already declared", self.symbols[name].lineno
            )
        self.symbols[name] = value

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        else:
            raise SymbolNotFound(f"No declaration error: Symbol [{name}] is not declared", self.symbols[name].lineno)


class symbol:
    def __init__(self, name, type, lineno=None):
        self.name = name
        self.type = type
        self.lineno = lineno

    def __repr__(self):
        return f"Symbol(name={self.name}, type={self.type})"


def build_symbol_table(node, table=None, var_type=None):
    from ASTnode import ASTnode

    if table is None:
        table = symbol_table()

    if isinstance(node, ASTnode):
        if node.nodetype == "function":
            try:
                table.define(node.value, symbol(node.value, "function", node.lineno))
            except RedeclarationError as e:
                print(f"{e}")
                exit()

            param = next((child for child in node.children if child.nodetype == "param"), None)
            if param:
                params_extract(param, table)

            block = next((child for child in node.children if child.nodetype == "commands"), None)
            if block:
                for cmd in block.children:
                    build_symbol_table(cmd, table)
        elif node.nodetype == "declaration":
            var_type = node.children[0].value
            decls = node.children[1]
            try:
                declarations_extract(decls, table, var_type)
            except TypeMismatchError as e:
                print(f"{e}")
                exit()

    return table


def evaluate_expr_type(expr, table):
    if expr.nodetype == "number":
        if isinstance(expr.value, int):
            return "inteiro"
        elif isinstance(expr.value, float):
            return "real"
    elif expr.nodetype == "string":
        return "caracter"
    elif expr.nodetype == "boolean":
        return "logico"
    elif expr.nodetype == "identifier":
        try:
            sym = table.lookup(expr.value)
        except SymbolNotFound as e:
            print(f"{e}")
            exit()
        return sym.type
    elif expr.nodetype in ["binary_expression", "logical_expression", "relational_expression"]:
        try:
            left_type = evaluate_expr_type(expr.children[0], table)
            right_type = evaluate_expr_type(expr.children[2], table)
        except SymbolNotFound as e:
            print(f"{e}")
            exit()

        if expr.nodetype == "binary_expression":
            if left_type and right_type in ["inteiro", "real"]:
                if left_type == right_type:
                    return left_type
                else:
                    return "real"
            else:
                raise TypeMismatchError(
                    f"Type mismatch: {expr.nodetype} ({expr.value}) expected types 'inteiro' or 'real', but get type '{left_type}' and '{right_type}' instead",
                    expr.lineno,
                )
        if expr.nodetype == "logical_expression":
            if left_type == right_type == "logico":
                return "logico"
            else:
                raise TypeMismatchError(
                    f"Type mismatch: {expr.nodetype} ({expr.value}) expected type 'logico', but get type '{left_type}' and '{right_type}' instead",
                    expr.lineno,
                )
        if expr.nodetype == "relational_expression":
            return "logico"
    else:
        raise TypeMismatchError(
            f"Type mismatch: {expr.nodetype} ({expr.value}) expected types 'inteiro', 'real', 'logico' or expression, but get type 'unknown' instead",
            expr.lineno,
        )


def declarations_extract(decls, table, var_type):
    if decls.nodetype == "declarations":
        for idx, child in enumerate(decls.children):
            if child.nodetype == "identifier":
                try:
                    table.define(child.value, symbol(child.value, var_type, child.lineno))
                except RedeclarationError as e:
                    print(f"{e}")
                    exit()
            elif child.nodetype == "atribuition":
                expr = decls.children[idx + 1]
                try:
                    expr_type = evaluate_expr_type(expr, table)
                except TypeMismatchError as e:
                    print(f"{e}")
                    exit()
                if expr_type != var_type:
                    raise TypeMismatchError(
                        f"Type mismatch: Symbol [{decls.children[idx - 1].value}] expected type '{var_type}' but get type '{expr_type}' instead",
                        child.lineno,
                    )
            elif child.nodetype == "declarations":
                try:
                    declarations_extract(child, table, var_type)
                except TypeMismatchError as e:
                    print(f"{e}")
                    exit()


def params_extract(param, table):
    if param.nodetype == "param":
        var_type = param.children[0].value
        try:
            table.define(param.children[1].value, symbol(param.children[1].value, var_type, param.children[1].lineno))
        except RedeclarationError as e:
            print(f"{e}")
            exit()
        if param.children[-1].nodetype == "param":
            params_extract(param.children[-1], table)
