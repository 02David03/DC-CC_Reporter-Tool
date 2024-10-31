from pycparser import c_ast

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


# Simulink defines its own KCG types (header "kcg_types.h")
def expand_kcg_type (some_type):
    literal_type = KCG_TYPE_TO_LITERAL_TYPE.get(some_type)
    if literal_type:
        return literal_type
    else:
        return some_type


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
                # PtrDecl -> TypeDecl -> IdentifierType
                param_type = param.type.type.type.names[0]
                param_type = expand_kcg_type(param_type)
                printf_output_formats.append(LITERAL_TYPE_TO_FORMAT[param_type])
                printf_output_args.append('*' + param.name)
            else:
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

    