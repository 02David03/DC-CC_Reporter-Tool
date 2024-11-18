import argparse
import os
import json
import copy

import instrument
from param_helpers import create_param_value_comparator
from test_results import TestResults
from test_driver import test_c_function
from dc_cc_analyzer import analyze_dc_cc
from c_function import CFunction

arg_parser = argparse.ArgumentParser(
    description="Instrument and test C functions"
)
arg_parser.add_argument('sut')
arg_group = arg_parser.add_argument_group('Actions')
arg_group.add_argument('-i', '--instrument', dest='source_dir', help='Instrument code and compile it')
arg_group.add_argument('-t', '--test', action='store_true', help='Test instrumented code')
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
arg_group.add_argument('-p', '--precision', default=1e-5, type=float, help='Threshold for equality of floating point numbers')

opts = arg_parser.parse_args()

if not (opts.source_dir or opts.test or opts.analyze):
    msg = 'No action specified!'
    print(msg)
    print('=' * len(msg) + '\n')
    arg_parser.print_help()
    exit(1)
    
if opts.analyze and not opts.test:
    print('DC|CC analysis not possible without testing a function (SUT)')
    exit(1)

if opts.source_dir:
    selection = set()
    if opts.functions:
        selection.update(opts.functions.split(','))
    if opts.except_functions:
        selection.update(opts.except_functions.split(','))
    exclude = not opts.functions
    instrument.instrument_for_elicitation(opts.sut, opts.source_dir, opts.storage_dir, selection, exclude)

if opts.test:
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

    compare = create_param_value_comparator(opts.precision)

    test_results = TestResults(function_defs)
    c_function = CFunction(c_library_path, opts.sut, sut_def)

    test_c_function(c_function, sut_def, test_results, opts.test_csv, compare)

    if not len(test_results.failed_tests):
        print('All tests successful.')

    previous_test_number = None
    for failure in test_results.failed_tests:
        if previous_test_number != failure.test_number:
            print(f'Test #{failure.test_number} failed')

        print(f'Expected {failure.param_name}={failure.expected_value}'
                + f' got {failure.param_name}={failure.actual_value}')
        previous_test_number = failure.test_number

    if opts.analyze:
        component_defs = copy.deepcopy(function_defs)
        component_defs.pop(opts.sut)
        analyze_dc_cc(test_results, c_function, component_defs, compare)
