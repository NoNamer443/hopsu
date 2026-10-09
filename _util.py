import sys
import hopsu

KINDS: dict[type[Exception], str] = {
    hopsu.HopsuStackError: "stack",
    hopsu.HopsuSyntaxError: "syntax",
}


def red(s: str) -> str:
    if sys.stderr.isatty():
        return f"\033[31m{s}\033[0m"
    return s
