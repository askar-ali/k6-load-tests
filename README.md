# k6-load-tests

Performance baselines and capacity planning for client-facing services with k6.

> Lab recreation of the load-testing approach I use in production (since 10/2025).
> Runs against a local mock service by default; point `BASE_URL` at a real one.

## Test types

| Script | Purpose | Shape |
|--------|---------|-------|
| `tests/smoke.js` | Is the service up and sane? | 1 VU, 30s |
| `tests/load.js` | Baseline at expected traffic | ramp to 20 VUs, hold, ramp down |
| `tests/stress.js` | Find the breaking point | stepped ramp until thresholds fail |
| `tests/spike.js` | Survive and recover from a sudden 10x surge | 10 -> 100 -> 10 VUs |
| `tests/soak.js` | Find leaks and slow degradation | constant load for hours (`SOAK_DURATION`) |
| `tests/checkout-flow.js` | Realistic login -> browse -> order journey | per-VU users from CSV |

Every script enforces thresholds (p95 latency, error rate), so a regression fails the run.

## Usage

```bash
python3 mock/server.py &                 # local target on :8080
k6 run tests/smoke.js
BASE_URL=http://my-service k6 run tests/load.js
./run.sh load                            # saves JSON summary to results/
```

See `docs/capacity-plan.md` for turning results into a capacity number.
