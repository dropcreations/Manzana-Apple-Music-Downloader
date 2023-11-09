import os
import sys
import sqlite3

def __get_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

KEYSDIR = os.path.join(__get_path(),'keys')
os.makedirs(KEYSDIR, exist_ok=True)
KEYSFILE = os.path.join(KEYSDIR, 'keys.db')

con = sqlite3.connect(KEYSFILE)
cur = con.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS DecryptKeys
    (
        PSSH VARCHAR(255) NOT NULL PRIMARY KEY,
        KID VARCHAR(255),
        KEY VARCHAR(255) NOT NULL
    );'''
)
con.commit()
con.close()

def get(__key):
    con = sqlite3.connect(KEYSFILE)
    cur = con.cursor()
    cur.execute(f'SELECT KEY FROM DecryptKeys WHERE PSSH="{__key}"')
    ret = cur.fetchall()
    con.commit()
    con.close()

    if ret:
        return ret[0][0]
    return None

def set(__key, __value):
    __value = __value[0].split(':')
    
    con = sqlite3.connect(KEYSFILE)
    cur = con.cursor()
    cur.execute(f'''INSERT INTO DecryptKeys
        (
            PSSH,
            KID,
            KEY
        )
        VALUES
        (
            "{__key}",
            "{__value[0]}",
            "{__value[1]}"
        );'''
    )
    con.commit()
    con.close()