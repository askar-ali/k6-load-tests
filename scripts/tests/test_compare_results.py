import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "compare-results.py")


def summary(p95, err=0.0, rps=50.0):
    return {"metrics": {
        "http_req_duration": {"p(95)": p95, "avg": p95 / 2},
        "http_req_failed": {"value": err},
        "http_reqs": {"rate": rps},
    }}


def run(base, cur, *extra):
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for name, data in (("b.json", base), ("c.json", cur)):
            path = os.path.join(d, name)
            with open(path, "w") as f:
                json.dump(data, f)
            paths.append(path)
        return subprocess.run([sys.executable, "-I", SCRIPT, *paths, *extra],
                              capture_output=True, text=True)


class CompareTests(unittest.TestCase):
    def test_same_results_pass(self):
        self.assertEqual(run(summary(100), summary(100)).returncode, 0)

    def test_small_slowdown_within_limit_passes(self):
        self.assertEqual(run(summary(100), summary(115)).returncode, 0)

    def test_large_slowdown_fails(self):
        r = run(summary(100), summary(150))
        self.assertEqual(r.returncode, 1)
        self.assertIn("p95 latency regressed", r.stdout)

    def test_error_rate_over_limit_fails(self):
        self.assertEqual(run(summary(100), summary(100, err=0.05)).returncode, 1)

    def test_custom_limit(self):
        self.assertEqual(run(summary(100), summary(150), "--max-latency-regress", "60").returncode, 0)


if __name__ == "__main__":
    unittest.main()
