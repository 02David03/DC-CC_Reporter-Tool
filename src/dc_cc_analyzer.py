from enum import Enum
from itertools import combinations, starmap
import collections

from param_helpers import is_output_param


AnalysisStatus = Enum('AnalysisStatus', ('SUCCESS', 'PROBLEMATIC', 'AMBIGUOUS'))

AnalysisResults = collections.namedtuple('AnalysisResults', ('input_params', 'component_outputs'))


def analyze_dc_cc (test_results, c_function, component_defs, compare):

    all_component_output_params = {}

    component_internal_output_vars = []
    for func_name in component_defs:
        component_internal_output_vars.extend(map(
            lambda param: param['call_name'],
            filter(
                lambda param: param['local'] and is_output_param(param),
                component_defs[func_name]
            )
        ))
        all_component_output_params[func_name] = list(filter(
            lambda param: is_output_param(param),
            component_defs[func_name]
        ))

    analysis_results = AnalysisResults(
        dict.fromkeys(c_function.input_names, AnalysisStatus.AMBIGUOUS),
        dict.fromkeys(component_internal_output_vars, AnalysisStatus.AMBIGUOUS)
    )

    for (i, u) in combinations(range(len(test_results)), 2):
        (inputs_a, outputs_a, components_inputs_a, components_outputs_a) = test_results[i]
        (inputs_b, outputs_b, components_inputs_b, components_outputs_b) = test_results[u]

        equal_outputs = all(starmap(
            compare,
            zip(outputs_a, outputs_b)
        ))

        varied_inputs_count = 0
        varied_input_msg = None
        varied_input_name = None
        for j in range(len(inputs_a)):
            if not compare(inputs_a[j], inputs_b[j]):
                varied_inputs_count += 1
                variation_msg = '(%s ⇔ %s)' % (inputs_a[j], inputs_b[j])
                varied_input_msg = c_function.input_names[j] + variation_msg
                varied_input_name = c_function.input_names[j]
                

        if varied_inputs_count == 1:
            if equal_outputs:
                print('Same output tests %d and %d, varied parameter:' % (i+1, u+1))
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
                if not compare(components_outputs_a[func_name][j], components_outputs_b[func_name][j]):
                    varied_components_outputs_count += 1
                    varied_component_output_name = component_output_param_def['call_name']
                    # print('Varied component "%s" outputs: %s ⇔ %s' %
                    #     (func_name, components_outputs_a[func_name][j], components_outputs_b[func_name][j])
                    # )

        if varied_components_outputs_count == 1:
            if equal_outputs:
                if analysis_results.component_outputs[varied_component_output_name] == AnalysisStatus.AMBIGUOUS:
                    analysis_results.component_outputs[varied_component_output_name] = AnalysisStatus.PROBLEMATIC
            else:
                analysis_results.component_outputs[varied_component_output_name] = AnalysisStatus.SUCCESS

    return analysis_results