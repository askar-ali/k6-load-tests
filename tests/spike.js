import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL } from '../lib/config.js';

// Sudden 10x surge, then recovery. Verifies the service survives and recovers.
export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '10s', target: 100 },   // spike
    { duration: '1m', target: 100 },
    { duration: '10s', target: 10 },    // drop
    { duration: '1m', target: 10 },     // recovery window
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<800'],
  },
};

export default function () {
  check(http.get(`${BASE_URL}/api/items`), { 'status 200': (r) => r.status === 200 });
  sleep(0.3);
}
