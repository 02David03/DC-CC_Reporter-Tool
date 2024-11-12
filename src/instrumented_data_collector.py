import os
import sys
import io
from tempfile import TemporaryFile
import ctypes


class InstrumentedDataCollector():
    def __init__ (self):
        self.libc = ctypes.CDLL(None)
        self.c_stdout = ctypes.c_void_p.in_dll(self.libc, 'stdout')
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