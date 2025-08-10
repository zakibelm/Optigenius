#!/usr/bin/env bash
set -euo pipefail

echo "Running ruff..."
python -m ruff check .

echo "Running black --check..."
python -m black --check .

echo "Running pytest..."
python -m pytest -q
