from pathlib import Path
import pandas as pd
import json
from product_normalizer.exceptions import FileReadError, InvalidDataError
import logging

logger = logging.getLogger(__name__)


def load_column_aliases(path: Path) -> dict[str, list[str]]:
    try:
        logger.info(f"开始加载列名配置:{path}")
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        logger.info(f"列明加载成功，共{len(data)}行数")
    except FileNotFoundError as e:
        raise FileReadError(f"配置文件{path}不存在，原因是：{e}")
    except PermissionError as e:
        raise FileReadError(f"配置文件{path}无法读取，原因是：{e}")
    except json.decoder.JSONDecodeError as e:
        raise InvalidDataError(f"配置文件{path}的JSON格式无效，原因是：{e}")
    return data


def standardize_column_names(alises: dict[str, list[str]], df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"开始列名标准化，共{len(df.columns)}行数")
    rename = {}
    for x in df.columns:
        x_rename = x.strip().lower()
        for standard_name, alis_list in alises.items():
            normalized_alises = [alise.strip().lower() for alise in alis_list]
            if x_rename in normalized_alises:
                rename[x] = standard_name
                break
    new_df = df.rename(columns=rename)
    logger.info(f"列名标准化完成，成功映射{len(rename)}列")
    return new_df
