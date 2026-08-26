import logging
from pathlib import Path


def setup_logging() -> None:
    Path("logs").mkdir(exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s|%(levelname)s|%(name)s|%(message)s")
    file_handler = logging.FileHandler(
        filename="logs/app.log",
        encoding="utf-8",
        mode="a"
    )
    console_handler = logging.StreamHandler()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info("product-normalizer 启动")
