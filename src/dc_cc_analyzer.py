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

        analysis_results = AnalysisResults(
            dict.fromkeys(self.c_function.input_names, AnalysisStatus.AMBIGUOUS),
            dict.fromkeys(self.test_results.internal_vars_names, AnalysisStatus.AMBIGUOUS)
        )

        for (param_idx, u) in combinations(range(len(self.test_results)), 2):
            (inputs_a, outputs_a, internal_vars_a) = self.test_results[param_idx]
            (inputs_b, outputs_b, internal_vars_b) = self.test_results[u]

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
                    

            if varied_inputs_count == 1:
                if equal_outputs:
                    print('Same output tests %d and %d, varied parameter:' % (param_idx+1, u+1))
                    print(' ', varied_input_msg)
                    if analysis_results.input_params[varied_input_name] == AnalysisStatus.AMBIGUOUS:
                        analysis_results.input_params[varied_input_name] = AnalysisStatus.PROBLEMATIC
                else:
                    analysis_results.input_params[varied_input_name] = AnalysisStatus.SUCCESS

            changed_variable = None
            internal_variations_count = 0
            for var_name in self.test_results.internal_vars_names:
                if not self.compare(internal_vars_a[var_name], internal_vars_b[var_name]):
                    internal_variations_count += 1
                    changed_variable = var_name

            if internal_variations_count == 1:
                if equal_outputs:
                    if analysis_results.internal_vars[changed_variable] == AnalysisStatus.AMBIGUOUS:
                        analysis_results.internal_vars[changed_variable] = AnalysisStatus.PROBLEMATIC
                else:
                    analysis_results.internal_vars[changed_variable] = AnalysisStatus.SUCCESS

        return analysis_results


    def analyze_with_tricked_variables (self, analysis_results, source_dir, output_dir):
        analysis_results = copy.deepcopy(analysis_results)
        for var_name, status in analysis_results.internal_vars.items():
            if status != AnalysisStatus.AMBIGUOUS:
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

            outputs_values = map(
                lambda output_var: output_var.value,
                outputs
            )
            equal_outputs = all(starmap(
                self.compare,
                zip(outputs_values, self.test_results[0].outputs)
            ))
            if equal_outputs:
                analysis_results.internal_vars[var_name] = AnalysisStatus.PROBLEMATIC
            else:
                analysis_results.internal_vars[var_name] = AnalysisStatus.SUCCESS

        return analysis_results