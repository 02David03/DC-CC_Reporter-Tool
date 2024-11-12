import argparse
import os
import json

import instrument
from test_driver import test_c_function
from dc_cc_analyzer import analyze_dc_cc

arg_parser = argparse.ArgumentParser(
    description="Instrument and test C functions"
)
arg_group = arg_parser.add_argument_group('Actions')
arg_group.add_argument('-i', '--instrument', dest='source_dir', help='Instrument code and compile it')
arg_group.add_argument('-t', '--test', dest='sut', help='Test instrumented code')
arg_group.add_argument('-a', '--analyze', action='store_true', help='Analyze for DC|CC')

arg_group = arg_parser.add_argument_group('Instrumentation options')
exclusive_group = arg_group.add_mutually_exclusive_group()
exclusive_group.add_argument('-f', '--functions', help='Functions to instrument')
exclusive_group.add_argument('-F', '--except-functions', help='Functions to NOT instrument')

arg_group = arg_parser.add_argument_group('Instrumentation/Test options')
arg_group.add_argument('-s', '--storage-dir', default='output', help='Folder for instrumented code (it will be rewritten) / Source folder to test')

arg_group = arg_parser.add_argument_group('Test options')
arg_group.add_argument('-c', '--test-csv', default='test.csv', help='CSV containing test cases')

arg_group = arg_parser.add_argument_group('DC|CC options')
arg_group.add_argument('-d', '--differences', default=1, type=int, help='How much differences characterizes coupling')
arg_group.add_argument('-p', '--precision', default=1e-9, type=float, help='Threshold for equality of floating point numbers')

opts = arg_parser.parse_args()

if not (opts.source_dir or opts.sut or opts.analyze):
    msg = 'No action specified!'
    print(msg)
    print('=' * len(msg) + '\n')
    arg_parser.print_help()
    exit(1)
    
if opts.analyze and not opts.sut:
    print('DC|CC analysis not possible without testing a function (SUT)')
    exit(1)

if opts.source_dir:
    selection = set()
    if opts.functions:
        selection.update(opts.functions.split(','))
    if opts.except_functions:
        selection.update(opts.except_functions.split(','))
    exclude = not opts.functions
    instrument.instrument_source(opts.source_dir, opts.storage_dir, selection, exclude)

if opts.sut:
    if not os.path.isfile(opts.test_csv):
        print('CSV file "%s" not found!' % opts.test_csv)
        exit(1)

    function_defs_json_path = os.path.join(opts.storage_dir, instrument.FUNCTIONS_JSON_FILE)
    c_library_path = os.path.join(opts.storage_dir, instrument.LIBRARY_FILE)
    if not (os.path.isfile(function_defs_json_path) and os.path.isfile(c_library_path)):
        print('Could not load folder "%s".' % opts.storage_dir)
        print('Make sure it is previously instrumented code!')
        exit(1)

    function_defs_json_file = open(function_defs_json_path)
    function_defs = json.load(function_defs_json_file)
    function_defs_json_file.close()

    sut_def = function_defs.get(opts.sut)
    if sut_def == None: 
        print(f'No function found with the name "{opts.sut}"')
        exit(1)

    def compare (a, b):
        type_a = type(a)
        type_b = type(b)
        if type_a != type_b:
            raise Exception('Incompatible types!')
        elif type_a == float:
            return abs(a - b) < opts.precision
        else:
            return a == b

    test_results = test_c_function(opts.sut, c_library_path, function_defs, opts.test_csv, compare, opts.analyze)

    if opts.analyze:
        analyze_dc_cc(test_results, opts.differences, compare)
