from itertools import combinations, starmap

def analyze_dc_cc (test_results, degree_of_difference, compare):

    for (i, u) in combinations(range(len(test_results)), 2):
        (inputs_a, outputs_a) = test_results[i]
        (inputs_b, outputs_b) = test_results[u]

        equal_outputs = all(starmap(
            compare,
            zip(outputs_a, outputs_b)
        ))
        if not equal_outputs:
            continue

        varied_inputs = []
        for k in range(len(inputs_a)):
            if not compare(inputs_a[k], inputs_b[k]):
                varied_inputs.append(test_results.input_names[k] + f'({inputs_a[k]} ⇔ {inputs_b[k]})')

        if len(varied_inputs) == degree_of_difference:
            print('Same output tests %d and %d' % (i+1, u+1), end='')
            if degree_of_difference > 0:
                parameter_msg = ', varied parameter%s:'
                parameter_msg %= 's' if degree_of_difference > 1 else ''
                print('%s\n\t%s' % (parameter_msg, ', '.join(varied_inputs)))
            else:
                print()
