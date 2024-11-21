from enum import Enum
from itertools import combinations, starmap
import collections
import random
import copy

from instrument import instrument_for_interference


AnalysisStatus = Enum('AnalysisStatus', ('SUCCESS', 'PROBLEMATIC', 'AMBIGUOUS'))
AnalysisResults = collections.namedtuple('AnalysisResults', ('input_params', 'internal_vars'))

class Analyzer ():

    def __init__ (self, test_results, c_function, compare):
        self.test_results = test_results
        self.c_function = c_function
        self.compare = compare

    def analyze_dc_cc (self):
        input_params = {
            input_name: {
                **dict.fromkeys(self.c_function.output_names),
                'status': AnalysisStatus.AMBIGUOUS           
            }
            for input_name in self.c_function.input_names
        }

        internal_vars = {
            var_name: {
                'sut_outputs': None,
                'status': AnalysisStatus.AMBIGUOUS        
            }
            for var_name in self.test_results.internal_vars_names
        }

        analysis_results = AnalysisResults(input_params, internal_vars)

        for test_no_a, test_no_b in combinations(range(len(self.test_results)), 2):
            (inputs_a, outputs_a, expected_outputs_a, internal_vars_a) = self.test_results[test_no_a]
            (inputs_b, outputs_b, expected_outputs_b, internal_vars_b) = self.test_results[test_no_b]

            equal_outputs = all(starmap(
                self.compare,
                zip(outputs_a, outputs_b)
            ))

            varied_inputs_count = 0
            varied_input_msg = None
            varied_input_name = None
            for j in range(len(inputs_a)):
                if not self.compare(inputs_a[j], inputs_b[j]):
                    varied_inputs_count += 1
                    variation_msg = '(%s ⇔ %s)' % (inputs_a[j], inputs_b[j])
                    varied_input_msg = self.c_function.input_names[j] + variation_msg
                    varied_input_name = self.c_function.input_names[j]

            #SUT analysis        
            if varied_inputs_count == 1:
                if equal_outputs:
                    print('Same output tests %d and %d, varied parameter:' % (test_no_a+1, test_no_b+1))
                    print(' ', varied_input_msg)
                    if analysis_results.input_params[varied_input_name]['status'] == AnalysisStatus.AMBIGUOUS:
                        analysis_results.input_params[varied_input_name]['status'] = AnalysisStatus.PROBLEMATIC
                else:
                    analysis_results.input_params[varied_input_name]['status'] = AnalysisStatus.SUCCESS
                    for k in range(len(outputs_a)):
                        current_output = self.c_function.output_names[k]

                        if not analysis_results.input_params[varied_input_name][current_output]:
                            analysis_results.input_params[varied_input_name][current_output] = []

                        if not self.compare(outputs_a[k], outputs_b[k]):
                            if not (test_no_a + 1, test_no_b + 1) in analysis_results.input_params[varied_input_name][current_output]:
                                analysis_results.input_params[varied_input_name][current_output].append((test_no_a + 1, test_no_b + 1))
            
            #Internal variables analysis
            changed_variable = None
            internal_variations_count = 0
            for var_name in self.test_results.internal_vars_names:
                if not self.compare(internal_vars_a[var_name], internal_vars_b[var_name]):
                    internal_variations_count += 1
                    changed_variable = var_name

            if internal_variations_count == 1:
                if equal_outputs:
                    if analysis_results.internal_vars[changed_variable]['status'] == AnalysisStatus.AMBIGUOUS:
                        analysis_results.internal_vars[changed_variable]['status'] = AnalysisStatus.PROBLEMATIC
                else:
                    analysis_results.internal_vars[changed_variable]['status'] = AnalysisStatus.SUCCESS
                    for k in range(len(outputs_a)):
                        current_output = self.c_function.output_names[k]

                        if not analysis_results.internal_vars[changed_variable]['sut_outputs']:
                            analysis_results.internal_vars[changed_variable]['sut_outputs'] = []

                        if not self.compare(outputs_a[k], outputs_b[k]):
                            if not current_output in analysis_results.internal_vars[changed_variable]['sut_outputs']:
                                analysis_results.internal_vars[changed_variable]['sut_outputs'].append(current_output)

        return analysis_results


    def analyze_with_tricked_variables (self, analysis_results, source_dir, output_dir):
        analysis_results = copy.deepcopy(analysis_results)
        for var_name, value in analysis_results.internal_vars.items():
            if value['status'] != AnalysisStatus.AMBIGUOUS:
                continue
            
            basic_value = self.test_results[0].internal_vars[var_name]
            for i in range(1, len(self.test_results)):
                new_value = self.test_results[i].internal_vars[var_name]
                if new_value != basic_value:
                    break
            else:
                while True:
                    new_value = random.randint(0, 255)
                    if new_value != basic_value:
                        break

            instrument_for_interference(self.c_function.func_name, var_name, True, new_value, source_dir, output_dir)
            # Unload from memory Dynamic Loaded Library to force loading from instrumented code
            self.c_function.reload()
            outputs = self.c_function.run(*self.test_results[0].inputs)

            outputs_values = list(map(
                lambda output_var: output_var.value,
                outputs
            ))
            
            equal_outputs = all(starmap(
                self.compare,
                zip(outputs_values, self.test_results[0].outputs)
            ))
            
            if equal_outputs:
                analysis_results.internal_vars[var_name]['status'] = AnalysisStatus.PROBLEMATIC
            else:
                analysis_results.internal_vars[var_name]['status'] = AnalysisStatus.SUCCESS
                for idx in range(len(outputs_values)):
                    current_output = self.c_function.output_names[idx]
                    
                    if not analysis_results.internal_vars[var_name]['sut_outputs']:
                        analysis_results.internal_vars[var_name]['sut_outputs'] = []

                    if not self.compare(outputs_values[idx], self.test_results[0].outputs[idx]):
                        if not current_output in analysis_results.internal_vars[var_name]['sut_outputs']:
                            analysis_results.internal_vars[var_name]['sut_outputs'].append(current_output)

        return analysis_results