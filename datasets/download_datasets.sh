#!/usr/bin/env bash
set -euo pipefail

mkdir -p raw

if [[ -f raw/README.txt ]]; then
  echo "Datasets already downloaded."
  exit 0
fi

echo "Placeholder download script. Add dataset sources as needed." > raw/README.txt
