import os
import shutil
import subprocess
import json

from instrumentator import Instrumentator
from c_transformer import CTransformer

LIBRARY_FILE = 'libsut.so'

FUNCTIONS_JSON_FILE = 'functions.json'

def instrument_source (source_dir, output_dir, selection, exclude):

    c_files = list(filter(
        lambda f: f.endswith('.c'),
        os.listdir(source_dir)
    ))

    shutil.rmtree(output_dir, ignore_errors=True)

    def ignore_instrumented_files (src, names):
        return c_files if src == source_dir else []

    shutil.copytree(
        source_dir,
        output_dir,
        ignore=ignore_instrumented_files
    )

    instrumentator = Instrumentator(selection, exclude)
    c_transformer = CTransformer(instrumentator)
    for filename in c_files:

        try:
            c_transformed = c_transformer.transform(os.path.join(source_dir, filename))
        except KeyError as error:
            print('Could not process type "%s" on file "%s"' % (
                error.args[0],
                filename
            ))
            exit(1)

        output_file = open(os.path.join(output_dir, filename), 'w')
        # ensure printf is defined even if the source to instrument
        # does not include <stdio.h>
        output_file.write('int printf(const char * format, ...);\n')
        output_file.write(c_transformed)
        output_file.close()

    functions_json_file = open(os.path.join(output_dir, FUNCTIONS_JSON_FILE), 'w')
    json.dump(instrumentator.functions, functions_json_file, sort_keys=True, indent=2)
    functions_json_file.close()
        
    compilation_command = ['gcc', '-shared', '-o', LIBRARY_FILE, '-fPIC', *c_files]

    subprocess.run(compilation_command, check=True, cwd=output_dir)
    print("Compilation completed.")