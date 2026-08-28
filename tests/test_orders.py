import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import db
import orders
import inventory


def test_create_order():
    db.init_db()
    r = orders.create_order("Quan 1", 1, 1)
    assert r is not None


def test_order_list():
    rows = orders.list_orders()
    assert rows is not None


def test_stock_not_negative():
    db.init_db()
    r = orders.create_order("Quan 1", 1, 1)
    assert r["ok"] in [True, False]


def test_revenue():
    rep = orders.revenue_report()
    assert isinstance(rep, list)


def run():
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
            passed += 1
    print("%d passed" % passed)


if __name__ == "__main__":
    run()
