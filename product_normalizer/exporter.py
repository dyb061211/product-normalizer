import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def export_standardized_data(df: pd.DataFrame, output_path: Path) -> None:
    logger.info("开始导出")
    final_columns = [
        "sku",
        "upc",
        "product_name",
        "brand",
        "material",
        "color",
        "size",
        "source_url",
        "notes",
    ]
    df = df.reindex(columns=final_columns)
    df = df.fillna("")
    df.to_excel(
        output_path,
        index=False
    )
    logger.info(f"导出成功到{output_path}")


def export_validation_report(df: pd.DataFrame, output_path: Path) -> None:
    logger.info(f"开始导出校验报告，共{len(df)}条问题")
    final_columns = [
        "source",
        "row_number",
        "field",
        "value",
        "error_type",
        "message"
    ]
    df = df.reindex(columns=final_columns)
    df.to_excel(
        output_path,
        index=False
    )
    logger.info(f"校验报告导出成功：{output_path}")
