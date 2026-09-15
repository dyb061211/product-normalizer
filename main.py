import logging
from product_normalizer.service import process_product_files
from product_normalizer.exceptions import ProductNormalizerError
from product_normalizer.logging_config import setup_logging
from product_normalizer.settings import  PRODUCTS_INPUT_PATH, UPC_INPUT_PATH, \
    STANDARDIZED_PRODUCTS_OUTPUT_PATH, VALIDATION_REPORT_PATH

logger = logging.getLogger(__name__)


def main() -> None:
    path_upc = UPC_INPUT_PATH
    path_products = PRODUCTS_INPUT_PATH
    output_path = STANDARDIZED_PRODUCTS_OUTPUT_PATH
    output_path_validation_report = VALIDATION_REPORT_PATH

    setup_logging()

    try:
        process_product_files(
            path_upc,
            path_products,
            output_path,
            output_path_validation_report,
            "cli"
        )
    except ProductNormalizerError as e:
        logger.exception("程序失败")
        print(e)
        return

    logger.info("product-normalizer 处理完成")


if __name__ == "__main__":
    main()
