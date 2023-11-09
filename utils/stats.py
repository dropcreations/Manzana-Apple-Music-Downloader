import os
import sys
import json

def __get_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

TEMPDIR = os.path.join(__get_path(),'temp')
os.makedirs(TEMPDIR, exist_ok=True)

OUTPUTDIR = os.path.join(__get_path(),'output')
os.makedirs(OUTPUTDIR, exist_ok=True)

STATSFILE = os.path.join(TEMPDIR, 'progress.mstats')

if not os.path.exists(STATSFILE):
    with open(STATSFILE, 'w+', encoding='utf8') as fp:
        json.dump({}, fp)

def get(__key):
    with open(STATSFILE, 'r+', encoding='utf8') as fp:
        return json.load(fp).get(__key)
    
def set(__key, __value):
    with open(STATSFILE, 'r+', encoding='utf8') as fp:
        cd = json.load(fp)
        cd[__key] = __value
    
    with open(STATSFILE, 'w+', encoding='utf8') as fp:
        json.dump(cd, fp)