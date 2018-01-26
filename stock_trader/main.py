import csv
import time
import os
import sys
from ticker.models import Ticker

ROOTDIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(ROOTDIR)

def Main():

    t = Ticker()
    
    t.run()
    time.sleep(1)
    

if __name__ == '__main__':
    Main()