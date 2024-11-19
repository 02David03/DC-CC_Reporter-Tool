def report_test_results_in_terminal (test_results):
    if not len(test_results.failed_tests):
        print('All tests successful.')

    previous_test_number = None
    for failure in test_results.failed_tests:
        if previous_test_number != failure.test_number:
            print(f'Test #{failure.test_number} failed')

        print(f'Expected {failure.param_name}={failure.expected_value}'
                + f' got {failure.param_name}={failure.actual_value}')
        previous_test_number = failure.test_number


def report_analysis_results_in_terminal (analysis_results):
    print('\nInput Parameters Analysis\n')
    for input_name, status in analysis_results.input_params.items():
        print(input_name, status.name)
    print('\nInternal Variables Analysis\n')
    for component_output_name, status in analysis_results.internal_vars.items():
        print(component_output_name, status.name)