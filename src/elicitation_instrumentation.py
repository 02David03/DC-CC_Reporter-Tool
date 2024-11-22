from pycparser import c_ast
from elicitation_code_setter import ElicitationCodeSetter
from filehandle_closer import FilehandleCloser

from instrumentation_helpers import expand_kcg_type

LITERAL_TYPE_TO_FORMAT = {
    'int': '%d',
    'float': '%f',
    'double': '%lf',
    'char': '%c'
}

DELIMITER = '©©©©'

INSTRUMENTATION_C_FILEHANDLE = '_sigma_four_file'

SUT_RUN_TOKEN = DELIMITER + 'SUT_RUN' + DELIMITER


class ProxyAST ():
 
    def __init__ (self, delimiter_string, printf_output_formats, printf_output_args):
        self.delimiter_string = delimiter_string
        self.printf_output_formats = printf_output_formats
        self.printf_output_args = printf_output_args

    def get_nodes (self, return_statement_node=None):
        delimiter_node = c_ast.FuncCall(
            name=c_ast.ID(name='fprintf'),
            args=c_ast.ExprList(exprs=[
                c_ast.Constant(
                    type='string',
                    value=INSTRUMENTATION_C_FILEHANDLE
                ),
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

        intercept_instruction = None
        if len(printf_args_nodes):
            intercept_instruction = c_ast.FuncCall(
                    name=c_ast.ID(name='fprintf'),
                    args=c_ast.ExprList(exprs=[
                        c_ast.Constant(
                            type='string',
                            value=INSTRUMENTATION_C_FILEHANDLE
                        ),
                        printf_format_node,
                        *printf_args_nodes
                    ])
            )
            
        return [delimiter_node, intercept_instruction, delimiter_node]
        

class ElicitationInstrumentation (c_ast.NodeVisitor):
    functions = {}
    
    def __init__(self, sut_name, output_file_path):
        self.sut_name = sut_name
        # Since this value will be used inside a string,
        # make sure it is escaped.
        self.output_file_path = output_file_path.replace('\\', '\\\\')

    def visit_FuncDef(self, node):
        function_name = node.decl.name

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
        
        
        if function_name == self.sut_name:
            fopen_call = c_ast.FuncCall(
                name=c_ast.ID(name='fopen'),
                args=c_ast.ExprList(exprs=[
                    c_ast.Constant(
                        type='string',
                        value='"%s"' % self.output_file_path
                    ),
                    c_ast.Constant(
                        type='string',
                        value='"a"'
                    )
                ])
            )
            sut_run_print = c_ast.FuncCall(
                name=c_ast.ID(name='fprintf'),
                args=c_ast.ExprList(exprs=[
                    c_ast.ID(name=INSTRUMENTATION_C_FILEHANDLE),
                    c_ast.Constant(
                        type='string',
                        value='"%s\\n"' % SUT_RUN_TOKEN
                    )
                ])
            )
            node.body.block_items = [
                    c_ast.Assignment(
                    op='=',
                    lvalue=c_ast.ID(name=INSTRUMENTATION_C_FILEHANDLE),
                    rvalue=fopen_call
                ),
                sut_run_print,
                *node.body.block_items
            ]
            FilehandleCloser(INSTRUMENTATION_C_FILEHANDLE, with_return).visit(node)
        else:
            # don't instrument main SUT function,
            # we get its return through ctypes foreign function interface
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
