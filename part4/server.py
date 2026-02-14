"""
Part 4 - Local server: serves static files and proxies /api/* to Part 3 (port 5000).
Run from part4 folder: python server.py
Then open http://127.0.0.1:8000/
No CORS issues because browser talks only to this server.
"""
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

API_BACKEND = "http://127.0.0.1:5000"
PORT = 8000


class ProxyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/"):
            self._proxy_request()
        else:
            # First page = login; then after login user goes to index.html (Places)
            path_only = self.path.split("?")[0] if "?" in self.path else self.path
            if path_only.rstrip("/") == "":
                self.path = "/login.html" + (self.path[self.path.index("?"):] if "?" in self.path else "")
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            self._proxy_request()
        else:
            super().do_POST()

    def do_PUT(self):
        if self.path.startswith("/api/"):
            self._proxy_request()
        else:
            self.send_error(404)

    def do_DELETE(self):
        if self.path.startswith("/api/"):
            self._proxy_request()
        else:
            self.send_error(404)

    def _proxy_request(self):
        url = API_BACKEND + self.path
        if self.command == "GET" and "?" in self.path:
            pass  # query string already in path
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else None
            req = urllib.request.Request(
                url,
                data=body,
                method=self.command,
                headers={k: v for k, v in self.headers.items() if k.lower() not in ("host", "connection")},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() not in ("transfer-encoding", "connection"):
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(resp.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            try:
                self.wfile.write(e.read())
            except Exception:
                pass
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Proxy error: Part 3 API not reachable ({e})".encode())


if __name__ == "__main__":
    server = HTTPServer(("", PORT), ProxyHandler)
    print(f"Serving Part 4 at http://127.0.0.1:{PORT}/  (API proxied to {API_BACKEND})")
    server.serve_forever()
