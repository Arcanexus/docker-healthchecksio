import logging
import sys
import threading
from logfmter import Logfmter
from pythonjsonlogger.json import JsonFormatter
from .common import bcolors, get_formatted_datetime
from .config import current_config


class CustomFormatter(logging.Formatter):
    def format(self, record):
        current_datetime = get_formatted_datetime()
        thread_name = threading.current_thread().name
        thread_id = threading.get_ident()
        loglvl = record.levelname.upper()
        msg = record.getMessage()
        msg = msg.replace(' UP ', f"{bcolors.OKGREEN} UP {bcolors.ENDC}")
        msg = msg.replace(' DOWN ', f"{bcolors.RED} DOWN {bcolors.ENDC}")

        if loglvl == 'DEBUG':
            logcolor = bcolors.GREEN
            return f"{logcolor}{current_datetime} - [{loglvl}] - [{thread_name}-{thread_id}] - {msg}{bcolors.ENDC}"
        elif loglvl == 'INFO':
            logcolor = bcolors.OKBLUE
        elif loglvl == 'WARNING':
            logcolor = bcolors.YELLOW
        elif loglvl == 'ERROR':
            logcolor = bcolors.RED
        elif loglvl == 'CRITICAL':
            logcolor = bcolors.RED
            return f"{logcolor}{current_datetime} - [{loglvl}] - [{thread_name}-{thread_id}] - {msg}{bcolors.ENDC}"
        else:
            logcolor = bcolors.ENDC

        return f"{current_datetime} - [{logcolor}{loglvl}{bcolors.ENDC}] - [{thread_name}-{thread_id}] - {msg}{bcolors.ENDC}"


def get_logger():
    logger = logging.getLogger('custom_logger')

    try:
        loglevel = current_config.get('config.logs.log_level')
        print(f"Log level: {loglevel}")
    except:
        loglevel = "INFO"

    try:
        logformat = current_config.get('config.logs.format')
        print(f"Log format: {logformat}")
    except:
        logformat = "console"

    logger.setLevel(getattr(logging, loglevel.upper(), logging.DEBUG))

    stdouthandler = logging.StreamHandler(sys.stdout)

    if logformat == "console":
        formatter = CustomFormatter()
    elif logformat == "logfmt":
        formatter = Logfmter(
            keys=["time", "level", "process", "thread"],
            mapping={"time": "asctime", "level": "levelname",
                     "process": "processName", "thread": "threadName"},
        )
    elif logformat == "json":
        formatter = JsonFormatter(
            fmt='%(asctime)s %(levelname)s %(processName)s %(threadName)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            rename_fields={"levelname": "level"},
        )

    stdouthandler.setFormatter(formatter)

    logger.addHandler(stdouthandler)
    return logger


logging = get_logger()
logging.setLevel(current_config.get('config.logs.log_level').upper())
