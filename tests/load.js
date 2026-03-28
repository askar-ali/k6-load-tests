import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL, thresholds } from '../lib/config.js';

// Baseline at expected traffic.
export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '2m', target: 20 },
    { duration: '30s', target: 0 },
  ],
  thresholds,
};

export default function () {
  const r = http.get(`${BASE_URL}/api/items`);
  check(r, { 'status 200': (res) => res.status === 200 });
  sleep(Math.random() * 1 + 0.5);
}
