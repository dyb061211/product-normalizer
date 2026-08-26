import pandas as pd
import logging

logger = logging.getLogger(__name__)


def merge_product_data(upc_df: pd.DataFrame, product_df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"开始合并数据：UPC{len(upc_df)}行，Products{len(product_df)}行")
    new_df = pd.merge(
        upc_df,
        product_df,
        on="sku",
        how="left"
    )
    logger.info(f"合并后数据{len(new_df)}行")
    return new_df
