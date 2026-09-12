import datetime
from db import get_db


def adjust_stock(product_id, new_stock):
    """Sửa tồn kho trực tiếp - dùng khi kiểm kê."""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
    row = c.fetchone()
    if row is None:
        conn.close()
        return {"ok": False, "error": "không tìm thấy sản phẩm"}

    old = row["stock"]
    c.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
    c.execute(
        "INSERT INTO stock_log (product_id, delta, reason, created_at) VALUES (?,?,?,?)",
        (product_id, new_stock - old, "kiểm kê", datetime.datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    return {"ok": True, "stock": new_stock}


def restock(product_id, qty):
    """Nhập thêm hàng."""
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (qty, product_id))
    c.execute(
        "INSERT INTO stock_log (product_id, delta, reason, created_at) VALUES (?,?,?,?)",
        (product_id, qty, "nhập hàng", datetime.datetime.now().isoformat()),
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
