from pathlib import Path
import pandas as pd
import logging
from product_normalizer.exceptions import ProductNormalizerError
from product_normalizer.reader import read_excel_file
from product_normalizer.mapper import load_column_aliases, standardize_column_names
from product_normalizer.cleaner import normalize_upc_data, normalize_product_data, clean_upc_data, clean_product_data
from product_normalizer.merger import merge_product_data
from product_normalizer.exporter import export_standardized_data, export_validation_report
from product_normalizer.logging_config import setup_logging
from product_normalizer.validator import validate_required_columns, collect_empty_field_issues, \
    collect_duplicate_field_issues
from product_normalizer.settings import CONFIG_PATH, PRODUCTS_INPUT_PATH, UPC_INPUT_PATH, \
    STANDARDIZED_PRODUCTS_OUTPUT_PATH, VALIDATION_REPORT_PATH, UPC_REQUIRED_COLUMNS, PRODUCTS_REQUIRED_COLUMNS

logger = logging.getLogger(__name__)


def main() -> None:
    path_upc = UPC_INPUT_PATH
    path_products = PRODUCTS_INPUT_PATH
    output_path = STANDARDIZED_PRODUCTS_OUTPUT_PATH
    output_path_validation_report = VALIDATION_REPORT_PATH

    setup_logging()

    try:
        aliases = load_column_aliases(CONFIG_PATH)
        raw_df_upc = read_excel_file(path_upc)
        raw_df_products = read_excel_file(path_products)
        standardize_df_upc = standardize_column_names(aliases, raw_df_upc)
        standardize_df_products = standardize_column_names(aliases, raw_df_products)
        validate_required_columns(standardize_df_upc, UPC_REQUIRED_COLUMNS, "UPC")
        validate_required_columns(standardize_df_products, PRODUCTS_REQUIRED_COLUMNS, "Products")
        normalize_product = normalize_product_data(standardize_df_products)
        normalize_upc = normalize_upc_data(standardize_df_upc)
        df_empty_upc_sku = collect_empty_field_issues(normalize_upc, "sku", "UPC")
        df_empty_upc_upc = collect_empty_field_issues(normalize_upc, "upc", "UPC")
        df_duplicate_upc_sku = collect_duplicate_field_issues(normalize_upc, "sku", "UPC")
        df_duplicate_upc_upc = collect_duplicate_field_issues(normalize_upc, "upc", "UPC")
        df_empty_product_sku = collect_empty_field_issues(normalize_product, "sku", "Products")
        df_duplicate_product_sku = collect_duplicate_field_issues(normalize_product, "sku", "Products")
        issues = pd.concat([
            df_empty_upc_sku,
            df_empty_upc_upc,
            df_duplicate_upc_sku,
            df_duplicate_upc_upc,
            df_empty_product_sku,
            df_duplicate_product_sku
        ], ignore_index=True)
        export_validation_report(issues, output_path_validation_report)

    except ProductNormalizerError as e:
        logger.exception("程序失败")
        print(e)
        return

    clean_df_upc = clean_upc_data(normalize_upc)
    clean_df_products = clean_product_data(normalize_product)

    merged_df = merge_product_data(clean_df_upc, clean_df_products)
    export_standardized_data(merged_df, output_path)

    logger.info("product-normalizer 处理完成")


if __name__ == "__main__":
    main()
