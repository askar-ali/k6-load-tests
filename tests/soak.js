import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL, thresholds } from '../lib/config.js';

// Moderate constant load for hours: finds leaks and slow degradation.
// Override length with: SOAK_DURATION=30m k6 run tests/soak.js
export const options = {
  stages: [
    { duration: '2m', target: 15 },
    { duration: __ENV.SOAK_DURATION || '2h', target: 15 },
    { duration: '2m', target: 0 },
  ],
  thresholds,
};

export default function () {
  check(http.get(`${BASE_URL}/api/items`), { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
