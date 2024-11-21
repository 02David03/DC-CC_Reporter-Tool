from pycparser import c_ast

from instrumentation_helpers import find_return_statement


class ElicitationCodeSetter (c_ast.NodeVisitor):

    def _insert_proxy_nodes (self, node):
        if isinstance(node, c_ast.Compound):
            self.visit(node)
        elif isinstance(node, c_ast.Return):
            return c_ast.Compound([
                *self.output_proxy_ast.get_nodes(return_statement_node=node),
                node
            ])
        return node

    def __init__ (self, input_proxy_ast, output_proxy_ast):
        self.input_proxy_ast = input_proxy_ast
        self.output_proxy_ast = output_proxy_ast

    def visit_Compound (self, node):
        statement_list = node.block_items
        self.visit(statement_list)
        index = find_return_statement(statement_list)
        if index == None:
            return
        instructions = self.output_proxy_ast.get_nodes(return_statement_node=statement_list[index])
        for instruction in reversed(instructions):
            statement_list.insert(index, instruction)
        
    def visit_For (self, node):
        node.stmt = self._insert_proxy_nodes(node.stmt)

    def visit_While (self, node):
        node.stmt = self._insert_proxy_nodes(node.stmt)
    
    def visit_If (self, node):
        node.iftrue = self._insert_proxy_nodes(node.iftrue)
        node.iffalse = self._insert_proxy_nodes(node.iffalse)

    '''
    "with_return" indicates if there will be a return statement
    '''
    def insert_instrumentation (self, node, with_return):
        preamble_instrumentation = self.input_proxy_ast.get_nodes()
        if with_return:
            self.visit(node.body)
            node.body.block_items = [
                *preamble_instrumentation,
                *node.body.block_items
            ]
        else:
            postface_instrumentation = self.output_proxy_ast.get_nodes()
            node.body.block_items = [
                *preamble_instrumentation,
                *node.body.block_items,
                *postface_instrumentation
            ]