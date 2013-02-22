import os
import sys
from functools import wraps

def no_stdout_or_stderr(func):
    '''
    Blocks stdout and stderr from being displayed. It will not block Nose
    errors, Python exceptions, etc. Useful for functions that automatically
    write to the command line, like argparse.

    Need to use additional functools.wraps decorator for Nose to recongize
    custom decorators. See: http://stackoverflow.com/questions/7727678/
    '''
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stderr = open(os.devnull, "w")
        sys.stdout = open(os.devnull, "w")
        func(self, *args, **kwargs)
        sys.stdout = self.stdout
        sys.stderr = self.stderr
    return wrapper
