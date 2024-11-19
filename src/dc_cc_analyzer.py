from enum import Enum
from itertools import combinations, starmap
import collections
import random
import copy

from param_helpers import is_output_param
from instrument import instrument_for_interference


AnalysisStatus = Enum('AnalysisStatus', ('SUCCESS', 'PROBLEMATIC', 'AMBIGUOUS'))

AnalysisResults = collections.namedtuple('AnalysisResults', ('input_params', 'component_outputs'))

class Analyzer ():

    def __init__ (self, test_results, c_function, component_defs, compare):
        self.test_results = test_results
        self.c_function = c_function
        self.component_defs = component_defs
        self.compare = compare

    def analyze_dc_cc (self):

        all_component_output_params = {}

        component_internal_output_vars = []

        for func_name in self.component_defs:
            component_internal_output_vars.extend(map(
                lambda param: param['call_name'],
                filter(
                    lambda param: param['local'] and is_output_param(param),
                    self.component_defs[func_name]
                )
            ))
        
            all_component_output_params[func_name] = list(filter(
                lambda param: is_output_param(param),
                self.component_defs[func_name]
            ))

        analysis_results = AnalysisResults(
            dict.fromkeys(self.c_function.input_names, AnalysisStatus.AMBIGUOUS),
            dict.fromkeys(component_internal_output_vars, AnalysisStatus.AMBIGUOUS)
        )

        for (param_idx, u) in combinations(range(len(self.test_results)), 2):
            (inputs_a, outputs_a, components_inputs_a, components_outputs_a) = self.test_results[param_idx]
            (inputs_b, outputs_b, components_inputs_b, components_outputs_b) = self.test_results[u]

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

            varied_component_output_name = None
            varied_components_outputs_count = 0
            for func_name in components_outputs_a:
                for j in range(len(components_outputs_a[func_name])):
                    component_output_param_def = all_component_output_params[func_name][j]
                    if not component_output_param_def['local']:
                        continue
                    if not self.compare(components_outputs_a[func_name][j], components_outputs_b[func_name][j]):
                        varied_components_outputs_count += 1
                        varied_component_output_name = component_output_param_def['call_name']

            if varied_components_outputs_count == 1:
                if equal_outputs:
                    if analysis_results.component_outputs[varied_component_output_name] == AnalysisStatus.AMBIGUOUS:
                        analysis_results.component_outputs[varied_component_output_name] = AnalysisStatus.PROBLEMATIC
                else:
                    analysis_results.component_outputs[varied_component_output_name] = AnalysisStatus.SUCCESS

        return analysis_results


    def analyze_with_tricked_variables (self, analysis_results, source_dir, output_dir):
        var_idx = None
        component_name = None
        analysis_results = copy.deepcopy(analysis_results)
        for var, status in analysis_results.component_outputs.items():
            if status != AnalysisStatus.AMBIGUOUS:
                continue
            var_found = False
            for comp in self.component_defs:
                if var_found:
                    break
                for param_idx, param in enumerate(filter(
                    is_output_param,
                    self.component_defs[comp]
                )):
                    if param['call_name'] == var:
                        var_idx = param_idx
                        component_name = comp
                        var_found = True
                        break
            
            basic_value = self.test_results[0].components_outputs[component_name][var_idx]
            for i in range(1, len(self.test_results)):
                new_value = self.test_results[i].components_outputs[component_name][var_idx]
                if new_value != basic_value:
                    break
            else:
                while True:
                    new_value = random.randint(0, 255)
                    if new_value != basic_value:
                        break

            instrument_for_interference(self.c_function.func_name, var, True, new_value, source_dir, output_dir)
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
                analysis_results.component_outputs[var] = AnalysisStatus.PROBLEMATIC
            else:
                analysis_results.component_outputs[var] = AnalysisStatus.SUCCESS

        return analysis_results