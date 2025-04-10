class symbol_table:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def define(self, name, value):
        if name in self.symbols:
            raise Exception(f"Symbol '{name}' already defined")
        self.symbols[name] = value

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            raise Exception(f"Symbol '{name}' not found")


class symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return f"Symbol(name={self.name}, type={self.type})"


def build_symbol_table(node, table=None, var_type=None):
    from ASTnode import ASTnode

    if table is None:
        table = symbol_table()

    if isinstance(node, ASTnode):
        if node.nodetype == "function":
            table.define(node.value, symbol(node.value, "function"))

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
            declarations_extract(decls, table, var_type)

    return table


def declarations_extract(decls, table, var_type):
    if decls.nodetype == "declarations":
        for child in decls.children:
            if child.nodetype == "identifier":
                table.define(child.value, symbol(child.value, var_type))
            elif child.nodetype == "declarations":
                declarations_extract(child, table, var_type)


def params_extract(param, table):
    if param.nodetype == "param":
        var_type = param.children[0].value
        table.define(param.children[1].value, symbol(param.children[1].value, var_type))
        if param.children[-1].nodetype == "param":
            params_extract(param.children[-1], table)
