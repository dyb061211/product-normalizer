import pandas as pd
import logging

logger = logging.getLogger(__name__)


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    else:
        temp = str(value).strip()
        return temp


def normalize_upc(value: object) -> str:
    text = normalize_text(value)
    if text:
        text = text.replace(" ", "")
        if "." in text:
            x1, x2 = text.rsplit(".", 1)
            if x2 and all(x == "0" for x in x2):
                text = x1
    return text


def normalize_sku(value: object) -> str:
    return normalize_text(value)


def normalize_upc_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"开始标准化 UPC 数据，共{len(df)}行")
    new_df = df.copy()
    new_df["sku"] = new_df["sku"].map(normalize_sku)
    new_df["upc"] = new_df["upc"].map(normalize_upc)
    return new_df


def normalize_product_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"开始标准化 Products 数据，共{len(df)}行")
    new_df = df.copy()
    new_df["sku"] = new_df["sku"].map(normalize_sku)
    text_columns = [
        "product_name",
        "brand",
        "material",
        "color",
        "size",
        "source_url",
    ]
    for col in text_columns:
        if col not in new_df.columns: continue
        new_df[col] = new_df[col].map(normalize_text)
    return new_df


def clean_upc_data(new_df: pd.DataFrame) -> pd.DataFrame:
    if (new_df["sku"] == "").sum() != 0:
        logger.warning(f"检测到{(new_df["sku"] == "").sum()}条空SKU")
    if new_df[new_df["sku"] != ""].duplicated(subset=["sku"], keep="first").sum() != 0:
        logger.warning(f"检测到{new_df[new_df["sku"] != ""].duplicated(subset=["sku"], keep="first").sum()}条重复SKU")
    if new_df[new_df["upc"] != ""].duplicated(subset=["upc"], keep="first").sum():
        logger.warning(f"检测到{new_df[new_df["upc"] != ""].duplicated(subset=["upc"], keep="first").sum()}条重复UPC")
    new_df = new_df[new_df["sku"] != ""]
    new_df.drop_duplicates(subset=["sku"], inplace=True)
    new_df.reset_index(drop=True, inplace=True)
    logger.info(f"数据清洗完毕，剩余{len(new_df)}行")
    return new_df


def clean_product_data(new_df: pd.DataFrame) -> pd.DataFrame:
    if (new_df["sku"] == "").sum() != 0:
        logger.warning(f"检测到{(new_df["sku"] == "").sum()}条空SKU")
    if new_df[new_df["sku"] != ""].duplicated(subset=["sku"], keep="first").sum() != 0:
        logger.warning(f"检测到{new_df[new_df["sku"] != ""].duplicated(subset=["sku"], keep="first").sum()}条重复SKU")
    new_df = new_df[new_df["sku"] != ""]
    new_df = new_df.drop_duplicates(subset=["sku"], keep="first")
    new_df.reset_index(drop=True, inplace=True)
    logger.info(f"数据清洗完毕，剩余{len(new_df)}行")
    return new_df
