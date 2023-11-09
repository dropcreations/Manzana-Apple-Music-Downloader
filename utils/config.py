import os
import sys
import json
import base64

from rich import box
from rich.table import Table
from rich.console import Console
from rich.columns import Columns

from utils import logger

cons = Console()

def __get_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

CONFIGDIR = os.path.join(__get_path(),'config')
os.makedirs(CONFIGDIR, exist_ok=True)

DEVICEDIR = os.path.join(__get_path(),'device')
os.makedirs(DEVICEDIR, exist_ok=True)

CONFIGFILE = os.path.join(CONFIGDIR, 'config.manzana')
DEVICELIST = os.listdir(DEVICEDIR)

def __get_device():
    logger.info("Loading device...")

    if len(DEVICELIST) == 0:
        logger.error("Unable to find a device! Please add a device to continue...", 1)
    elif len(DEVICELIST) == 1:
        return DEVICELIST[0]
    else:
        ids = []

        table = Table(box=box.ROUNDED)
        table.add_column("ID", justify="center")
        table.add_column("Device", justify="left")

        for i, device in enumerate(DEVICELIST):
            table.add_row(str(i), device)
            ids.append(i)

        print()
        columns = Columns(["       ", table])
        cons.print(columns)
        id = input("\n\t Enter ID: ")
        print()

        if id == "": logger.error("Please enter an ID to continue!", 1)
        else:
            try: id = int(id)
            except: logger.error("Input is not valid!", 1)

        if id in ids:
            return DEVICELIST[id]
        else: logger.error("ID not found in the list!", 1)

def get(__key):
    with open(CONFIGFILE, 'r+') as fp:
        return json.loads(
            base64.b64decode(
                fp.read()
            ).decode()
        ).get(__key)

def set(__key, __value):
    with open(CONFIGFILE, 'r+') as fp:
        con = json.loads(
            base64.b64decode(
                fp.read()
            ).decode()
        )
        con[__key] = __value

    with open(CONFIGFILE, 'w+') as fp:
        fp.write(
            base64.b64encode(
                bytes(json.dumps(con), 'utf8')
            ).decode()
        )

def delete(__key):
    with open(CONFIGFILE, 'r+') as fp:
        con = json.loads(
            base64.b64decode(
                fp.read()
            ).decode()
        )

        if __key in con:
            del con[__key]

    with open(CONFIGFILE, 'w+') as fp:
        fp.write(
            base64.b64encode(
                bytes(json.dumps(con), 'utf8')
            ).decode()
        )

def get_config():
    if not os.path.exists(CONFIGFILE):
        con = {}
    else:
        with open(CONFIGFILE, 'r+') as fp:
            con = json.loads(
                base64.b64decode(
                    fp.read()
                ).decode()
            )

    device = __get_device()
    logger.debug(f'Using device: {device}...')

    con['deviceName'] = device
    con['devicePath'] = os.path.join(DEVICEDIR, device)

    if not 'mediaUserToken' in con:
        logger.info("Enter your mediaUserToken to continue...")
        con['mediaUserToken'] = input('\n\tmediaUserToken: ')
        print()

    with open(CONFIGFILE, 'w+') as fp:
        fp.write(
            base64.b64encode(
                bytes(json.dumps(con), 'utf8')
            ).decode()
        )