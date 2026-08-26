import pandas as pd
from pandas.testing import assert_frame_equal
from product_normalizer.merger import merge_product_data


def test_merge_product_data_matches_by_sku():
    upc_df = pd.DataFrame({
        "sku": ["A001", "A002"],
        "upc": ["001", "002"],
    })
    product_df = pd.DataFrame({
        "sku": ["A001", "A002"],
        "product_name": ["Chair", "Table"],
    })
    actual = merge_product_data(upc_df, product_df)
    expected = pd.DataFrame({
        "sku": ["A001", "A002"],
        "upc": ["001", "002"],
        "product_name": ["Chair", "Table"],
    })
    assert_frame_equal(actual, expected)


def test_merge_product_data_keeps_unmatched_upc_rows():
    upc_df = pd.DataFrame({
        "sku": ["A001", "A999"],
        "upc": ["001", "999"],
    })
    product_df = pd.DataFrame({
        "sku": ["A001"],
        "product_name": ["Chair"],
    })
    actual = merge_product_data(
        upc_df,
        product_df,
    )
    assert len(actual) == 2
    assert actual.loc[0, "product_name"] == "Chair"
    assert pd.isna(actual.loc[1, "product_name"])
