"""Local web UI server — serves web/ and POST /api/convert via convert_units."""

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from convert_units import convert_units

WEB_DIR = Path(__file__).resolve().parent.parent / "web"
DEFAULT_PORT = 8080


class UnitConverterHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_POST(self):
        if self.path != "/api/convert":
            self.send_error(404, "Not Found")
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            payload = json.loads(body.decode("utf-8"))
            unit = payload["unit"]
            value = float(payload["value"])
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            self._send_json(400, {"status": "invalid", "failed_fields": ["parse"], "conversions": {}})
            return

        result = convert_units(unit, value)
        self._send_json(200, result)

    def _send_json(self, status_code, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        print(f"[web] {self.address_string()} - {format % args}")


def main():
    port = DEFAULT_PORT
    server = HTTPServer(("127.0.0.1", port), UnitConverterHandler)
    url = f"http://127.0.0.1:{port}"
    print(f"UnitConverter_20 web UI: {url}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
