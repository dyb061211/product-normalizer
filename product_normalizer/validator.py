import pandas as pd
from product_normalizer.exceptions import MissingRequiredColumnError


def validate_required_columns(df: pd.DataFrame, required_columns: list[str], source: str) -> None:
    missing_columns = []
    for col in required_columns:
        if col not in df.columns:
            missing_columns.append(col)
    if missing_columns:
        raise MissingRequiredColumnError(f"{source}文件缺少{",".join(missing_columns)}")


def collect_empty_field_issues(df: pd.DataFrame, field: str, source: str) -> pd.DataFrame:
    issues = []
    for x in range(len(df)):
        if df.loc[df.index[x], field] == "":
            issues.append({
                "source": source,
                "row_number": x + 2,
                "field": field,
                "value": "",
                "error_type": "EMPTY_VALUE",
                "message": f"{field}不能为空"
            })
    issues = pd.DataFrame(issues)
    return issues


def collect_duplicate_field_issues(df: pd.DataFrame, field: str, source: str) -> pd.DataFrame:
    issues = []
    duplicate_mask = ((df[field] != "") & (df[field].duplicated(keep=False)))
    for x in range(len(df)):
        if duplicate_mask.iloc[x]:
            issues.append(
                {
                    "source": source,
                    "row_number": x + 2,
                    "field": field,
                    "value": df.loc[df.index[x], field],
                    "error_type": "DUPLICATE",
                    "message": f"{field}重复"
                }
            )
    issues = pd.DataFrame(issues)
    return issues
