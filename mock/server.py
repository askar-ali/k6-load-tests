"""Local target: /healthz, /api/items (small artificial latency)."""
import json
import random
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


TOKENS = set()
USERS = {"alice": "pw-alice", "bob": "pw-bob", "carol": "pw-carol"}


class H(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length) or b"{}")
        if self.path == "/login":
            if USERS.get(payload.get("user")) == payload.get("password"):
                token = f"tok-{random.getrandbits(48):x}"
                TOKENS.add(token)
                return self._send(200, {"token": token})
            return self._send(401, {"error": "bad credentials"})
        if self.path == "/api/orders":
            if self.headers.get("Authorization", "").removeprefix("Bearer ") not in TOKENS:
                return self._send(401, {"error": "unauthorized"})
            time.sleep(random.uniform(0.01, 0.05))
            return self._send(201, {"id": random.getrandbits(32), "items": payload.get("items", [])})
        return self._send(404, {"error": "not found"})

    def do_GET(self):
        if self.path == "/api/me":
            token = self.headers.get("Authorization", "").removeprefix("Bearer ")
            if token not in TOKENS:
                return self._send(401, {"error": "unauthorized"})
            return self._send(200, {"user": "ok"})
        if self.path == "/healthz":
            code, body = 200, {"status": "ok"}
        elif self.path.startswith("/api/items"):
            time.sleep(random.uniform(0.005, 0.03))
            code, body = 200, {"items": list(range(10))}
        else:
            code, body = 404, {"error": "not found"}
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8080), H).serve_forever()
