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
from reports import report_results_in_js


OUTPUT_FOLDER = 'output'

arg_parser = argparse.ArgumentParser(
    description="Instrument and test C functions"
)
arg_parser.add_argument('c_src_dir')
arg_parser.add_argument('sut')

opts = arg_parser.parse_args()

test_csv = os.path.join(opts.c_src_dir, 'test.csv')

instrument.set_up_output_folder(opts.c_src_dir, OUTPUT_FOLDER)
instrument.instrument_for_elicitation(opts.sut, opts.c_src_dir, OUTPUT_FOLDER)

if not os.path.isfile(test_csv):
    print('CSV file "%s" not found!' % test_csv)
    exit(1)

function_defs_json_path = os.path.join(OUTPUT_FOLDER, instrument.FUNCTIONS_JSON_FILE)
c_library_path = os.path.join(OUTPUT_FOLDER, instrument.LIBRARY_FILE)
if not (os.path.isfile(function_defs_json_path) and os.path.isfile(c_library_path)):
    print('Could not load folder "%s".' % OUTPUT_FOLDER)
    print('Make sure it is previously instrumented code!')
    exit(1)

function_defs_json_file = open(function_defs_json_path)
function_defs = json.load(function_defs_json_file)
function_defs_json_file.close()

sut_def = function_defs.get(opts.sut)
if sut_def == None: 
    print(f'No function found with the name "{opts.sut}"')
    exit(1)

compare = create_param_value_comparator()
c_function = CFunction(c_library_path, opts.sut, sut_def)
test_results = TestResults(function_defs)

test_c_function(c_function, sut_def, test_results, test_csv, compare)
instrumentation_data_filehandle = open(os.path.join(OUTPUT_FOLDER, instrument.INSTRUMENTATION_OUTPUT_FILE))
test_results.process_instrumentation_data(instrumentation_data_filehandle)
instrumentation_data_filehandle.close()

analyzer = Analyzer(test_results, c_function, compare)
analysis_results = analyzer.analyze_dc_cc()
analysis_results_tricked = analyzer.analyze_with_tricked_variables(analysis_results, opts.c_src_dir, OUTPUT_FOLDER)
components_defs = copy.deepcopy(function_defs)
components_defs.pop(opts.sut)
report_results_in_js(components_defs, test_results, analysis_results, analysis_results_tricked.internal_vars)
