from symbol_table import *


def semantic_analysis(node, table):
    """This function performs semantic analysis in each function in AST, using the local symbol table.
    It checks for type mismatches, undeclared variables, and other semantic errors.

    Args:
        node (ASTnode): The AST node to analyze.
        table (symbol_table): The symbol table to use for semantic analysis.
    """
    from ASTnode import ASTnode

    if isinstance(node, ASTnode):
        if node.nodetype == "function":
            block = next((child for child in node.children if child.nodetype == "commands"), None)
            if block:
                for cmd in block.children:
                    try:
                        semantic_analysis(cmd, table)
                    except Exception as e:
                        print(f"{e}")
                        exit()

        # 'assignment_expression' handler
        elif node.nodetype == "assignment_expression":
            try:
                declared = table.lookup(node.children[0].value)
            except SymbolNotFound as e:
                print(f"{e}")
                exit()

            try:
                expr_type = evaluate_expr_type(node.children[2], table)
            except TypeMismatchError as e:
                print(f"{e}")
                exit()

            if expr_type != declared.type:
                raise TypeMismatchError(
                    f"Type mismatch: Symbol [{declared.value}] expected type '{declared.type}' but get type '{expr_type}' instead",
                    node.lineno,
                )

        # 'increment_expression' handler
        elif node.nodetype == "increment_expression":
            try:
                declared = table.lookup(node.children[0].value)
            except SymbolNotFound as e:
                print(f"{e}")
                exit()
            if declared.type != "inteiro":
                raise TypeMismatchError(
                    f"Type mismatch: Increment operation only allowed on 'inteiro' type, but got '{declared.type}' instead'",
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
                        semantic_analysis(cmd, table)
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
                    semantic_analysis(init_expr, table)
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
                    semantic_analysis(step_expr, table)
                except Exception as e:
                    print(f"{e}")
                    exit()
            else:
                raise InvalidForLoopError(
                    f"Invalid para loop: Invalid step expression in [para] loop", step_expr.lineno
                )
