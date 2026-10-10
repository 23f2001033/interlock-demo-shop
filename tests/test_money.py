from shop.money import apply_rate, format_money


def test_format_money():
    assert format_money(0) == "$0.00"
    assert format_money(5) == "$0.05"
    assert format_money(1999) == "$19.99"
    assert format_money(123450) == "$1,234.50"
    assert format_money(-250) == "-$2.50"


def test_apply_rate_rounds_half_up():
    assert apply_rate(3998, 0.0725) == 290  # 289.855
    assert apply_rate(200, 0.0725) == 15  # 14.5
    assert apply_rate(1250, 0.04) == 50
    assert type(apply_rate(995, 0.19)) is int
