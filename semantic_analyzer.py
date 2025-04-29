from symbol_table import *
from ASTnode import ASTnode


def semantic_analysis(node, table, global_table):
    """This function performs semantic analysis in each function in AST, using the local symbol table.
    It checks for type mismatches, undeclared variables, and other semantic errors.

    Args:
        node (ASTnode): The AST node to analyze.
        table (symbol_table): The symbol table to use for semantic analysis.
    """
    if isinstance(node, ASTnode):
        if node.nodetype == "function":
            block = next((child for child in node.children if child.nodetype == "commands"), None)
            if block:
                for cmd in block.children:
                    try:
                        semantic_analysis(cmd, table, global_table)
                    except Exception as e:
                        print(f"{e}")
                        exit()

        # 'assignment_expression' handler
        elif node.nodetype == "assignment_expression":
            try:
                declared = table.lookup(node.children[0].value)
            except SymbolNotFound as e:
                print(f"[Line {node.children[0].lineno}]: {e}")
                exit()

            try:
                expr_type = evaluate_expr_type(node.children[2], table)
            except TypeMismatchError as e:
                print(f"{e}")
                exit()

            if expr_type != declared.type:
                raise TypeMismatchError(
                    f"Type mismatch: Symbol [{node.children[0].value}] expected type '{declared.type}' but get type '{expr_type}' instead",
                    node.lineno,
                )

        # 'increment_expression' handler
        elif node.nodetype == "increment_expression":
            try:
                declared = table.lookup(node.children[0].value)
            except SymbolNotFound as e:
                print(f"[Line {node.children[0].lineno}]: {e}")
                exit()

            if declared.type != "inteiro":
                raise TypeMismatchError(
                    f"Type mismatch: Increment operation only allowed on 'inteiro' type, but got '{declared.type}' instead'",
                    node.lineno,
                )

        elif node.nodetype == "return_expression":
            try:
                expr_type = evaluate_expr_type(node.children[1], table)
            except SymbolNotFound as e:
                print(f"[Line {node.children[0].lineno}]: {e}")
                exit()

        elif node.nodetype == "call_function_expression":
            func_name = node.children[0].value
            try:
                declared = global_table.lookup(func_name)
            except SymbolNotFound as e:
                print(f"[Line {node.children[0].lineno}]: {e}")
                exit()
            params = next((child for child in node.children if child.nodetype == "expression_list"), None)
            if params:
                arg_list = args_extract(params.children, table)
            else:
                arg_list = []

            # Check if the number of arguments matches
            if len(arg_list) != len(declared.params):
                raise ParamCountError(
                    f"Param count error: Function '{func_name}' expected {len(declared.params)} arguments, but got {len(arg_list)} instead",
                    node.lineno,
                )

            # check argument types
            for i in range(len(arg_list)):
                if arg_list[i] != declared.params[i]:
                    raise TypeMismatchError(
                        f"Type mismatch: Argument {i + 1} of function '{func_name}' expected type '{declared.params[i]}', but got '{arg_list[i]}' instead",
                        node.lineno,
                    )

        # 'if' and 'while' statement handler
        elif node.nodetype in ["if", "while"]:
            condition = node.children[1]
            try:
                condition_type = evaluate_expr_type(condition, table)
            except TypeMismatchError as e:
                print(f"{e}")
                exit()

            if condition_type != "logico":
                raise TypeMismatchError(
                    f"Type mismatch: {node.nodetype} Condition must be of type 'logico', but got '{condition_type}' instead'",
                    node.lineno,
                )
            block = next((child for child in node.children if child.nodetype == "commands"), None)
            if block:
                for cmd in block.children:
                    try:
                        semantic_analysis(cmd, table, global_table)
                    except Exception as e:
                        print(f"{e}")
                        exit()

        # 'for' loop handler'
        elif node.nodetype == "for":
            init_expr = node.children[1]
            cond_expr = node.children[3]
            step_expr = node.children[5]

            # first expression (initialization)
            if init_expr.nodetype == "assignment_expression":
                try:
                    semantic_analysis(init_expr, table, global_table)
                except Exception as e:
                    print(f"{e}")
                    exit()
            else:
                raise InvalidForLoopError(
                    f"Invalid para loop: Invalid initialization expression in [para] loop", init_expr.lineno
                )

            # second expression (condition)
            try:
                cond_type = evaluate_expr_type(cond_expr, table)
            except TypeMismatchError as e:
                print(f"{e}")
                exit()
            if cond_type != "logico":
                raise TypeMismatchError(
                    f"Type mismatch: Condition of 'para' loop must be of type 'logico', but got '{cond_type}' instead'",
                    cond_expr.lineno,
                )

            # third expression (step)
            if step_expr.nodetype in ["increment_expression", "assignment_expression"]:
                try:
                    semantic_analysis(step_expr, table, global_table)
                except Exception as e:
                    print(f"{e}")
                    exit()
            else:
                raise InvalidForLoopError(
                    f"Invalid para loop: Invalid step expression in [para] loop", step_expr.lineno
                )


