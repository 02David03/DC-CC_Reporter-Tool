from pycparser import c_ast

TYPE_TO_FORMAT = {
    'int': '%d',
    'float': '%f',
    'double': '%lf',
    'char': '%s'
}

DELIMITER = 'ΣΣΣΣ'


def create_instrumentation_code (title, printf_formats, printf_args):
    delimiter = c_ast.FuncCall(
            name=c_ast.ID(name='printf'),
            args=c_ast.ExprList(exprs=[
                c_ast.Constant(
                    type='string',
                    value='"\\n' + DELIMITER + title + '\\n"'
                )
            ])
    )
    intercept_instruction = c_ast.FuncCall(
            name=c_ast.ID(name='printf'),
            args=c_ast.ExprList(exprs=[
                c_ast.Constant(
                    type='string',
                    value='"' + ' '.join(printf_formats) + '"'
                ),
                *map(lambda arg: c_ast.Constant(
                        type='string',
                        value=arg
                    ),
                    printf_args
                )
            ])
    )
    return [delimiter, intercept_instruction, delimiter]

class Instrumentator (c_ast.NodeVisitor):
    functions = {}
    
    def __init__(self, selection, exclude):
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
        ast_args = node.decl.type.args
        if not ast_args:
            return
        ast_params = ast_args.params

        printf_input_formats = []
        printf_input_args = []
        printf_output_formats = []
        printf_output_args = []

        params = []
        for param in ast_params:
            is_pointer = isinstance(param.type, c_ast.PtrDecl)
            if is_pointer:
                # PtrDecl -> TypeDecl -> IdentifierType
                type = param.type.type.type.names[0]
                if type == 'char':
                    printf_input_formats.append(TYPE_TO_FORMAT[type])
                    printf_input_args.append(param.name)
                else:
                    printf_output_formats.append(TYPE_TO_FORMAT[type])
                    printf_output_args.append('*' + param.name)
            else:
                # TypeDecl -> IdentifierType
                type = param.type.type.names[0]
                printf_input_formats.append(TYPE_TO_FORMAT[type])
                printf_input_args.append(param.name)
            params.append({
                'name': param.name,
                'type': type,
                'is_pointer': is_pointer
            })

        preamble_instrumentation = create_instrumentation_code(
            function_name + '.in',
            printf_input_formats,
            printf_input_args
        )
        postface_instrumentation = create_instrumentation_code(
            function_name + '.out',
            printf_output_formats,
            printf_output_args
        )

        node.body.block_items = [
            *preamble_instrumentation,
            *node.body.block_items,
            *postface_instrumentation
        ]
        
        self.functions[function_name] = params

    