import pandas as pd
import pytest
from product_normalizer.validator import validate_required_columns, collect_empty_field_issues, \
    collect_duplicate_field_issues
from product_normalizer.exceptions import MissingRequiredColumnError
from pandas.testing import assert_frame_equal


def test_validate_required_columns_passes_when_columns_exist():
    df = pd.DataFrame({
        "sku": ["A001"],
        "upc": ["001234"]
    })
    validate_required_columns(df, ["sku", "upc"], "UPC")


def test_validate_required_columns_raises_when_columns_missing():
    df = pd.DataFrame({
        "upc": ["001234"]
    })
    with pytest.raises(MissingRequiredColumnError):
        validate_required_columns(df, ["sku", "upc"], "UPC")


def test_validate_required_columns_error_message():
    df = pd.DataFrame({
        "upc": ["001234"]
    })
    with pytest.raises(MissingRequiredColumnError) as e:
        validate_required_columns(df, ["sku", "upc"], "UPC")
    assert "sku" in str(e.value)


def test_collect_empty_field_issues_finds_empty_sku():
    df = pd.DataFrame({
        "sku": ["A001", "", "A003"],
        "upc": ["001", "002", "003"],
    })
    actual = collect_empty_field_issues(df, "sku", "UPC")
    expected = pd.DataFrame([
        {
            "source": "UPC",
            "row_number": 3,
            "field": "sku",
            "value": "",
            "error_type": "EMPTY_VALUE",
            "message": "sku不能为空",
        }
    ])
    assert_frame_equal(actual, expected)


def test_collect_duplicate_field_issues_returns_empty_when_no_issue():
    df = pd.DataFrame({
        "sku": ["A001", "A002", "A003"],
    })
    issues = collect_duplicate_field_issues(df, "sku", "UPC")
    assert len(issues) == 0


def test_collect_duplicate_field_issues_finds_all_duplicates():
    df = pd.DataFrame({
        "sku": [
            "A001",
            "A002",
            "A001",
        ]
    })
    actual = collect_duplicate_field_issues(df, "sku", "UPC")
    expected = pd.DataFrame([
        {
            "source": "UPC",
            "row_number": 2,
            "field": "sku",
            "value": "A001",
            "error_type": "DUPLICATE",
            "message": "sku重复",
        },
        {
            "source": "UPC",
            "row_number": 4,
            "field": "sku",
            "value": "A001",
            "error_type": "DUPLICATE",
            "message": "sku重复",
        },
    ])
    assert_frame_equal(actual, expected)


def test_collect_duplicate_field_issues_ignores_empty_values():
    df = pd.DataFrame({
        "sku": ["", "", "A001"],
    })
    issues = collect_duplicate_field_issues(df, "sku", "UPC")
    assert len(issues) == 0
