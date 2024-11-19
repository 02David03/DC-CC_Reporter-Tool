import argparse
import os
import json
import copy

import instrument
from param_helpers import create_param_value_comparator
from test_results import TestResults
from test_driver import test_c_function
from dc_cc_analyzer import Analyzer
from c_function import CFunction
from reports import report_test_results_in_terminal, report_analysis_results_in_terminal


arg_parser = argparse.ArgumentParser(
    description="Instrument and test C functions"
)
arg_parser.add_argument('sut')
arg_group = arg_parser.add_argument_group('Actions')
arg_group.add_argument('-i', '--instrument', dest='source_dir', help='Instrument code and compile it')
arg_group.add_argument('-t', '--test', action='store_true', help='Test instrumented code')
arg_group.add_argument('-a', '--analyze', action='store_true', help='Analyze for DC|CC')

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
    instrument.instrument_for_elicitation(opts.sut, opts.source_dir, opts.storage_dir)

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
    report_test_results_in_terminal(test_results)


    if opts.analyze:
        component_defs = copy.deepcopy(function_defs)
        component_defs.pop(opts.sut)
        analyzer = Analyzer(test_results, c_function, component_defs, compare)
        analysis_results = analyzer.analyze_dc_cc()
        report_analysis_results_in_terminal(analysis_results)
        analysis_results = analyzer.analyze_with_tricked_variables(analysis_results, opts.source_dir, opts.storage_dir)
        report_analysis_results_in_terminal(analysis_results)
