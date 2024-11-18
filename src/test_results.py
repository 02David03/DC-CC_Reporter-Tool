import re
import collections

from param_helpers import is_output_param, convert_string
from elicitation_instrumentation import DELIMITER


TestResultEntry = collections.namedtuple('TestResultEntry', (
    'inputs',
    'outputs',
    'components_inputs',
    'components_outputs'
))

TestFailureEntry = collections.namedtuple('TestFailureEntry', (
    'test_number',
    'param_name',
    'expected_value',
    'actual_value'
))

INSTRUMENTATION_REGEX = re.compile(DELIMITER + r'(\w+)\.(in|out)')


def _convert_collected_string (string, param_type):
    if param_type == 'char':
        return bytes(string, 'utf-8')[0]
    else:
        return convert_string(string, param_type)


class TestResults:

    _entries = []

    failed_tests = []

    def __init__ (self, function_defs):
        self.functions_defs = function_defs
    
    def _process_instrumented_data (self, instrumented_data):
        components_inputs_entry = {}
        components_outputs_entry = {}
        for lines in zip(instrumented_data, instrumented_data[1:], instrumented_data[2:]):
            if lines[0] == lines[2] and lines[0].startswith(DELIMITER):
                function_name, direction = INSTRUMENTATION_REGEX.match(lines[0]).groups()
                params = lines[1].split()
                function_def = self.functions_defs[function_name]

                if direction == 'in':
                    filter_lambda = lambda p: not is_output_param(p)
                    entry = components_inputs_entry
                else:
                    filter_lambda = is_output_param
                    entry = components_outputs_entry
                converted_param_list = []
                for param_def, param_value in zip(filter(filter_lambda, function_def), params):
                    converted_param_list.append(_convert_collected_string(param_value, param_def['type']))
                entry[function_name] = converted_param_list
        
        return components_inputs_entry, components_outputs_entry

    
    def add (self, inputs, outputs, instrumented_data):
        components_inputs, components_outputs = self._process_instrumented_data(instrumented_data)
        self._entries.append(TestResultEntry(
            inputs,
            outputs,
            components_inputs,
            components_outputs
        ))
    
    def register_failure (self, test_number, param_name, expected_value, actual_value):
        self.failed_tests.append(TestFailureEntry(test_number, param_name, expected_value, actual_value))

    def __len__ (self):
        return len(self._entries)

    def __getitem__ (self, idx):
        return self._entries[idx]