import ctypes
from param_helpers import is_output_param


class CFunction ():
    def __init__ (self, c_library_path, func_name, func_def):
        c_library = ctypes.CDLL(c_library_path)
        c_function = getattr(c_library, func_name)

        self.output_idxs = []
        self.output_names = []

        self.input_idxs = []
        self.input_names = []

        c_signature = []
        for i, param in enumerate(func_def):
            c_type = getattr(ctypes, 'c_' + param['type'])
            if is_output_param(param):
                c_type = ctypes.POINTER(c_type)
                self.output_idxs.append(i)
                self.output_names.append(param['name'])
            else:
                self.input_idxs.append(i)
                self.input_names.append(param['name'])
                    
            c_signature.append(c_type)

        c_function.restype = None
        c_function.argtypes = c_signature
        self._c_function = c_function

    def run (self, *args):
        output_variables = []
        arg_list = list(args)
        for i in self.output_idxs:
            # obtain an instance from this pointer type
            variable = self._c_function.argtypes[i]._type_()
            # pass variable by reference
            arg_list.insert(i, ctypes.byref(variable))
            output_variables.append(variable)

        self._c_function(*arg_list)
        return output_variables