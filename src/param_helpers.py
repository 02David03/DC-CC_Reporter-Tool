def is_output_param (param):
    return param['is_pointer'] or param['name'] == '@return'

def create_param_value_comparator (precision):

    def compare (a, b):
        type_a = type(a)
        type_b = type(b)
        if type_a != type_b:
            raise Exception('Incompatible types!')
        elif type_a == float:
            return abs(a - b) < precision
        else:
            return a == b

    return compare