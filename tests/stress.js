import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL } from '../lib/config.js';

// Step up load to find where latency/errors degrade. Thresholds abort the run.
export const options = {
  stages: [
    { duration: '1m', target: 50 },
    { duration: '1m', target: 100 },
    { duration: '1m', target: 200 },
    { duration: '1m', target: 400 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_failed: [{ threshold: 'rate<0.05', abortOnFail: true }],
    http_req_duration: [{ threshold: 'p(95)<1000', abortOnFail: true }],
  },
};

export default function () {
  const r = http.get(`${BASE_URL}/api/items`);
  check(r, { 'status 200': (res) => res.status === 200 });
  sleep(0.5);
}
