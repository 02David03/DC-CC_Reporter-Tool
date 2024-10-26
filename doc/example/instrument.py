import os
import re
import subprocess
import sys


if len(sys.argv) < 2:
    print('You must specify C source folder!')
    print('Usage:', sys.argv[0], '<c_source_folder>')
    exit(1)

source_dir = sys.argv[1]

filenames = list(map(
    lambda f: source_dir + '/' + f,
    filter(
        lambda f: f.endswith('.c'),
        os.listdir(source_dir)
    )
))

wrap_filename = 'wrappings.c'
wrap_filehandle = open(wrap_filename, 'w')
wrap_filehandle.write('#include <stdio.h>')

function_regex = re.compile(
    r'\w+\s+\w+\s*\((?:[\w\s*]+?)(?:\s*,\s*[\w\s*]+?)*\)\s*?{',
    re.MULTILINE
)
function_type_and_name_regex = re.compile(r'(\w+(?:\s+|\s*\*\s*))(\w+)')
arg_regex = re.compile(r'(\w+)\s*(\*)?\s*(\w+)')

function_names = []

for filename in filenames:
    with open(filename) as filehandle:
        c_source = filehandle.read()

        for function_definition in function_regex.findall(c_source):
            
            startArgumentsIdx, endArgumentsIdx = function_definition.find('('), function_definition.find(')')
            # don't include initial '('
            argumentsString = function_definition[startArgumentsIdx + 1 : endArgumentsIdx]
            
            wrapped_function_name = function_type_and_name_regex.sub(r'\1__wrap_\2', function_definition, count=1)
            
            real_function_name = function_type_and_name_regex.sub(r'\1__real_\2', function_definition, count=1)
            real_function_name = real_function_name.rstrip(' {')

            function_return, function_name = function_type_and_name_regex.match(function_definition).group(1, 2)
            function_return = function_return.strip()
            function_names.append(function_name)

            arguments = list(map(
                lambda x: x.strip(),
                argumentsString.split(',')
            ))

            printf_formats = []
            printf_args = []
            real_function_args = []
            
            type_to_format = {
                'int': '%d',
                'float': '%f',
                'double': '%lf'
            }
            for arg in arguments:
                arg_type, is_arg_pointer, arg_name = arg_regex.match(arg).group(1, 2, 3)

                if type_to_format.get(arg_type) and is_arg_pointer:
                    printf_args.append('*' + arg_name)
                else:
                    printf_args.append(arg_name)

                printf_formats.append(type_to_format.get(arg_type, '%s'))

                real_function_args.append(arg_name)
            
            printf_format_string = ' '.join(printf_formats)
            printf_args_string = ', '.join(printf_args)
            
            wrapped_function_return_string = ''
            real_invocation_return_string = ''
            if function_return != 'void':
                real_invocation_return_string = f'{function_return} _ret = '
                wrapped_function_return_string = f'''printf("return: {type_to_format.get(arg_type, '%s')}\\n", _ret);
    return _ret;'''

            wrapped_function = f'''

{real_function_name};

{wrapped_function_name}
    printf("=== {function_name} [inputs] ===\\n");
    printf("{printf_format_string}\\n", {printf_args_string});
    {real_invocation_return_string}__real_{function_name}({', '.join(real_function_args)});
    printf("=== {function_name} [outputs] ===\\n");
    printf("{printf_format_string}\\n", {printf_args_string});
    {wrapped_function_return_string}
}}
'''
            wrap_filehandle.write(wrapped_function)

wrap_filehandle.close()

if len(function_names) == 0:
    linker_flags = ''
    print('WARNING: no functions detected !')
else:
    linker_flags = '-Wl,' + ','.join(map(
        lambda function_name: '--wrap=' + function_name,
        function_names
    ))

# ['gcc', '-shared', '-o', 'codigo.so', '-fPIC', 'codigo.c']
compilation_command = [
    'gcc', '-o', 'executable',
    linker_flags,
    wrap_filename, *filenames
]
try:
    subprocess.run(compilation_command, check=True)
    print("Compilation completed.")
except subprocess.CalledProcessError as e:
    print(f"Compilation failure: {e}")
