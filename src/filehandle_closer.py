from pycparser import c_ast

from instrumentation_helpers import find_return_statement


class FilehandleCloser (c_ast.NodeVisitor):
    def __init__ (self, c_filehandle, with_return):
        self.with_return = with_return
        self.fclose_call = c_ast.FuncCall(
            name=c_ast.ID(name='fclose'),
            args=c_ast.ExprList(exprs=[
                c_ast.ID(name=c_filehandle)
            ])
        )

    def visit_Compound (self, node):
        if self.with_return:
            index = find_return_statement(node.block_items)
            if index != None:
                node.block_items.insert(index, self.fclose_call)
            self.visit(node.block_items)
        else:
            node.block_items.append(self.fclose_call)
        