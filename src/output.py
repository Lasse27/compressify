import datetime as dt

INFO: str = "[INFO]"
WARN: str = "[WARN]"
LEVEL_CHAR_LEN: int = len(INFO)
HEADER: str = "\033[95m"
OKBLUE: str = "\033[94m"
OKCYAN: str = "\033[96m"
OKGREEN: str = "\033[92m"
WARNING: str = "\033[93m"
FAIL: str = "\033[91m"
ENDC: str = "\033[0m"
BOLD: str = "\033[1m"
UNDERLINE: str = "\033[4m"


class Console:
    _scopes: list[str] = list()
    _scopes_char_len: int = 0
    _show_timestamps: bool = False
    _show_colorized: bool = False
    _show_output: bool = False

    # Pushes a string as a scope into the output
    def push_scope(self, scope: str):
        self._scopes.append(scope)
        self._scopes_char_len += len(scope)

    # Pops the last scope from the output
    def pop_scope(self):
        scope = self._scopes.pop()
        self._scopes_char_len -= len(scope)

    def toggle_output(self, toggle: bool):
        self._show_output = toggle

    # Enable or disable timestamps in the console output
    def toggle_timestamps(self, toggle: bool):
        self._show_timestamps = toggle

    # Enable or disable colors in the console output
    def toggle_colorized(self, toggle: bool):
        self._show_colorized = toggle

    # Logs a string with the current configuration into the output console as raw text.
    def log_raw(self, message: str):
        if not self._show_output:
            return

        print(LEVEL_CHAR_LEN * " ", end=" ")
        if self._scopes_char_len > 0:
            print(self._scopes_char_len * " ", end=" ")

        print(message)

    # Logs a string with the current configuration into the output console as info.
    def log_info(self, message: str):
        if not self._show_output:
            return

        if self._show_timestamps:
            print(dt.datetime.now().strftime("%H:%m:%S:%f"), end=" ")

        if self._show_colorized:
            print(OKCYAN, end="")

        print(INFO, end=" ")

        if self._show_colorized:
            print(ENDC, end="")

        for scope in self._scopes:
            print(f"({scope})", end=" ")

        print(message)

    # Logs a string with the current configuration into the output console as warn.
    def log_warn(self, message: str):

        if not self._show_output:
            return

        if self._show_timestamps:
            print(dt.datetime.now().strftime("%H:%m:%S:%f"), end=" ")

        if self._show_colorized:
            print(WARNING, end="")

        print(WARN, end=" ")

        if self._show_colorized:
            print(ENDC, end="")

        print(message)

    def simple_prompt(self, prompt: str) -> bool:

        print(LEVEL_CHAR_LEN * " ", end=" ")
        if self._scopes_char_len > 0:
            print(self._scopes_char_len * " ", end=" ")

        print(f"> {prompt} [y, N]")

        print(LEVEL_CHAR_LEN * " ", end=" ")
        if self._scopes_char_len > 0:
            print(self._scopes_char_len * " ", end=" ")

        try:
            key = input("> ")
            if key != "y" and key != "Y":
                return True
            return False
        except KeyboardInterrupt:
            exit(-1)
