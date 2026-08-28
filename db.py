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

    # bang menu - them sau khi lam trang menu
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
        ("Ca phe sua da", "ly", 25000, 40),
        ("Ca phe den da", "ly", 20000, 35),
        ("Bac xiu", "ly", 30000, 25),
        ("Tra dao cam sa", "ly", 45000, 12),
        ("Banh mi thit", "cai", 35000, 8),
        ("Croissant", "cai", 40000, 5),
        ("Ca phe hat rang", "kg", 250000, 3),
    ]
    c.executemany(
        "INSERT INTO products (name, unit, price, stock) VALUES (?,?,?,?)", products
    )

    # menu page dung bang rieng
    items = [
        ("Ca phe sua da", 25000, "do uong"),
        ("Ca phe den da", 20000, "do uong"),
        ("Bac xiu", 30000, "do uong"),
        ("Tra dao cam sa", 42000, "do uong"),
        ("Banh mi thit", 35000, "do an"),
    ]
    c.executemany("INSERT INTO items (title, price, category) VALUES (?,?,?)", items)

    conn.commit()


STORES = ["Quan 1", "Quan 3", "Quan 7", "Thu Duc", "Binh Thanh", "Go Vap"]
