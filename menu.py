from db import get_db


def get_menu():
    """Danh sách món cho trang menu."""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY category, title")
    out = [dict(r) for r in c.fetchall()]
    conn.close()
    return out


def update_menu_price(item_id, price):
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE items SET price = ? WHERE id = ?", (price, item_id))
    conn.commit()
    conn.close()
    return {"ok": True}
