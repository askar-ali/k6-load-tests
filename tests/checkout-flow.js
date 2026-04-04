import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';
import { BASE_URL, thresholds } from '../lib/config.js';

// Each VU logs in as a different user from the CSV, then browses and places an order.
const users = new SharedArray('users', () =>
  papaparse.parse(open('../data/users.csv'), { header: true }).data.filter((u) => u.user));

export const options = {
  vus: 6,
  duration: '30s',
  thresholds,
};

export default function () {
  const u = users[(__VU - 1) % users.length];
  let token;

  group('login', () => {
    const res = http.post(`${BASE_URL}/login`, JSON.stringify({ user: u.user, password: u.password }),
      { headers: { 'Content-Type': 'application/json' }, tags: { name: 'login' } });
    check(res, { 'login 200': (r) => r.status === 200 });
    token = res.json('token');
  });

  const auth = { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } };

  group('browse', () => {
    const res = http.get(`${BASE_URL}/api/items`, { ...auth, tags: { name: 'items' } });
    check(res, { 'items 200': (r) => r.status === 200 });
  });

  group('order', () => {
    const res = http.post(`${BASE_URL}/api/orders`, JSON.stringify({ items: [1, 2] }),
      { ...auth, tags: { name: 'order' } });
    check(res, { 'order 201': (r) => r.status === 201 });
  });
  sleep(1);
}
