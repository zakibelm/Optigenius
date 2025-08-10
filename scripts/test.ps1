#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Running ruff..."
python -m ruff check .

Write-Host "Running black --check..."
python -m black --check .

Write-Host "Running pytest..."
python -m pytest -q
