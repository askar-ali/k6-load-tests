#!/usr/bin/env bash
# Usage: ./run.sh <smoke|load|stress|spike|soak|checkout-flow>
# Saves a JSON summary under results/. Set BASELINE=<file> to gate on regressions.
# Set K6_PROMETHEUS_RW_SERVER_URL to stream metrics to Prometheus.
set -euo pipefail
cd "$(dirname "$0")"

TEST="${1:?smoke|load|stress}"
[[ -f "tests/${TEST}.js" ]] || { echo "unknown test: $TEST" >&2; exit 1; }
command -v k6 >/dev/null || { echo "k6 not installed" >&2; exit 1; }

STAMP="$(date +%Y%m%d-%H%M%S)"
CURRENT="results/${TEST}-${STAMP}.json"

# Optional: stream metrics to Prometheus remote-write (see docs/prometheus-output.md).
OUT_ARGS=()
if [[ -n "${K6_PROMETHEUS_RW_SERVER_URL:-}" ]]; then
  OUT_ARGS=(--out experimental-prometheus-rw)
fi

k6 run "${OUT_ARGS[@]}" --summary-export "$CURRENT" "tests/${TEST}.js"

# Optional: fail on regression against a stored baseline.
if [[ -n "${BASELINE:-}" ]]; then
  python3 -I scripts/compare-results.py "$BASELINE" "$CURRENT"
fi
