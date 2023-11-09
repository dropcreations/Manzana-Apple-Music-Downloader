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

CACHEDIR = os.path.join(__get_path(),'cache')
os.makedirs(CACHEDIR, exist_ok=True)
CACHEFILE = os.path.join(CACHEDIR, 'cache.manzana')

if not os.path.exists(CACHEFILE):
    with open(CACHEFILE, 'w+', encoding='utf8') as fp:
        json.dump({}, fp)

def get(__key):
    with open(CACHEFILE, 'r+', encoding='utf8') as fp:
        return json.load(fp).get(__key)
    
def set(__key, __value):
    with open(CACHEFILE, 'r+', encoding='utf8') as fp:
        cd = json.load(fp)
        cd[__key] = __value
    
    with open(CACHEFILE, 'w+', encoding='utf8') as fp:
        json.dump(cd, fp)