import json
import os
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

import db
import orders
import inventory
import menu
import config

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n == 0:
            return {}
        return json.loads(self.rfile.read(n).decode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/" or path == "/index.html":
            f = os.path.join(STATIC_DIR, "index.html")
            data = open(f, "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        if path == "/api/products":
            conn = db.get_db()
            rows = [dict(r) for r in conn.execute("SELECT * FROM products ORDER BY id")]
            conn.close()
            return self._json(rows)

        if path == "/api/orders":
            return self._json(orders.list_orders())

        if path == "/api/reports/revenue":
            return self._json(orders.revenue_report())

        if path == "/api/inventory/low":
            return self._json(inventory.low_stock(config.LOW_STOCK_THRESHOLD))

        if path == "/api/menu":
            return self._json(menu.get_menu())

        if path == "/api/stores":
            return self._json(db.STORES)

        self._json({"error": "not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            body = self._body()
        except Exception:
            return self._json({"ok": False, "error": "body không hợp lệ"}, 400)

        if path == "/api/orders":
            r = orders.create_order(
                body.get("store", "Quận 1"),
                int(body["product_id"]),
                int(body.get("qty", 1)),
            )
            return self._json(r, 200 if r.get("ok") else 400)

        if path == "/api/inventory/adjust":
            r = inventory.adjust_stock(int(body["product_id"]), int(body["stock"]))
            return self._json(r)

        if path == "/api/inventory/restock":
            r = inventory.restock(int(body["product_id"]), int(body["qty"]))
            return self._json(r)

        if path == "/api/menu/price":
            r = menu.update_menu_price(int(body["item_id"]), float(body["price"]))
            return self._json(r)

        if path == "/api/products/price":
            conn = db.get_db()
            conn.execute(
                "UPDATE products SET price = ? WHERE id = ?",
                (float(body["price"]), int(body["product_id"])),
            )
            conn.commit()
            conn.close()
            return self._json({"ok": True})

        self._json({"error": "not found"}, 404)

    def log_message(self, fmt, *args):
        pass


def main():
    db.init_db()
    server = ThreadingHTTPServer(("127.0.0.1", config.POS_PORT), Handler)
    print("Ba Cay POS dang chay: http://127.0.0.1:%d" % config.POS_PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()
