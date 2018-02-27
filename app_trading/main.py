'''
https://stackoverflow.com/questions/72852/how-to-do-relative-imports-in-python/73149#73149

This is the answer to the relative imports problem.

Use the -m switch so package structure info is sent to Python.

The real reason why this problem occurs with relative imports, is that relative imports works by taking the __name__ property of the module. If the module is being directly run, then __name__ is set to __main__ and it doesn't contain any information about package structure. And, thats why python complains about the relative import in non-package error. 
'''

import os
import sys

sys.path.append(os.path.join(os.path.split(__file__)[0], "models"))

import time
from models.portfolio import Portfolio
from models.taxes import TaxMan
from models.ticker import Ticker


def Main():

    t = Ticker()
    
    while True:
        t.stock_performance()
        time.sleep(30)


if __name__ == '__main__':
    Main()