import os
import shutil
import subprocess
import json
import pycparser

from elicitation_instrumentation import ElicitationInstrumentation
from func_call_analyzer import FuncCallAnalyzer
from variable_instrumentation import VariableInstrumentation, LocalVariableStrategy, NonLocalVariableStrategy
from func_body_visitor import FuncBodyVisitor
from c_transformer import CTransformer

LIBRARY_FILE = 'libsut.so'

FUNCTIONS_JSON_FILE = 'functions.json'

def _instrument (transformations, source_dir, output_dir):

    c_files = list(filter(
        lambda f: f.endswith('.c'),
        os.listdir(source_dir)
    ))

    c_transformer = CTransformer(transformations)
    for filename in c_files:

        try:
            c_transformed = c_transformer.transform(os.path.join(source_dir, filename))
        except Exception as error:
            if type(error) == KeyError:
                print('Could not process type "%s" on file "%s"' % (
                    error.args[0],
                    filename
                ))
            elif type(error) == pycparser.plyparser.ParseError:
                print('Could not complete parsing C project:')
                print(' ', error)
            else:
                raise error
            exit(1)

        output_file = open(os.path.join(output_dir, filename), 'w')
        # ensure printf is defined even if the source to instrument
        # does not include <stdio.h>
        output_file.write('int printf(const char * format, ...);\n')
        output_file.write(c_transformed)
        output_file.close()
        
    compilation_command = ['gcc', '-shared', '-o', LIBRARY_FILE, '-fPIC', *c_files]

    subprocess.run(compilation_command, check=True, cwd=output_dir)

def set_up_output_folder (source_dir, output_dir):
    shutil.rmtree(output_dir, ignore_errors=True)

    def ignore_files_to_instrument (src, names):
        return filter(lambda name: name.endswith('.c'), names)

    shutil.copytree(
        source_dir,
        output_dir,
        ignore=ignore_files_to_instrument
    )

def instrument_for_elicitation (sut_function, source_dir, output_dir):

    elicitation = ElicitationInstrumentation(sut_function)
    func_call_analyzer = FuncCallAnalyzer()
    transformations = [elicitation, FuncBodyVisitor(sut_function, func_call_analyzer)]

    _instrument(transformations, source_dir, output_dir)

    functions = func_call_analyzer.process(elicitation.functions)

    functions_json_file = open(os.path.join(output_dir, FUNCTIONS_JSON_FILE), 'w')
    json.dump(functions, functions_json_file, sort_keys=True, indent=2)
    functions_json_file.close()


def instrument_for_interference (sut_function, variable_name, local, substitute_value, source_dir, output_dir):
    if local:
        variable_strategy = LocalVariableStrategy(variable_name)
    else:
        variable_strategy = NonLocalVariableStrategy(variable_name)
    variable_interference = VariableInstrumentation(variable_strategy, substitute_value)
    transformations = [FuncBodyVisitor(sut_function, variable_interference)]

    _instrument(transformations, source_dir, output_dir)

    if not variable_interference.instrumented:
        raise Exception('Could not find variable "%s" inside function "%s" to instrument !' % (
            variable_name, sut_function
        ))
