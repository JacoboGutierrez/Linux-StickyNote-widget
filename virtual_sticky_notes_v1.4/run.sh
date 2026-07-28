#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -d "$ROOT/.venv" ]]; then
  python3 -m venv "$ROOT/.venv"
  "$ROOT/.venv/bin/python" -m pip install --upgrade pip
  "$ROOT/.venv/bin/pip" install -r "$ROOT/requirements.txt"
fi

exec "$ROOT/.venv/bin/python" "$ROOT/main.py"
