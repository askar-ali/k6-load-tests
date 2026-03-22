"""Local target: /healthz, /api/items (small artificial latency)."""
import json
import random
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class H(BaseHTTPRequestHandler):
    def do_GET(self):
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
