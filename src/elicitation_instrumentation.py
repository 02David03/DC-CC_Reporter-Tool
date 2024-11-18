from pycparser import c_ast
from elicitation_code_setter import ElicitationCodeSetter

KCG_TYPE_TO_LITERAL_TYPE = {
    'kcg_int': 'int',
    'kcg_real': 'double',
    'kcg_bool': 'char',
    'kcg_char': 'char'
}

LITERAL_TYPE_TO_FORMAT = {
    'int': '%d',
    'float': '%f',
    'double': '%lf',
    'char': '%c'
}

DELIMITER = 'ΣΣΣΣ'


class ProxyAST ():
 
    def __init__ (self, delimiter_string, printf_output_formats, printf_output_args):
        self.delimiter_string = delimiter_string
        self.printf_output_formats = printf_output_formats
        self.printf_output_args = printf_output_args

    def get_nodes (self, return_statement_node=None):
        delimiter_node = c_ast.FuncCall(
            name=c_ast.ID(name='printf'),
            args=c_ast.ExprList(exprs=[
                c_ast.Constant(
                    type='string',
                    value=self.delimiter_string
                )
            ])
        )
        printf_format_node = c_ast.Constant(
            type='string',
            value='"' + ' '.join(self.printf_output_formats) + '"'
        )
        printf_args_nodes = list(map(
            lambda arg: c_ast.Constant(
                type='string',
                value=arg
            ),
            self.printf_output_args.copy()
        ))
        if return_statement_node:
            printf_args_nodes.append(return_statement_node.expr)
        intercept_instruction = c_ast.FuncCall(
                name=c_ast.ID(name='printf'),
                args=c_ast.ExprList(exprs=[
                    printf_format_node,
                    *printf_args_nodes
                ])
        )
        return [delimiter_node, intercept_instruction, delimiter_node]


# Simulink defines its own KCG types (header "kcg_types.h")
def expand_kcg_type (some_type):
    literal_type = KCG_TYPE_TO_LITERAL_TYPE.get(some_type)
    if literal_type:
        return literal_type
    else:
        return some_type
        

class ElicitationInstrumentation (c_ast.NodeVisitor):
    functions = {}
    
    def __init__(self, sut_name, selection, exclude):
        self.sut_name = sut_name
        self.exclude = exclude
        self.selection = selection

    def visit_FuncDef(self, node):
        function_name = node.decl.name
        if self.exclude:
            if function_name in self.selection:
                return
        else:
            if not function_name in self.selection:
                return

        function_arg_list = node.decl.type.args
        if not function_arg_list:
            return
        declared_params = function_arg_list.params

        printf_input_formats = []
        printf_input_args = []
        printf_output_formats = []
        printf_output_args = []

        params = []
        for param in declared_params:
            if isinstance(param.type, c_ast.ArrayDecl):
                print('Skipping function "%s" because param "%s" is array' % (
                    function_name,
                    param.name
                ))
                return
            is_pointer = isinstance(param.type, c_ast.PtrDecl)
            if is_pointer:
                # The sequence of ".type" below return nodes in the following classes:
                # PtrDecl -> TypeDecl -> IdentifierType
                param_type = param.type.type.type.names[0]
                param_type = expand_kcg_type(param_type)
                printf_output_formats.append(LITERAL_TYPE_TO_FORMAT[param_type])
                printf_output_args.append('*' + param.name)
            else:
                # The sequence of ".type" below return nodes in the following classes:
                # TypeDecl -> IdentifierType
                param_type = param.type.type.names[0]
                param_type = expand_kcg_type(param_type)
                printf_input_formats.append(LITERAL_TYPE_TO_FORMAT[param_type])
                printf_input_args.append(param.name)
            params.append({
                'name': param.name,
                'type': param_type,
                'is_pointer': is_pointer
            })
        
        # The sequence of ".type" below return nodes in the following classes:
        # Decl -> TypeDecl -> IdentifierType
        function_return_type = node.decl.type.type.type.names[0]
        function_return_type = expand_kcg_type(function_return_type)

        delimiter_string = '"\\n' + DELIMITER + function_name + '.out' + '\\n"'

        with_return = function_return_type != 'void'
        if with_return:
            params.append({
                'name': '@return',
                'type': function_return_type,
                'is_pointer': False
            })
            printf_output_formats.append(LITERAL_TYPE_TO_FORMAT[function_return_type])
        self.functions[function_name] = params
        
        # don't instrument main SUT function,
        # we get its return through ctypes foreign function interface
        if function_name != self.sut_name:
            input_proxy_ast = ProxyAST(
                '"\\n' + DELIMITER + function_name + '.in' + '\\n"',
                printf_input_formats,
                printf_input_args
            )

            output_proxy_ast = ProxyAST(
                delimiter_string,
                printf_output_formats,
                printf_output_args
            )
            elicitation_code_setter = ElicitationCodeSetter(input_proxy_ast, output_proxy_ast)
            elicitation_code_setter.insert_instrumentation(node, with_return)
