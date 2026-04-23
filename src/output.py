from argparse import Namespace
import logging

LEVEL_MAP = {
    "DEBUG": "DEBG",
    "INFO": "INFO",
    "WARNING": "WARN",
    "ERROR": "ERR",
    "CRITICAL": "CRIT",
}

GREY = "\x1b[38;20m"
YELLOW = "\x1b[33;20m"
RED = "\x1b[31;20m"
BOLD_RED = "\x1b[31;1m"
RESET = "\x1b[0m"
CYAN = "\x1b[36;20m"
BOLD_CYAN = "\x1b[36;1m"
GREEN = "\x1b[32;20m"
BOLD_GREEN = "\x1b[32;1m"

class CustomFormatter(logging.Formatter):
    
    format = "%(message)s"  # type: ignore

    FORMATS = {
        logging.DEBUG: GREEN + ">> " +  format + RESET,  # type: ignore
        logging.INFO: CYAN + ">> " +  format + RESET,  # type: ignore
        logging.WARNING: YELLOW + ">> (Warning) " +  format + RESET,  # type: ignore
        logging.ERROR: RED + ">> (Error) " +  format + RESET,  # type: ignore
        logging.CRITICAL: BOLD_RED + ">> (Critical) " +  format + RESET,  # type: ignore
    }
    
    def format(self, record):
        record.levelname = LEVEL_MAP.get(record.levelname, record.levelname)
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def init_logger(arguments: Namespace) -> logging.Logger:
    logger: logging.Logger = logging.getLogger("pypdf")
    logger.setLevel(logging.ERROR)
    
    # Handle level of logger
    logger = logging.getLogger("compressify")
    match(arguments.verbosity):
        case 0:
            logger.setLevel(logging.CRITICAL)
        case 1:
            logger.setLevel(logging.ERROR)
        case 2:
            logger.setLevel(logging.WARN)
        case 3:
            logger.setLevel(logging.INFO)
        case 4:
            logger.setLevel(logging.DEBUG)
        case _:
            logger.disabled = True
    
    # Create formatter
    handler = logging.StreamHandler()
    formatter = CustomFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

def printSectionHeader(message: str):
    print(f">> {BOLD_CYAN}{message}{RESET}")