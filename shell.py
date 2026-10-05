import sys
import hopsu
try:
    from _util import red, KINDS
except ImportError:
    from ._util import red, KINDS

__all__ = ("main",)


def main() -> None:
    print(f"Hopsu v{hopsu.__version__}")
    print("Commands: restart, exit")

    shell = hopsu.Hopsu()

    while True:
        try:
            code = input("\n>>> ").strip()
        except KeyboardInterrupt:
            continue
        except EOFError:
            sys.exit(0)

        match code:
            case "restart":
                shell.clear()
                print("Done.")
            case "exit":
                sys.exit(0)
            case _:
                try:
                    shell.run(code)
                except hopsu.HopsuError as e:
                    print(red(f"HopsuError: {KINDS.get(type(e), "other")}: {e}"), file=sys.stderr)
                except KeyboardInterrupt:
                    continue


if __name__ == "__main__":
    main()