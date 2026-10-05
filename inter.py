from argparse import ArgumentParser
import sys
import hopsu
try:
    from _util import red, KINDS
except ImportError:
    from ._util import red, KINDS

__all__ = ("main",)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("input", help="input file's path")
    parser.add_argument("--encoding", default="UTF-8", help="input file's encoding")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding=args.encoding) as f:
            code = f.read()
    except (OSError, UnicodeDecodeError, LookupError) as e:
        print(red(f"Error: {type(e).__name__}: {e}"), file=sys.stderr)
        sys.exit(1)

    inter = hopsu.Hopsu()
    try:
        inter.run(code)
    except hopsu.HopsuError as e:
        print(red(f"HopsuError: {KINDS.get(type(e), "other")}: {e}"), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()