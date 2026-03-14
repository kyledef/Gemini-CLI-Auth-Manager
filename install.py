#!/usr/bin/env python3
"""Compatibility installer shim.

Preferred workflow:
1) uv tool install .
2) gchange setup
"""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    print("[Deprecated] install.py is kept for compatibility.")
    print("[Recommended] Run: uv tool install . && gchange setup")

    script = Path(__file__).resolve().with_name("gemini_cli_auth_manager.py")
    cmd = [sys.executable, str(script), "setup"]
    return subprocess.run(cmd, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
