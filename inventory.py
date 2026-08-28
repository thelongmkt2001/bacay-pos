import datetime
from db import get_db


def adjust_stock(product_id, new_stock):
    """Sua ton kho truc tiep - dung khi kiem ke."""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
    row = c.fetchone()
    if row is None:
        conn.close()
        return {"ok": False, "error": "khong tim thay san pham"}

    old = row["stock"]
    c.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
    c.execute(
        "INSERT INTO stock_log (product_id, delta, reason, created_at) VALUES (?,?,?,?)",
        (product_id, new_stock - old, "kiem ke", datetime.datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    return {"ok": True, "stock": new_stock}


def restock(product_id, qty):
    """Nhap them hang."""
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (qty, product_id))
    c.execute(
        "INSERT INTO stock_log (product_id, delta, reason, created_at) VALUES (?,?,?,?)",
        (product_id, qty, "nhap hang", datetime.datetime.now().isoformat()),
    )
    conn.commit()
    c.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
    stock = c.fetchone()["stock"]
    conn.close()
    return {"ok": True, "stock": stock}


def low_stock(threshold=10):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE stock < ? ORDER BY stock", (threshold,))
    out = [dict(r) for r in c.fetchall()]
    conn.close()
    return out
