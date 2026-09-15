from pathlib import Path
import pandas as pd
from product_normalizer.mapper import load_column_aliases,standardize_column_names
from product_normalizer.reader import read_excel_file
from product_normalizer.settings import CONFIG_PATH,UPC_REQUIRED_COLUMNS,PRODUCTS_REQUIRED_COLUMNS
from product_normalizer.validator import validate_required_columns,collect_duplicate_field_issues,collect_empty_field_issues
from product_normalizer.cleaner import normalize_upc_data,normalize_product_data,clean_product_data,clean_upc_data
from product_normalizer.exporter import export_validation_report,export_standardized_data
from product_normalizer.merger import merge_product_data
from product_normalizer.repository import create_run,update_run_failed,update_run_success,save_validation_issues

def process_product_files(upc_path:Path,products_path:Path,output_path:Path,validation_report_path:Path,source:str,upc_filename:str|None=None,products_filename:str|None=None)->None:
    if upc_filename is None:
        upc_filename=upc_path.name
    if products_filename is None:
        products_filename=products_path.name
    run_id=create_run(source,upc_filename,products_filename)
    try:
        aliases = load_column_aliases(CONFIG_PATH)
        raw_df_upc = read_excel_file(upc_path)
        raw_df_products = read_excel_file(products_path)
        standardize_df_upc = standardize_column_names(aliases, raw_df_upc)
        standardize_df_products = standardize_column_names(aliases, raw_df_products)
        validate_required_columns(standardize_df_upc, UPC_REQUIRED_COLUMNS, "UPC")
        validate_required_columns(standardize_df_products, PRODUCTS_REQUIRED_COLUMNS, "Products")
        normalize_upc = normalize_upc_data(standardize_df_upc)
        normalize_products = normalize_product_data(standardize_df_products)
        df_empty_upc_sku = collect_empty_field_issues(normalize_upc, "sku", "UPC")
        df_empty_upc_upc = collect_empty_field_issues(normalize_upc, "upc", "UPC")
        df_duplicate_upc_sku = collect_duplicate_field_issues(normalize_upc, "sku", "UPC")
        df_duplicate_upc_upc = collect_duplicate_field_issues(normalize_upc, "upc", "UPC")
        df_empty_product_sku = collect_empty_field_issues(normalize_products, "sku", "Products")
        df_duplicate_product_sku = collect_duplicate_field_issues(normalize_products, "sku", "Products")
        issues = pd.concat([
            df_empty_upc_sku,
            df_empty_upc_upc,
            df_duplicate_upc_sku,
            df_duplicate_upc_upc,
            df_empty_product_sku,
            df_duplicate_product_sku
        ], ignore_index=True)
        export_validation_report(issues, validation_report_path)
        clean_df_upc = clean_upc_data(normalize_upc)
        clean_df_products = clean_product_data(normalize_products)
        merged_df = merge_product_data(clean_df_upc, clean_df_products)
        export_standardized_data(merged_df, output_path)
        save_validation_issues(run_id, issues)
        update_run_success(run_id,len(raw_df_upc),len(raw_df_products),len(merged_df),len(issues))
    except Exception as e:
        update_run_failed(run_id,str(e))
        raise