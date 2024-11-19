from abc import ABC, abstractmethod
from pycparser import c_ast


class VariableStrategy (ABC):

    def __init__ (self, variable_name):
        self.variable_name = variable_name

    @abstractmethod
    def is_in_arg_list (self, arg_list):
        return NotImplemented
    
    @abstractmethod
    def recognizes_assignment (self, node):
        return NotImplemented
    
    @abstractmethod
    def get_node (self):
        return NotImplemented


class LocalVariableStrategy (VariableStrategy):

    def is_in_arg_list (self, arg_list):
        for arg_node in arg_list:
            if type(arg_node) == c_ast.UnaryOp:
                if arg_node.op == '&' and type(arg_node.expr) == c_ast.ID:
                    if arg_node.expr.name == self.variable_name:
                        return True
        return False
    
    def recognizes_assignment (self, node):
        return type(node.lvalue) == c_ast.ID and node.lvalue.name == self.variable_name
    
    def get_node (self):
        return c_ast.ID(name=self.variable_name)


class NonLocalVariableStrategy (VariableStrategy):

    def is_in_arg_list (self, arg_list):
        for arg_node in arg_list:
            if type(arg_node) == c_ast.ID:
                if arg_node.name == self.variable_name:
                        return True
        return False
    
    def recognizes_assignment (self, node):
        return (type(node.lvalue) == c_ast.UnaryOp
            and node.lvalue.op == '*'
            and node.lvalue.expr.name == self.variable_name)
    
    def get_node (self):
        variable_identifier = c_ast.ID(name=self.variable_name)
        return c_ast.UnaryOp(op='*', expr=variable_identifier)


class VariableInstrumentation (c_ast.NodeVisitor):
    instrumented = False

    def __init__ (self, variable_strategy, substitute_value):
        self.variable_strategy = variable_strategy
        self.substitute_value = substitute_value

    def try_to_interfere (self, compound):
        insertion_index = None

        for index, node in enumerate(compound.block_items):
            arg_list = None
            is_variable_being_assigned = False
            if type(node) == c_ast.Assignment:
                if self.variable_strategy.recognizes_assignment(node):
                    is_variable_being_assigned = True
                elif type(node.rvalue) == c_ast.FuncCall:
                    arg_list = node.rvalue.args.exprs
            
            elif type(node) == c_ast.FuncCall:
                arg_list = node.args.exprs
    
            if is_variable_being_assigned or arg_list and self.variable_strategy.is_in_arg_list(arg_list):
                # we will insert after current node
                insertion_index = index + 1
                break
        if insertion_index == None:
            return False

        variable_node = self.variable_strategy.get_node()
        interference = c_ast.Assignment(
            op='=',
            lvalue=variable_node,
            rvalue=c_ast.Constant(type='string', value=self.substitute_value)
        )
        compound.block_items.insert(insertion_index, interference)
        return True


    def visit_Compound (self, node):
        self.instrumented = self.try_to_interfere(node)
        if not self.instrumented:
            self.visit(node.block_items)
