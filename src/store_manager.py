"""
Store manager application
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
from urllib.parse import parse_qs
from views.template_view import show_main_menu
from http.server import BaseHTTPRequestHandler, HTTPServer
from views.user_view import show_user_form, register_user, remove_user
from views.product_view import show_product_form, register_product, remove_product
from views.order_view import show_order_form, register_order, remove_order
from views.report_view import show_highest_spending_users

class StoreManager(BaseHTTPRequestHandler):
    def do_GET(self):
        id = self.path.split("/")[-1]
        if self.path == "/" or self.path == "/home":
            self._send_html(show_main_menu())
            return
        if self.path == "/users":
            self._send_html(show_user_form())
        elif self.path.startswith("/users/remove/"):
            response = remove_user(id)
            self._send_html(response)
        elif self.path == "/products":
            self._send_html(show_product_form())
        elif self.path.startswith("/products/remove/"):
            response = remove_product(id)
            self._send_html(response)
        elif self.path == "/orders":
            self._send_html(show_order_form())
        elif self.path.startswith("/orders/remove/"):
            response = remove_order(id)
            self._send_html(response)
        elif self.path == "/orders/reports/highest_spenders":
            self._send_html(show_highest_spending_users())
        elif self.path == "/form.css":
            script_dir = os.path.dirname(__file__)
            # Serve CSS with the correct MIME type
            with open(script_dir + "/form.css", "r") as file:
                css = "".join(file.readlines())
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                self.wfile.write(css.encode("utf-8"))
        else:
            self._send_html("<h2>404 Page Not Found</h2>", status=404)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode("utf-8")
        params = parse_qs(body)
        if self.path == "/users/add":
            response = register_user(params)
            self._send_html(response)
        elif self.path == "/products/add":
            response = register_product(params)
            self._send_html(response)
        elif self.path == "/orders/add":
            response = register_order(params)
            self._send_html(response)
        else:
            self._send_html("<h2>404 Page Not Found</h2>", status=404)

    def _send_html(self, html, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5000), StoreManager)
    print("Server running on http://0.0.0.0:5000")
    server.serve_forever()
