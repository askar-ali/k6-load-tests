# Capacity planning from load-test results

## Method
1. Run `load.js` at several VU levels against a production-like environment.
2. Record per level: RPS, p95 latency, error rate, CPU/memory per pod.
3. The **sustainable capacity** is the highest RPS where p95 and error rate stay inside
   the thresholds in `lib/config.js`.
4. Run `stress.js` to find the breaking point; note which resource saturates first.

## Sizing formula
```
replicas = ceil( peak_rps * (1 + headroom) / rps_per_pod_at_threshold )
headroom = 0.3 to 0.5 (spikes, node loss, deploys)
```
Add one extra replica per failure domain you must survive losing.

## Results template (fill with real measurements)
| VUs | RPS | p95 (ms) | Error % | Pod CPU | Pod mem | Notes |
|-----|-----|----------|---------|---------|---------|-------|
|     |     |          |         |         |         |       |

> The smoke run against the local mock is only a harness check; its numbers say
> nothing about any real service.
