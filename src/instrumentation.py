import os
import shutil
import subprocess
import json
import pathlib
from pycparser import parse_file, c_ast, c_generator

LIBRARY_FILE = 'libsut.so'

FUNCTIONS_JSON_FILE = 'functions.json'

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

class Instrumentator(c_ast.NodeVisitor):
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
        

def instrument_source (source_dir, output_dir, selection, exclude):

    filenames = list(filter(
            lambda f: f.endswith('.c'),
            os.listdir(source_dir)
    ))

    shutil.rmtree(output_dir, ignore_errors=True)
    os.mkdir(output_dir)
    
    script_dir = pathlib.Path(__file__).parent.absolute()
    for filename in filenames:
        ast = parse_file(
            os.path.join(source_dir, filename),
            use_cpp=True,
            cpp_args=['-E', '-I' + str(script_dir.joinpath('fake_libc_include'))]
        )
    
        instrumentator = Instrumentator(selection, exclude)
        instrumentator.visit(ast)
    
        generator = c_generator.CGenerator()
        output_file = open(os.path.join(output_dir, filename), 'w')
        output_file.write('int printf(const char * format, ...);\n')
        output_file.write(generator.visit(ast))
        output_file.close()
        
        functions_json_file = open(os.path.join(output_dir, FUNCTIONS_JSON_FILE), 'w')
        json.dump(instrumentator.functions, functions_json_file, sort_keys=True, indent=2)
        functions_json_file.close()
        
    compilation_command = ['gcc', '-shared', '-o', LIBRARY_FILE, '-fPIC', *filenames]
    # compilation_command = [
    #   'gcc', '-o', 'executable', *filenames
    # ]
    try:
        subprocess.run(compilation_command, check=True, cwd=output_dir)
        print("Compilation completed.")
    except subprocess.CalledProcessError as e:
        print(f"Compilation failure: {e}")
    