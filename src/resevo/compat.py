"""Deprecated ``researchloop`` console entrypoint."""

from __future__ import annotations

import sys

from .cli import main as _main


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    print("warning: 'researchloop' is deprecated; use 'resevo' instead.", file=sys.stderr)
    return _main(args)


if __name__ == "__main__":
    raise SystemExit(main())
