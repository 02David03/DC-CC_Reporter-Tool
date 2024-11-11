from pycparser import c_ast
import copy

class FuncCallAnalyzer (c_ast.NodeVisitor):
    def __init__ (self):
        self.calls = []
        self.call_assignments = []
        self.local_variables = set()
    
    def visit_Decl(self, node):
        self.local_variables.add(node.name)
    
    def visit_FuncCall (self, node):
        # The first ".name" returns and ID node.
        # Store tuple (function_name, argument_list)
        self.calls.append((node.name.name, node.args.exprs))
        

    def visit_Assignment (self, node):
        if isinstance(node.rvalue, c_ast.FuncCall):
            # The first ".name" returns and ID node.
            func_name = node.rvalue.name.name
            if isinstance(node.lvalue, c_ast.ID):
                # Store tuple (function_name, store_variable)
                # Example of statement processed:
                #   store_variable = function_name();
                self.call_assignments.append((func_name, node.lvalue.name))
            elif isinstance(node.lvalue, c_ast.UnaryOp):
                self.call_assignments.append((func_name, node.lvalue.expr.name))
            self.visit(node.rvalue)
    
    def process (self, functions):
        result_functions = copy.deepcopy(functions)
        for func_name, arg_list in self.calls:
            func_def = result_functions.get(func_name)
            if func_def == None:
                continue
            for param_def, arg in zip(func_def, arg_list):
                if isinstance(arg, c_ast.ID):
                    call_name = arg.name
                elif isinstance(arg, c_ast.UnaryOp) and isinstance(arg.expr, c_ast.ID):
                    call_name = arg.expr.name
                    if arg.op == '*' and not call_name in self.local_variables:
                        print('WARNING: "%s" in function "%s" is a global output passed as local input' % (
                            call_name, func_name
                        ))
                else:
                    raise Exception('Unhandled parameter in function "%s": %s' % (func_name, arg))
                param_def['call_name'] = call_name
                param_def['local'] = call_name in self.local_variables

        for func_name, store_var in self.call_assignments:
            func_def = result_functions.get(func_name)
            if func_def == None:
                continue
            last_param = func_def[-1]
            if last_param['name'] == '@return':
                last_param['call_name'] = store_var
                last_param['local'] = store_var in self.local_variables

        return result_functions
