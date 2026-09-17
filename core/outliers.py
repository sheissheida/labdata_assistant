import pandas as pd
import numpy as np
from core.cleaning import CleaningResult

def detect_outliers_iqr(
        df: pd.DataFrame,
        columns: list[str] | None = None,
        multiplier: float = 1.5,
) -> dict:

    if columns is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    else:
        numeric_cols = [col for col in columns if pd.api.types.is_numeric_dtype(df[col])]

    outlier_cells = []
    outlier_rows_set = set()
    affected_columns = {}

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - (multiplier * IQR)
        upper_bound = Q3 + (multiplier * IQR)

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

        if not outliers.empty:
            affected_columns[col] = len(outliers)

            for index, value in outliers[col].items():
                outlier_rows_set.add(int(index))
                outlier_cells.append({
                    "row_index": int(index),
                    "column": col,
                    "value": float(value), 
                    "lower_bound": float(lower_bound),
                    "upper_bound": float(upper_bound)
                })


    return {
        "operation": "detect_outliers",
        "method": "iqr",
        "multiplier": float(multiplier),
        "columns_checked": numeric_cols,
        "rows_checked": len(df),
        "outlier_count": len(outlier_cells),
        "outlier_rows": sorted(list(outlier_rows_set)),
        "outlier_cells": outlier_cells,
        "affected_columns": affected_columns
    }    

def nullify_outliers(df, outlier_report: dict) -> CleaningResult:
    df_cleaned = df.copy()
    cells = outlier_report.get("outlier_cells", [])
    affected_rows = set()

    for cell in cells:
        r_idx = cell["row_index"]
        col = cell["column"]
        df_cleaned.at[r_idx, col] = np.nan
        affected_rows.add(r_idx)

    report = {
        "operation": "outlier_treatment",
        "method": "nullify",
        "columns": outlier_report.get("columns_checked", []),
        "rows_before": len(df),
        "rows_after": len(df_cleaned),
        "rows_affected": len(affected_rows),
        "cells_affected": len(cells),
    }

    return CleaningResult(df=df_cleaned, report=report)

def cap_outliers(df, outlier_report: dict) -> CleaningResult:
    df_cleaned = df.copy()
    cells = outlier_report.get("outier_cells", [])
    affected_rows = set()

    for cell in cells:
        r_idx = cell["row_index"]
        col = cell["column"]
        val = cell["value"]
        lower = cell["lower_bound"]
        upper = cell["upper_bound"]

        if val < lower:
            df_cleaned.at[r_idx, col] = lower
            affected_rows.add(r_idx)
        elif val > upper:
            df_cleaned.at[r_idx, col] = upper
            affected_rows.add(r_idx)

    report = {
        "operation": "outlier_treatment",
        "method": "cap",
        "columns": outlier_report.get("columns_checked", []),
        "rows_before": len(df),
        "rows_after": len(df_cleaned),
        "rows_affected": len(affected_rows),
        "cells_affected": len(cells),
    }

    return CleaningResult(df=df_cleaned, report=report)

def drop_outliers(df, outlier_report: dict) -> CleaningResult:
    df_cleaned = df.copy()
    cells = outlier_report.get("outlier_cells", [])

    rows_to_drop = list(set([cell["row_index"] for cell in cells]))

    df_cleaned = df_cleaned.drop(index=rows_to_drop)

    report = {
        "operation": "outlier_treatment",
        "method": "drop",
        "columns": outlier_report.get("columns_checked", []),
        "rows_before": len(df),
        "rows_after": len(df_cleaned),
        "rows_affected": len(rows_to_drop),
        "cells_affected": len(cells),
    }

    return CleaningResult(df=df_cleaned, report=report)