from pycparser import c_ast
import copy

class FuncCallAnalyzer (c_ast.NodeVisitor):
    def __init__ (self):
        self.calls = []
        self.call_assigments = []
    
    def visit_FuncCall (self, node):
        # The first ".name" returns and ID node.
        # Store tuple (function_name, argument_list)
        self.calls.append((node.name.name, node.args.exprs))
        

    def visit_Assignment (self, node):
        if isinstance(node.rvalue, c_ast.FuncCall):
            if isinstance(node.lvalue, c_ast.ID):
                # The first ".name" returns and ID node.
                # Store tuple (function_name, store_variable, local)
                # Example of statement processed:
                #   store_variable = function_name();
                self.call_assigments.append((node.rvalue.name.name, node.lvalue.name, True))
            if isinstance(node.lvalue, c_ast.UnaryOp):
                if node.lvalue.op == '*':
                    self.call_assigments.append((node.rvalue.name.name, node.lvalue.expr.name, False))
    
    def process (self, functions):
        result_functions = copy.deepcopy(functions)
        for func_name, arg_list in self.calls:
            func_def = result_functions.get(func_name)
            if func_def == None:
                continue
            for param_def, arg in zip(func_def, arg_list):
                if isinstance(arg, c_ast.ID):
                    param_def['call_name'] = arg.name
                    param_def['local'] = not param_def['is_pointer']
                elif isinstance(arg, c_ast.UnaryOp):
                    if arg.op == '&' and isinstance(arg.expr, c_ast.ID):
                        param_def['call_name'] = arg.expr.name
                        param_def['local'] = True

        for func_name, store_var, local in self.call_assigments:
            func_def = result_functions.get(func_name)
            if func_def == None:
                continue
            last_param = func_def[-1]
            if last_param['name'] == '@return':
                last_param['call_name'] = store_var
                last_param['local'] = local

        return result_functions
