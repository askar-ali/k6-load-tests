import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL, thresholds } from '../lib/config.js';

export const options = { vus: 1, duration: '30s', thresholds };

export default function () {
  const health = http.get(`${BASE_URL}/healthz`);
  check(health, { 'health 200': (r) => r.status === 200 });

  const items = http.get(`${BASE_URL}/api/items`);
  check(items, { 'items 200': (r) => r.status === 200 });
  sleep(1);
}
