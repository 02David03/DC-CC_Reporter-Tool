from pycparser import c_ast

def find_return_statement (statements_list):
    for (i, stmt) in enumerate(statements_list):
        if isinstance(stmt, c_ast.Return):
            return i

KCG_TYPE_TO_LITERAL_TYPE = {
    'kcg_int': 'int',
    'kcg_real': 'double',
    'kcg_bool': 'char',
    'kcg_char': 'char'
}

# Simulink defines its own KCG types (header "kcg_types.h")
def expand_kcg_type (some_type):
    literal_type = KCG_TYPE_TO_LITERAL_TYPE.get(some_type)
    if literal_type:
        return literal_type
    else:
        return some_type
