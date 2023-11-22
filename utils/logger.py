import os
import sys
import logging

from datetime import datetime, date

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
os.makedirs(LOGSDIR, exist_ok=True)

LOGFILE = os.path.join(
    LOGSDIR,
    f'manzana_am_log_{date.today().strftime("%y%m%d")}{datetime.now().strftime("%H%M%S")}.log'
)

fmts = {
    logging.DEBUG: '\033[32;1m[{asctime}]\033[0m \033[33;1m[Manzana]\033[0m \033[32;1mDEBUG:\033[0m \033[1;37m{message}\033[0m',
    logging.INFO: '\033[32;1m[{asctime}]\033[0m \033[33;1m[Manzana]\033[0m \033[38;5;39;1mINFO:\033[0m \033[1;37m{message}\033[0m',
    logging.WARNING: '\033[32;1m[{asctime}]\033[0m \033[33;1m[Manzana]\033[0m \033[31;1mWARN:\033[0m \033[1;37m{message}\033[0m',
    logging.ERROR: '\033[32;1m[{asctime}]\033[0m \033[33;1m[Manzana]\033[0m \033[31;1mERROR:\033[0m \033[1;37m{message}\033[0m',
    logging.CRITICAL: '\033[32;1m[{asctime}]\033[0m \033[33;1m[Manzana]\033[0m \033[31;1mCRITICAL:\033[0m \033[1;37m{message}\033[0m'
}

class ManzanaFormatter(logging.Formatter):
    def format(self, record):
        logfmt = fmts[record.levelno]
        formatter = logging.Formatter(
            logfmt,
            datefmt='%d-%m-%y %H:%M:%S',
            style='{'
        )
        return formatter.format(record)
        
def __get_logger():
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(ManzanaFormatter())
    streamHandler.setLevel(logging.INFO)

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
        handlers=[streamHandler, fileHandler]
    )

    return logging.getLogger()

logger = __get_logger()

def info(msg, exit=0):
    logger.info(msg)
    if exit: sys.exit(1)

def error(msg, exit=0):
    logger.error(msg)
    if exit: sys.exit(1)

def warning(msg, exit=0):
    logger.warning(msg)
    if exit: sys.exit(1)

def debug(msg):
    logger.debug(msg)