from product_normalizer.cleaner import normalize_text, normalize_upc, clean_upc_data, clean_product_data
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal


@pytest.mark.parametrize(
    "value,expected",
    [
        (" A001 ", "A001"),
        (None, ""),
        (123, "123"),
        ("A001", "A001"),
    ],
)
def test_normalize_text(value, expected):
    result = normalize_text(value)
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (" 001234 ", "001234"),
        ("001 234", "001234"),
        ("001234.0", "001234"),
        ("001234.000", "001234"),
        ("001234.001", "001234.001"),
        (None, ""),
    ],
)
def test_normalize_uoc(value, expected):
    result = normalize_upc(value)
    assert result == expected


def test_clean_upc_data_removes_empty_and_duplicate_sku():
    df = pd.DataFrame({
        "sku": [
            "A001",
            "",
            "A002",
            "A001",
        ],
        "upc": [
            "001",
            "002",
            "003",
            "004",
        ],
    })
    actual = clean_upc_data(df)
    expected = pd.DataFrame({
        "sku": [
            "A001",
            "A002",
        ],
        "upc": [
            "001",
            "003",
        ],
    })
    assert_frame_equal(actual, expected)


def test_clean_product_data_removes_empty_and_duplicate_sku():
    df = pd.DataFrame({
        "sku": [
            "A001",
            "",
            "A002",
            "A001",
        ],
        "product_name": [
            "Chair",
            "Bad Product",
            "Table",
            "Another Chair",
        ],
    })
    actual = clean_product_data(df)
    expected = pd.DataFrame({
        "sku": [
            "A001",
            "A002",
        ],
        "product_name": [
            "Chair",
            "Table",
        ],
    })
    assert_frame_equal(actual, expected)


def test_clean_upc_data_keeps_valid_rows():
    df = pd.DataFrame({
        "sku": [
            "A001",
            "A002",
        ],
        "upc": [
            "001",
            "002",
        ],
    })
    actual = clean_upc_data(df)
    expected = pd.DataFrame({
        "sku": [
            "A001",
            "A002",
        ],
        "upc": [
            "001",
            "002",
        ],
    })
    assert_frame_equal(actual, expected)
