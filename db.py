import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "bacay.db")


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        unit TEXT,
        price REAL,
        stock INTEGER
    )""")

    # bảng menu - thêm sau khi làm trang menu
    c.execute("""CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price REAL,
        category TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store TEXT,
        created_at TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS order_lines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        qty INTEGER
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS stock_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        delta INTEGER,
        reason TEXT,
        created_at TEXT
    )""")

    conn.commit()

    c.execute("SELECT COUNT(*) as n FROM products")
    if c.fetchone()["n"] == 0:
        seed(conn)

    conn.close()


def seed(conn):
    c = conn.cursor()
    products = [
        ("Cà phê sữa đá", "ly", 25000, 40),
        ("Cà phê đen đá", "ly", 20000, 35),
        ("Bạc xỉu", "ly", 30000, 25),
        ("Trà đào cam sả", "ly", 45000, 12),
        ("Bánh mì thịt", "cái", 35000, 8),
        ("Croissant", "cái", 40000, 5),
        ("Cà phê hạt rang", "kg", 250000, 3),
    ]
    c.executemany(
        "INSERT INTO products (name, unit, price, stock) VALUES (?,?,?,?)", products
    )

    # trang menu dùng bảng riêng
    items = [
        ("Cà phê sữa đá", 25000, "đồ uống"),
        ("Cà phê đen đá", 20000, "đồ uống"),
        ("Bạc xỉu", 30000, "đồ uống"),
        ("Trà đào cam sả", 42000, "đồ uống"),
        ("Bánh mì thịt", 35000, "đồ ăn"),
    ]
    c.executemany("INSERT INTO items (title, price, category) VALUES (?,?,?)", items)

    conn.commit()


STORES = ["Quận 1", "Quận 3", "Quận 7", "Thủ Đức", "Bình Thạnh", "Gò Vấp"]
