import re
import collections

from param_helpers import is_output_param, convert_string
from elicitation_instrumentation import DELIMITER, SUT_RUN_TOKEN


TestResultEntry = collections.namedtuple('TestResultEntry', (
    'inputs',
    'outputs',
    'expected_outputs',
    'internal_vars'
))

TestFailureEntry = collections.namedtuple('TestFailureEntry', (
    'test_number',
    'param_idx',
    'expected_value',
    'actual_value'
))

INSTRUMENTATION_REGEX = re.compile(DELIMITER + r'(\w+)\.(in|out)')

# how much lines it is needed for one function instrumentation output
LINE_GROUP = 3


def _convert_collected_string (string, param_type):
    if param_type == 'char':
        return bytes(string, 'utf-8')[0]
    else:
        return convert_string(string, param_type)


class TestResults:

    _entries = []

    internal_vars_names = []

    def __init__ (self, function_defs):
        self._functions_defs = function_defs
    
    def process_instrumentation_data (self, data_filehandle):
        lines = collections.deque([None] * (LINE_GROUP-1), maxlen=LINE_GROUP)
        sut_run_count = -1

        while sut_run_count < len(self):
            line = data_filehandle.readline()
            if not line:
                return
            if line.startswith(SUT_RUN_TOKEN):
                sut_run_count += 1
            
            lines.append(line)

            if lines[0] == lines[LINE_GROUP-1]:
                match = INSTRUMENTATION_REGEX.match(lines[0])
                if match:
                    function_name, direction = match.groups()
                    params = lines[1].split()
                    function_def = self._functions_defs[function_name]

                    if direction == 'out':
                        for param_def, param_value in zip(filter(is_output_param, function_def), params):
                            if param_def['local']:
                                variable_name = param_def['call_name']
                                self[sut_run_count].internal_vars[variable_name] = _convert_collected_string(param_value, param_def['type'])
                                if variable_name not in self.internal_vars_names:
                                    self.internal_vars_names.append(variable_name)


    def add (self, inputs, outputs, expected_outputs):
        self._entries.append(TestResultEntry(
            inputs,
            outputs,
            expected_outputs,
            {}
        ))

    def __len__ (self):
        return len(self._entries)

    def __getitem__ (self, idx):
        return self._entries[idx]
    