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
        
    # Create formatter
    handler = logging.StreamHandler()
    formatter = CustomFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    match(arguments.verbosity):
        case "critical":
            logger.setLevel(logging.CRITICAL)
        case "error":
            logger.setLevel(logging.ERROR)
        case "warning":
            logger.setLevel(logging.WARNING)
        case "info":
            logger.setLevel(logging.INFO)
        case "debug":
            logger.setLevel(logging.DEBUG)
        case "silent":
            logger.disabled = True
        case _:
            logger.setLevel(logging.WARNING)
            logger.warning(f"Unknown verbosity: '{arguments.verbosity}'.")
    
    return logger