def build_global_table(nodes, table=None):
    for node in nodes:
        if table is None:
            table = symbol_table(parent="programa")

        if isinstance(node, ASTnode):
            if node.nodetype == "function":
                param = next((child for child in node.children if child.nodetype == "param"), None)
                param_types = param_type_extract(param) if param else []

                try:
                    table.define(
                        node.value,
                        symbol(node.value, "function", node.lineno, params=param_types),
                    )
                except RedeclarationError as e:
                    print(f"{e}")
                    exit()

    return table


def build_local_table(node, table=None, var_type=None):
    if table is None:
        table = symbol_table(parent=node.value)

    if isinstance(node, ASTnode):
        if node.nodetype == "function":
            param = next((child for child in node.children if child.nodetype == "param"), None)

            if param:
                params_extract(param, table)

            block = next((child for child in node.children if child.nodetype == "commands"), None)
            if block:
                for cmd in block.children:
                    build_local_table(cmd, table)
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
            print(f"[Line {expr.lineno}]: {e}")
            exit()
        return sym.type
    elif expr.nodetype in ["binary_expression", "logical_expression", "relational_expression"]:
        try:
            left_type = evaluate_expr_type(expr.children[0], table)
            right_type = evaluate_expr_type(expr.children[2], table)
        except TypeMismatchError as e:
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
                dic = symbol_table.return_table(table)
                offset = calculate_offset(dic, var_type)

                try:
                    table.define(child.value, symbol(child.value, var_type, child.lineno, offset=offset))
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

        dic = symbol_table.return_table(table)
        offset = calculate_offset(dic, var_type)

        try:
            table.define(
                param.children[1].value,
                symbol(param.children[1].value, var_type, param.children[1].lineno, offset=offset),
            )
        except RedeclarationError as e:
            print(f"{e}")
            exit()
        if param.children[-1].nodetype == "param":
            params_extract(param.children[-1], table)


def calculate_offset(dic, var_type):
    basic_sizes = {
        "inteiro": 4,
        "real": 8,
        "logico": 1,
        "caracter": 1,
    }[var_type]
    if not dic:
        return -basic_sizes
    else:
        last_offset = list(dic.values())[-1].offset
        return last_offset - basic_sizes


def param_type_extract(param, types=None):
    if types is None:
        types = []
    if param.nodetype == "param":
        types.append(param.children[0].value)
        if param.children[-1].nodetype == "param":
            param_type_extract(param.children[-1], types)
    return types


def args_extract(children, table, param_list=None):
    if param_list is None:
        param_list = []

    for child in children:
        if child.nodetype in [
            "number",
            "string",
            "boolean",
            "identifier",
            "binary_expression",
            "logical_expression",
            "relational_expression",
        ]:
            try:
                id_type = evaluate_expr_type(child, table)
            except SymbolNotFound as e:
                print(f"[Line {child.lineno}]: {e}")
                exit()

            param_list.append(id_type)
        elif child.nodetype == "expression_list":
            param_list = args_extract(child.children, table, param_list)

    return param_list
