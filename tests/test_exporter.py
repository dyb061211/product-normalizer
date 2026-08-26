import pandas as pd
from pandas.testing import assert_frame_equal
from product_normalizer.exporter import export_standardized_data, export_validation_report


def test_export_standardized_data_writes_expected_excel(tmp_path):
    path = tmp_path / "standardized.xlsx"
    df = pd.DataFrame({
        "product_name": ["Chair"],
        "sku": ["A001"],
        "upc": ["001234"],
        "brand": [None],
    })
    export_standardized_data(df, path)
    assert path.exists()
    actual = pd.read_excel(
        path,
        dtype=str,
        keep_default_na=False
    )
    expected = pd.DataFrame({
        "sku": ["A001"],
        "upc": ["001234"],
        "product_name": ["Chair"],
        "brand": [""],
        "material": [""],
        "color": [""],
        "size": [""],
        "source_url": [""],
        "notes": [""],
    })
    assert_frame_equal(actual, expected)


def test_export_validation_report_keeps_headers_when_empty(tmp_path):
    path = tmp_path / "validation_report.xlsx"
    issues = pd.DataFrame()
    export_validation_report(
        issues,
        path,
    )
    assert path.exists()
    actual = pd.read_excel(
        path,
        keep_default_na=False,
    )
    expected_columns = [
        "source",
        "row_number",
        "field",
        "value",
        "error_type",
        "message",
    ]
    assert list(actual.columns) == expected_columns
    assert len(actual) == 0
