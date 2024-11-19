from pycparser import c_ast

class FuncBodyVisitor (c_ast.NodeVisitor):
    def __init__ (self, func_name, inner_visitor):
        self.func_name = func_name
        self.inner_visitor = inner_visitor

    def visit_FuncDef (self, func_def_node):
        function_name = func_def_node.decl.name
        if function_name == self.func_name:
            self.inner_visitor.visit(func_def_node.body)