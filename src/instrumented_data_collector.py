import os
import sys
import io
import ctypes
from tempfile import TemporaryFile
from ctypes.util import find_library

def load_standard_library():
    if os.name == 'nt':  # Windows
        return ctypes.CDLL("msvcrt.dll")
    else: # Linux
        libc_path = find_library("c")
        if not libc_path:
            raise OSError("Could not find the standard C library")
        return ctypes.CDLL(libc_path)

def load_stdout(libc):
    if os.name == 'nt':  # Windows
        stdout = ctypes.c_void_p.in_dll(libc, '_iob')  
        c_stdout = ctypes.cast(stdout, ctypes.POINTER(ctypes.c_void_p))[1] 
    else:  # Linux
        c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')

class InstrumentedDataCollector():
    def __init__ (self):
        self.libc = load_standard_library()
        self.c_stdout = load_stdout(self.libc)
        self.tempfile = TemporaryFile(mode='w+')
        self.intercepted_fd = sys.stdout.fileno()
        self.duplicated_stdout = os.dup(self.intercepted_fd)

    def __enter__ (self):
        os.dup2(self.tempfile.fileno(), self.intercepted_fd)
    
    def __exit__ (self, type, value, traceback):
        self.libc.fflush(self.c_stdout)
        self.tempfile.flush()
        os.dup2(self.duplicated_stdout, self.intercepted_fd)

    def get_data (self):
        self.tempfile.seek(0, io.SEEK_SET)
        content = self.tempfile.readlines()
        self.tempfile.truncate()
        return content
    
    def finish (self):
        self.tempfile.close()
        os.close(self.duplicated_stdout)