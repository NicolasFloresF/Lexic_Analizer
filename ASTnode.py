import ply.yacc as yacc


class ASTnode:
    def __init__(self, nodetype, children=None, value=None, lineno=None):
        self.nodetype = nodetype
        self.children = children if children is not None else []
        self.lineno = lineno
        self.value = value
        self.childnum = len(self.children)

    def __repr__(self, level=0):
        indent = "  " * level
        ret = f"{indent}{self.nodetype}"
        if self.value is not None:
            ret += f": {self.value}"
        ret += "\n"

        for child in self.children:
            if isinstance(child, ASTnode):
                ret += child.__repr__(level + 1)
            else:
                ret += "  " * (level + 1) + repr(child) + "\n"
        return ret
