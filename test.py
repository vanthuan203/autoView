import sys
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 80  # Bạn có thể thay đổi nếu cần

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Allow", "GET, OPTIONS")
        self.end_headers()

def add_firewall_rule(port: int, name: str = "AllowPythonPort"):
    python_path = sys.executable  # Lấy đường dẫn python.exe
    try:
        subprocess.run([
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name={name}",
            "dir=in",
            "action=allow",
            "protocol=TCP",
            f"localport={port}",
            f"program={python_path}",
            "enable=yes"
        ], check=True, shell=True)
        print(f"✅ Đã mở firewall cho {python_path} trên cổng {port}")
    except subprocess.CalledProcessError as e:
        print("❌ Không thể tạo rule firewall (cần quyền Admin)")
        print(e)

def run_server():
    with HTTPServer(("", PORT), QuietHandler) as httpd:
        print(f"🌐 Serving at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    add_firewall_rule(PORT)
    threading.Thread(target=run_server, daemon=True).start()
    
    print("🌀 Server đang chạy nền, nhấn Ctrl+C để dừng.")
    while True:
        pass  # Giữ chương trình sống
