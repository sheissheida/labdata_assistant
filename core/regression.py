import pandas as pd
import numpy as np


def calculate_linear_regression(df: pd.DataFrame, x_col: str, y_col: str) -> dict | None:
    clean_df = df[[x_col, y_col]].dropna()

    if len(clean_df) < 2:
        return None

    x = clean_df[x_col].values
    y = clean_df[y_col].values

    slope, intercept = np.polyfit(x, y, 1)

    y_pred = slope * x + intercept

    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

    rmse = np.sqrt(np.mean((y - y_pred) ** 2))
    mae = np.mean(np.abs(y - y_pred))

    return {
        "x_col": x_col,
        "y_col": y_col,
        "slope": float(slope),
        "intercept": float(intercept),
        "r2": float(r2),
        "rmse": float(rmse),
        "mae": float(mae),
    }