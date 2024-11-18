import csv

from instrumented_data_collector import InstrumentedDataCollector
from param_helpers import convert_string

    
def _convert_csv_string (string, param_type):
    if param_type == 'char':
        return int(string)
    else:
        return convert_string(string, param_type)


def test_c_function (sut_function, sut_def, test_results, test_csv, compare):
   

    collector = InstrumentedDataCollector()
    with open(test_csv) as csv_file:    
        csv_reader = csv.reader(csv_file)
        for (row_index, row) in enumerate(csv_reader):
            inputs = []
            for i in range(len(sut_def)):
                if i in sut_function.input_idxs:
                    param_type = sut_def[i]['type']
                    converted_input = _convert_csv_string(row[i], param_type)
                    inputs.append(converted_input)

            with collector:
                output_variables = sut_function.run(*inputs)

            outputs = []
            for i, var in zip(sut_function.output_idxs, output_variables):
                param_type = sut_def[i]['type']
                expected_result = _convert_csv_string(row[i], param_type)
                actual_result = var.value
                outputs.append(actual_result)
                if not compare(expected_result, actual_result):
                    param_name = sut_def[i]['name']
                    test_results.register_failure(row_index+1, param_name, row[i], actual_result)

            test_results.add(inputs, outputs, collector.get_data())

    collector.finish()
    return test_results
