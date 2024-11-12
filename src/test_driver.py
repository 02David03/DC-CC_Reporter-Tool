import ctypes
import csv
import re

from instrumentator import DELIMITER
from instrumented_data_collector import InstrumentedDataCollector

INSTRUMENTATION_REGEX = re.compile(DELIMITER + r'(\w+)\.(in|out)')

def _convert_string (string, param_type):
    if param_type in ['int']:
        return int(string)
    elif param_type in ['float', 'double']:
        return float(string)
    else:
        return string
    
def _convert_csv_string (string, param_type):
    if param_type == 'char':
        return int(string)
    else:
        return _convert_string(string, param_type)

def _convert_collected_string (string, param_type):
    if param_type == 'char':
        return bytes(string, 'utf-8')[0]
    else:
        return _convert_string(string, param_type)

class TestResults:
    inputs = []
    outputs = []
    components_inputs = []
    components_outputs = []

    def __init__ (self, functions_defs, input_names, output_names):
        self.functions_defs = functions_defs
        self.input_names = input_names
        self.output_names = output_names
    
    def _process_instrumented_data (self, instrumented_data):
        components_inputs_entry = {}
        components_outputs_entry = {}
        for lines in zip(instrumented_data, instrumented_data[1:], instrumented_data[2:]):
            if lines[0] == lines[2] and lines[0].startswith(DELIMITER):
                function_name, direction = INSTRUMENTATION_REGEX.match(lines[0]).groups()
                params = lines[1].split()
                function_def = self.functions_defs[function_name]

                if direction == 'in':
                    filter_lambda = lambda p: not p['is_pointer']
                    entry = components_inputs_entry
                else:
                    filter_lambda = lambda p: p['is_pointer']
                    entry = components_outputs_entry
                converted_param_list = []
                for param_def, param_value in zip(filter(filter_lambda, function_def), params):
                    converted_param_list.append(_convert_collected_string(param_value, param_def['type']))
                entry[function_name] = converted_param_list
        
        self.components_inputs.append(components_inputs_entry)
        self.components_outputs.append(components_outputs_entry)

    
    def add (self, inputs, outputs, instrumented_data):
        self.inputs.append(inputs)
        self.outputs.append(outputs)
        self._process_instrumented_data(instrumented_data)

    def __len__ (self):
        return len(self.inputs)

    def __getitem__ (self, idx):
        return (self.inputs[idx], self.outputs[idx])


def test_c_function (sut_name, c_library_path, functions_defs, test_csv, compare, return_test_results):
    sut_def = functions_defs[sut_name]
    c_library = ctypes.CDLL(c_library_path)
    c_sut_function = getattr(c_library, sut_name)

    c_signature = []

    output_idxs = []
    input_idxs = []

    input_names = []
    output_names = []

    for i, param in enumerate(sut_def):
        c_type = getattr(ctypes, 'c_' + param['type'])
        if param['is_pointer']:
            c_type = ctypes.POINTER(c_type)
            output_idxs.append(i)
            output_names.append(param['name'])
        else:
            input_idxs.append(i)
            input_names.append(param['name'])
                
        c_signature.append(c_type)

    c_sut_function.restype = None
    c_sut_function.argtypes = c_signature
    
    test_results = TestResults(functions_defs, input_names, output_names)

    collector = InstrumentedDataCollector()
    with open(test_csv) as csv_file:    
        csv_reader = csv.reader(csv_file)
        for (row_index, row) in enumerate(csv_reader):
            args = []
            inputs = []
            output_variables = []
            for i in range(len(sut_def)):
                if i in input_idxs:
                    param_type = sut_def[i]['type']
                    converted_input = _convert_csv_string(row[i], param_type)
                    inputs.append(converted_input)
                    args.append(converted_input)
                else:
                    # obtain an instance from this pointer type of variable
                    variable = c_signature[i]._type_()
                    # pass variable by reference
                    args.append(ctypes.byref(variable))
                    output_variables.append(variable)

            with collector:
                c_sut_function(*args)

            outputs = []
            for i, var in zip(output_idxs, output_variables):
                already_failed = False
                param_type = sut_def[i]['type']
                expected_result = _convert_csv_string(row[i], param_type)
                actual_result = var.value
                outputs.append(actual_result)
                if not compare(expected_result, actual_result):
                    if not already_failed:
                        print(f'Test at CSV line {row_index+1} failed')
                        already_failed = True
                    param_name = sut_def[i]['name']
                    print(f'Expected {param_name}={row[i]} got {param_name}={actual_result}')
            if return_test_results:
                test_results.add(inputs, outputs, collector.get_data())

    collector.finish()
    if return_test_results:
        return test_results
