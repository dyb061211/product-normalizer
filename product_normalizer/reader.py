import pandas as pd
from pathlib import Path
from product_normalizer.exceptions import FileReadError
import logging

logger = logging.getLogger(__name__)


def read_excel_file(path: Path) -> pd.DataFrame:
    try:
        logger.info(f"开始读取:{path}")
        df = pd.read_excel(path, dtype=str)
        logger.info(f"成功读取:{path},共{len(df)}行")
    except FileNotFoundError as e:
        raise FileReadError(f"{path}文件没有找到，原因:{e}")
    except PermissionError as e:
        raise FileReadError(f"没有权限打开这个{path}文件，原因:{e}")
    except ValueError as e:
        raise FileReadError(f"{path}Excel文件无法正常读取，原因:{e}")
    return df
