"""
Store manager application
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from views.user_view import show_user_form
from views.product_view import show_product_form
from views.order_view import show_order_form

class StoreManager(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/users":
            self._send_html(show_user_form())
        elif self.path == "/products":
            self._send_html(show_product_form())
        elif self.path == "/orders":
            self._send_html(show_order_form())
        else:
            self._send_html("<h1>404 Page Not Found</h1>", status=404)

    def do_POST(self):
        if self.path == "/":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode("utf-8")
            params = parse_qs(body)
            name = params.get("name", ["stranger"])[0]
            self._send_html(f"""
                <h1>Hello, {name}!</h1>
                <a href="/">Back to form</a>
            """)
        else:
            self._send_html("<h1>404 Page Not Found</h1>", status=404)

    def _send_html(self, html, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5000), StoreManager)
    print("Server running on http://0.0.0.0:5000")
    server.serve_forever()
