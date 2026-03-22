export const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8080';

export const thresholds = {
  http_req_failed: ['rate<0.01'],          // <1% errors
  http_req_duration: ['p(95)<300'],        // 95% under 300ms
  checks: ['rate>0.99'],
};
