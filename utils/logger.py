import os
import sys
import logging

from datetime import datetime, date
from rich.console import Console

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

LOGSDIR = os.path.join(__get_path(),'logs')

if not os.path.exists(LOGSDIR):
    os.makedirs(LOGSDIR)

LOGFILE = os.path.join(
    LOGSDIR,
    'manzana_aplm_log_{}{}.log'.format(
        date.today().strftime("%y%m%d"),
        datetime.now().strftime("%H%M%S")
    )
)
        
def __get_logger():
    fileHandler = logging.FileHandler(
        filename=LOGFILE,
        mode='w',
        encoding='utf8'
    )

    fileHandler.setFormatter(
        logging.Formatter(
            fmt='[{asctime}] [Manzana] {levelname}: {message}',
            datefmt='%d-%m-%y %H:%M:%S',
            style='{'
        )
    )
    
    fileHandler.setLevel(logging.DEBUG)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[fileHandler]
    )

    return logging.getLogger()

logger = __get_logger()

def info(msg, exit=0):
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    log = f"[bold green][{now}][/] [bold yellow][ManzanaCore][/] [deep_sky_blue1]INFO:[/] [default]{msg}[/]"

    cons.print(log)
    logger.info(msg)

    if exit: sys.exit(1)

def error(msg, exit=0):
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    log = f"[bold green][{now}][/] [bold yellow][ManzanaCore][/] [bold red]ERROR:[/] [default]{msg}[/]"

    cons.print(log)
    logger.error(msg)

    if exit: sys.exit(1)

def warning(msg, exit=0):
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    log = f"[bold green][{now}][/] [bold yellow][ManzanaCore][/] [bold red]WARN:[/] [default]{msg}[/]"

    cons.print(log)
    logger.warning(msg)

    if exit: sys.exit(1)

def debug(msg):
    logger.debug(msg)
