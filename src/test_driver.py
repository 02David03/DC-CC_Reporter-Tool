import csv

from param_helpers import convert_string

    
def _convert_csv_string (string, param_type):
    if param_type == 'char':
        return int(string)
    else:
        return convert_string(string, param_type)


def test_c_function (sut_function, sut_def, test_results, test_csv, compare):
   

    with open(test_csv) as csv_file:    
        csv_reader = csv.reader(csv_file)
        for (row_index, row) in enumerate(csv_reader):
            inputs = []
            for i in range(len(sut_def)):
                if i in sut_function.input_idxs:
                    param_type = sut_def[i]['type']
                    converted_input = _convert_csv_string(row[i], param_type)
                    inputs.append(converted_input)

            output_variables = sut_function.run(*inputs)

            outputs = []
            for i, var in zip(sut_function.output_idxs, output_variables):
                param_type = sut_def[i]['type']
                expected_result = _convert_csv_string(row[i], param_type)
                actual_result = var.value
                outputs.append(actual_result)
                if not compare(expected_result, actual_result):
                    param_idx = len(outputs) - 1
                    test_results.register_failure(row_index, param_idx, row[i], actual_result)

            test_results.add(inputs, outputs)

    return test_results
