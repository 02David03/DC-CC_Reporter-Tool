FLOAT_EQUALITY_PRECISION = 1e-5


def is_output_param (param):
    return param['is_pointer'] or param['name'] == '@return'

def create_param_value_comparator ():

    def compare (a, b):
        type_a = type(a)
        type_b = type(b)
        if type_a != type_b:
            raise Exception('Incompatible types!')
        elif type_a == float:
            return abs(a - b) < FLOAT_EQUALITY_PRECISION
        else:
            return a == b

    return compare

def convert_string (string, param_type):
    if param_type in ('int'):
        return int(string)
    elif param_type in ('float', 'double'):
        return float(string)
    else:
        return string