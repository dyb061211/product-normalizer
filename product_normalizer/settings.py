from pathlib import Path

PROHECT_ROOT: Path = Path(__file__).resolve().parent.parent

CONFIG_PATH: Path = (PROHECT_ROOT / "config" / "column_aliases.json")
UPC_INPUT_PATH: Path = (PROHECT_ROOT / "data" / "input" / "upc.xlsx")
PRODUCTS_INPUT_PATH: Path = (PROHECT_ROOT / "data" / "input" / "products.xlsx")
STANDARDIZED_PRODUCTS_OUTPUT_PATH: Path = (PROHECT_ROOT / "data" / "output" / "standardized_products.xlsx")
VALIDATION_REPORT_PATH: Path = (PROHECT_ROOT / "data" / "output" / "validation_report.xlsx")
UPC_REQUIRED_COLUMNS: list[str] = ["sku", "upc"]
PRODUCTS_REQUIRED_COLUMNS: list[str] = ["sku"]
