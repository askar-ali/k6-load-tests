#!/usr/bin/env bash
# Usage: ./run.sh <smoke|load|stress>   Saves a JSON summary under results/.
set -euo pipefail
cd "$(dirname "$0")"

TEST="${1:?smoke|load|stress}"
[[ -f "tests/${TEST}.js" ]] || { echo "unknown test: $TEST" >&2; exit 1; }
command -v k6 >/dev/null || { echo "k6 not installed" >&2; exit 1; }

STAMP="$(date +%Y%m%d-%H%M%S)"
k6 run --summary-export "results/${TEST}-${STAMP}.json" "tests/${TEST}.js"
