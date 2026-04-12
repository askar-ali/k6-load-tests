#!/usr/bin/env python3
"""Compare two k6 --summary-export files and fail on regression.

Usage: compare-results.py BASELINE.json CURRENT.json [--max-latency-regress 20] [--max-error-rate 1]
Fails (exit 1) if p95 latency grew by more than the allowed percentage, or the
error rate exceeds the absolute limit. Prints a table either way.
"""
import argparse
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as f:
        m = json.load(f)["metrics"]
    return {
        "p95": m["http_req_duration"]["p(95)"],
        "avg": m["http_req_duration"]["avg"],
        "error_rate": m["http_req_failed"].get("value", m["http_req_failed"].get("rate", 0)) * 100,
        "rps": m["http_reqs"]["rate"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline")
    ap.add_argument("current")
    ap.add_argument("--max-latency-regress", type=float, default=20.0, help="allowed p95 growth, percent")
    ap.add_argument("--max-error-rate", type=float, default=1.0, help="absolute error rate limit, percent")
    a = ap.parse_args()

    base, cur = load(a.baseline), load(a.current)
    p95_change = (cur["p95"] - base["p95"]) / base["p95"] * 100 if base["p95"] else 0.0

    print(f"{'metric':<12}{'baseline':>12}{'current':>12}")
    for k in ("p95", "avg", "error_rate", "rps"):
        print(f"{k:<12}{base[k]:>12.2f}{cur[k]:>12.2f}")
    print(f"p95 change: {p95_change:+.1f}% (limit +{a.max_latency_regress:.0f}%)")

    failed = False
    if p95_change > a.max_latency_regress:
        print("FAIL: p95 latency regressed beyond the limit")
        failed = True
    if cur["error_rate"] > a.max_error_rate:
        print(f"FAIL: error rate {cur['error_rate']:.2f}% exceeds {a.max_error_rate}%")
        failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
