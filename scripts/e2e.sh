#!/usr/bin/env bash
set -euo pipefail
export E2E_BASE_URL="${E2E_BASE_URL:-https://api.optigenius.pro}"
pytest -k e2e
