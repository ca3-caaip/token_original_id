import pytest
from token_original_id.utils import sort_lines, check_whitespaces, check_duplication, check_value_format, lint_address


def test_sort_lines():
    assert sort_lines([
        "uti,platform,original_id",
        "btc,,btc",
        "eth,,eth",
        "btc,bsc,0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
        "eth,bsc,0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
    ]) == [
        "uti,platform,original_id",
        "btc,,btc",
        "btc,bsc,0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
        "eth,,eth",
        "eth,bsc,0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
    ]

def test_lint_address():
    assert lint_address([
        "uti,platform,original_id",
        "btc,,BTC",
        "eth,,ETH",
        "btc,bsc,0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
        "eth,bsc,0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
    ]) == [
        "uti,platform,original_id",
        "btc,,btc",
        "eth,,eth",
        "btc,bsc,0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c",
        "eth,bsc,0x2170ed0880ac9a755fd29b2688956bd959f933f8",
    ]

def test_check_whitespaces():
    with pytest.raises(Exception) as e:
        check_whitespaces(["btc,,btc "])
    assert (str(e.value)) == "Line:1: whitespace included"
    assert check_whitespaces(["btc,,btc"]) is None


def test_check_duplication():
    with pytest.raises(Exception) as e:
        check_duplication(["btc,,btc", "btc,,btc"])
    assert (str(e.value)) == "Lines duplicated"
    assert check_duplication(["btc,,btc", "eth,,eth"]) is None


def test_check_value_format():
    with pytest.raises(Exception) as e:
        check_value_format(["btc,bitcoin,btc"])
    assert (str(e.value)) == 'Line:1: platform should be empty where uti equals original_id'
    assert check_value_format(["btc,,btc"]) is None

    with pytest.raises(Exception) as e:
        check_value_format(["eth,,0x2170Ed0880ac9A755fd29B2688956BD959F933F8"])
    assert (str(e.value)) == 'Line:1: platform should not be empty where uti not equals original_id'
    assert check_value_format(["eth,bsc,0x2170Ed0880ac9A755fd29B2688956BD959F933F8"]) is None
