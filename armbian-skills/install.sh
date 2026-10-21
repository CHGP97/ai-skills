#!/usr/bin/env bash
# Install the Armbian suite from this checkout; no network or target-device access.
set -euo pipefail
armbian_suite_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$armbian_suite_dir/scripts/install_skills.py" "$@"
