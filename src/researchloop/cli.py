"""Deprecated compatibility import for the old ResearchLoop CLI."""

from resevo.compat import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
