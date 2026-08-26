import json
from product_normalizer.mapper import load_column_aliases, standardize_column_names
import pytest
from pandas.testing import assert_frame_equal
import pandas as pd
from product_normalizer.exceptions import FileReadError, InvalidDataError


def test_load_column_aliases(tmp_path):
    path = tmp_path / "aliases.json"
    expected = {
        "sku": ["sku", "seller sku"],
        "upc": ["upc", "upc code"],
    }
    path.write_text(
        json.dumps(expected),
        encoding="utf-8"
    )
    actual = load_column_aliases(path)
    assert actual == expected


def test_load_column_aliases_raises_when_file_missing(tmp_path):
    path = tmp_path / "not_exist.json"

    with pytest.raises(FileReadError):
        load_column_aliases(path)


def test_load_column_aliases_raises_when_json_invalid(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(
        "这不是合法JSON",
        encoding="utf-8"
    )
    with pytest.raises(InvalidDataError):
        load_column_aliases(path)


def test_standardize_column_names():
    aliases = {
        "sku": ["sku", "seller sku"],
        "upc": ["upc", "upc code"],
    }
    df = pd.DataFrame({
        " Seller SKU ": ["A001"],
        "UPC Code": ["001234"],
        "Price": ["9.99"],
    })
    actual = standardize_column_names(aliases, df)
    expected = pd.DataFrame({
        "sku": ["A001"],
        "upc": ["001234"],
        "Price": ["9.99"],
    })
    assert_frame_equal(actual, expected)
