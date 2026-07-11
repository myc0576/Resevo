"""Deprecated MCP filename wrapper; use ``mcp\resevo_mcp.py``."""

from __future__ import annotations

import sys

from resevo_mcp import main


if __name__ == "__main__":
    print("warning: 'research_harness_mcp.py' is deprecated; use 'resevo_mcp.py'.", file=sys.stderr)
    raise SystemExit(main())
