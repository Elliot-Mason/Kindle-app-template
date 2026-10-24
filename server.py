import json
import os
import socket
import sys
import time
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
CONFIG_EXAMPLE = os.path.join(BASE_DIR, "config.example.json")


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    if os.path.exists(CONFIG_EXAMPLE):
        try:
            with open(CONFIG_EXAMPLE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "poll_interval_ms": 30000,
        "app_title": "Kindle Starter Template",
        "port": 5053,
    }


def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print(f"[TemplateApp] Error saving config: {e}")


def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


class AppHTTPHandler(SimpleHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        cfg = load_config()

        if path in ("/", "/kindle"):
            client_path = os.path.join(BASE_DIR, "kindle.html")
            if os.path.exists(client_path):
                with open(client_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        if path == "/api/data":
            now_str = time.strftime("%I:%M %p")
            self.send_json({
                "success": True,
                "title": cfg.get("app_title", "Kindle Starter Template"),
                "valueA": int(time.time()) % 100,
                "status": "ONLINE",
                "time": now_str,
                "pollIntervalMs": cfg.get("poll_interval_ms", 30000),
                "lanIp": get_lan_ip(),
                "port": cfg.get("port", 5053),
            })
            return

        if path == "/api/config":
            self.send_json(cfg)
            return

        self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/config":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8", errors="replace")
            try:
                body = json.loads(raw) if raw else {}
                cfg = load_config()
                cfg.update(body)
                save_config(cfg)
                self.send_json({"success": True, "config": cfg})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=400)
            return

        self.send_error(404, "Not Found")


class ThreadedServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


def main():
    cfg = load_config()
    port = cfg.get("port", 5053)
    server = ThreadedServer(("0.0.0.0", port), AppHTTPHandler)
    lan_ip = get_lan_ip()
    print("=" * 60)
    print("  Kindle App Starter Server")
    print(f"  Local:   http://localhost:{port}/kindle")
    print(f"  Kindle:  http://{lan_ip}:{port}/kindle")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        server.server_close()


if __name__ == "__main__":
    main()
