# Streaming k6 metrics to Prometheus/Grafana

```bash
docker compose -f observability/docker-compose.yml up -d
export K6_PROMETHEUS_RW_SERVER_URL=http://localhost:9090/api/v1/write
export K6_PROMETHEUS_RW_TREND_STATS="p(95),p(99),avg,max"
./run.sh load
```
In Grafana (http://localhost:3000) query `k6_http_req_duration_p95`, `k6_http_reqs_total`,
`k6_vus`. Import the community "k6 Prometheus" dashboard (ID 19665) for a ready-made view.

Why: summaries only show the end result; streaming lets you see *when* latency degrades
and correlate it with CPU/memory of the service under test.
