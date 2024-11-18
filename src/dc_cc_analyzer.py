from itertools import combinations, starmap

from param_helpers import is_output_param


def analyze_dc_cc (test_results, c_function, component_defs, compare):
    all_input_param_names = set(c_function.input_names)
    all_component_output_params = {}
    successful_input_params = set()
    problematic_input_params = set()

    all_component_output_names = set()
    successful_component_outputs = set()
    problematic_component_outputs = set()

    for func_name in component_defs:
        component_internal_output_vars = list(map(
            lambda param: param['call_name'],
            filter(
                lambda param: param['local'] and is_output_param(param),
                component_defs[func_name]
            )
        ))
        all_component_output_names.update(component_internal_output_vars)
        all_component_output_params[func_name] = list(filter(
            lambda param: is_output_param(param),
            component_defs[func_name]
        ))

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
                if varied_input_name not in successful_input_params:
                    print('Same output tests %d and %d, varied parameter:' % (i+1, u+1))
                    print(' ', varied_input_msg)
                    problematic_input_params.add(varied_input_name) 
            else:
                successful_input_params.add(varied_input_name)
            problematic_input_params -= successful_input_params
        
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
                problematic_component_outputs.add(varied_component_output_name)
            else:
                successful_component_outputs.add(varied_component_output_name)
        problematic_component_outputs -= successful_component_outputs
        
    
    ambiguous_input_params = all_input_param_names.difference(problematic_input_params, successful_input_params)
    if len(ambiguous_input_params):
        print('Ambiguous Input Parameters:')
        print(' ', ambiguous_input_params)
    
    if len(problematic_input_params):
        print('Problematic Input Parameters:')
        print(' ', problematic_input_params)
    
    if len(successful_input_params):
        print('Successful Input Parameters:')
        print(' ', successful_input_params)


    ambiguous_component_outputs = all_component_output_names.difference(successful_component_outputs, problematic_component_outputs)
    if len(ambiguous_component_outputs):
        print('Ambiguous Component Outputs:')
        print(' ', ambiguous_component_outputs)
    
    if len(problematic_component_outputs):
        print('Problematic Component Outputs:')
        print(' ', problematic_component_outputs)
    
    if len(successful_component_outputs):
        print('Successful Component Outputs:')
        print(' ', successful_component_outputs)
    
