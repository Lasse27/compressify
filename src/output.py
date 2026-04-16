import importlib.metadata as meta
import datetime as dt

_scopes: list[str] = list()
_info: str = "[INFO]"
_warn: str = "[WARN]"
_show_timestamps: bool = False
_show_colorized: bool = False


HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKCYAN = "\033[96m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"


# Pushes a string as a scope into the output
def push_scope(scope: str):
    _scopes.append(scope)


# Pops the last scope from the output
def pop_scope():
    _scopes.pop()


# Enable or disable timestamps in the console output
def toggle_timestamps(toggle: bool):
    global _show_timestamps
    _show_timestamps = True


# Enable or disable colors in the console output
def toggle_colorized(toggle: bool):
    global _show_colorized
    _show_colorized = toggle


# Logs a string with the current configuration into the output console as info.
def log_info(message: str):

    if _show_timestamps:
        print(dt.datetime.now().strftime("%H:%m:%S:%f"), end=" ")

    if _show_colorized:
        print(OKCYAN, end="")

    print(_info, end=" ")

    if _show_colorized:
        print(ENDC, end="")

    for scope in _scopes:
        print(f"({scope})", end=" ")

    print(message)


# Logs a string with the current configuration into the output console as warn.
def log_warn(message: str):
    
    if _show_timestamps:
        print(dt.datetime.now().strftime("%H:%m:%S:%f"), end=" ")
        
    if _show_colorized:
        print(WARNING, end="")

    print(_warn, end=" ")

    if _show_colorized:
        print(ENDC, end="")
        
    print(message)


if __name__ == "__main__":
    toggle_colorized(True)
    toggle_timestamps(True)
    log_info("Hello World")
    log_warn("Hello World")
    push_scope("Now Scope")
    log_info("Hello World")
    pop_scope()
    log_info("Hello World")
