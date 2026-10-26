"""Allow ``python -m mockloop.cli`` to run the command line tool."""

from mockloop.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
