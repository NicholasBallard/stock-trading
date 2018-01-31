import os

ROOTDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def upDir():
    export_dir = os.path.abspath(os.path.join(ROOTDIR, '..', '..'))
    print(export_dir)

upDir()