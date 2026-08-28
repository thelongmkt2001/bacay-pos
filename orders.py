import datetime
from db import get_db


def create_order(store, product_id, qty):
    """Tao don hang moi va tru ton kho."""
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    p = c.fetchone()
    if p is None:
        conn.close()
        return {"ok": False, "error": "khong tim thay san pham"}

    if p["stock"] < qty:
        conn.close()
        return {"ok": False, "error": "het hang"}

    now = datetime.datetime.now().isoformat()
    c.execute("INSERT INTO orders (store, created_at) VALUES (?,?)", (store, now))
    order_id = c.lastrowid

    c.execute(
        "INSERT INTO order_lines (order_id, product_id, qty) VALUES (?,?,?)",
        (order_id, product_id, qty),
    )

    c.execute("SELECT price FROM products WHERE id = ?", (product_id,))
    price = c.fetchone()["price"]
    total = price * qty

    c.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, product_id))
    c.execute(
        "INSERT INTO stock_log (product_id, delta, reason, created_at) VALUES (?,?,?,?)",
        (product_id, -qty, "ban hang", now),
    )

    conn.commit()
    conn.close()
    return {"ok": True, "order_id": order_id, "total": total}


def list_orders(limit=50):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        """SELECT o.id, o.store, o.created_at,
                  p.name, l.qty, p.price
           FROM orders o
           JOIN order_lines l ON l.order_id = o.id
           JOIN products p ON p.id = l.product_id
           ORDER BY o.id DESC LIMIT ?""",
        (limit,),
    )
    rows = []
    for r in c.fetchall():
        rows.append(
            {
                "id": r["id"],
                "store": r["store"],
                "created_at": r["created_at"],
                "product": r["name"],
                "qty": r["qty"],
                "total": r["price"] * r["qty"],
            }
        )
    conn.close()
    return rows


def revenue_report():
    """Tong doanh thu theo cua hang."""
    conn = get_db()
    c = conn.cursor()
    c.execute(
        """SELECT o.store, SUM(p.price * l.qty) as doanh_thu, COUNT(DISTINCT o.id) as so_don
           FROM orders o
           JOIN order_lines l ON l.order_id = o.id
           JOIN products p ON p.id = l.product_id
           GROUP BY o.store"""
    )
    out = [dict(r) for r in c.fetchall()]
    conn.close()
    return out
