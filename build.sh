#!/usr/bin/env bash
set -euo pipefail

PYTHON="python"
if [[ -x ".venv/bin/python" ]]; then
  PYTHON=".venv/bin/python"
fi

"$PYTHON" -m pip install -r requirements.txt
"$PYTHON" -m unittest discover
"$PYTHON" main.py
"$PYTHON" scripts/check_build_output.py
