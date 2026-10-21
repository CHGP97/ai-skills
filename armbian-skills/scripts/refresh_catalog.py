#!/usr/bin/env python3
"""Suite maintenance entry point; implementation lives beside canonical knowledge."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "knowledge/armbian/scripts/refresh_catalog.py"), run_name="__main__")
