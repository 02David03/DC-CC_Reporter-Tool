import re
import collections

from param_helpers import is_output_param, convert_string
from elicitation_instrumentation import DELIMITER


TestResultEntry = collections.namedtuple('TestResultEntry', (
    'inputs',
    'outputs',
    'internal_vars'
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

    internal_vars_names = []

    def __init__ (self, function_defs):
        self.functions_defs = function_defs
    
    def _process_instrumented_data (self, instrumented_data):

        internal_vars = {}
        for lines in zip(instrumented_data, instrumented_data[1:], instrumented_data[2:]):
            if lines[0] == lines[2] and lines[0].startswith(DELIMITER):
                function_name, direction = INSTRUMENTATION_REGEX.match(lines[0]).groups()
                params = lines[1].split()
                function_def = self.functions_defs[function_name]

                if direction == 'out':
                    for param_def, param_value in zip(filter(is_output_param, function_def), params):
                        if param_def['local']:
                            variable_name = param_def['call_name']
                            internal_vars[variable_name] = _convert_collected_string(param_value, param_def['type'])
                            if variable_name not in self.internal_vars_names:
                                self.internal_vars_names.append(variable_name)
        
        return internal_vars

    
    def add (self, inputs, outputs, instrumented_data):
        internal_vars = self._process_instrumented_data(instrumented_data)
        self._entries.append(TestResultEntry(
            inputs,
            outputs,
            internal_vars
        ))
    
    def register_failure (self, test_number, param_name, expected_value, actual_value):
        self.failed_tests.append(TestFailureEntry(test_number, param_name, expected_value, actual_value))

    def __len__ (self):
        return len(self._entries)

    def __getitem__ (self, idx):
        return self._entries[idx]