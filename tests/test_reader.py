import pandas as pd
import pytest
from product_normalizer.reader import read_excel_file
from product_normalizer.exceptions import FileReadError
from pandas.testing import assert_frame_equal


def test_read_excel_file_valid_excel(tmp_path):
    path = tmp_path / "test.xlsx"
    expected = pd.DataFrame({
        "sku": ["A001", "A002"],
        "upc": ["001", "002"],
    })
    expected.to_excel(path, index=False)
    actual = read_excel_file(path)
    assert_frame_equal(actual, expected)


def test_read_excel_file_raises_when_file_missing(tmp_path):
    path = tmp_path / "no_exist.xlsx"
    with pytest.raises(FileReadError):
        read_excel_file(path)
