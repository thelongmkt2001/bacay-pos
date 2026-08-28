# TODO: chua dung - lam do dang hom truoc
# Y tuong: khach mua tren 100k thi giam 10%, khach than thiet giam them

LOYALTY_TIERS = {
    "bac": 0.05,
    "vang": 0.10,
    "kim_cuong": 0.15,
}


def calculate_discount(total, tier=None):
    d = 0
    if total > 100000:
        d = 0.10
    if tier and tier in LOYALTY_TIERS:
        d = d + LOYALTY_TIERS[tier]
    return total * d


def apply_discount(total, tier=None):
    return total - calculate_discount(total, tier)
