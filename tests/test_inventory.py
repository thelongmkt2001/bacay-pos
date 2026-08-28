import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import db
import inventory


def test_restock():
    db.init_db()
    r = inventory.restock(1, 5)
    assert r["ok"]


def test_low_stock():
    rows = inventory.low_stock(10)
    assert rows is not None


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
