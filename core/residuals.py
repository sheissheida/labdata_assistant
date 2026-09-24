import pandas as pd
import numpy as np


def calculate_residuals(df: pd.DataFrame, x_col: str, y_col: str, model_type: str = "linear", degree: int = 2) -> dict | None:
    clean_df = df[[x_col, y_col]].dropna()

    if len(clean_df) < 2:
        return None

    x = clean_df[x_col].values
    y = clean_df[y_col].values

    if model_type == "linear":
        coeffs = np.polyfit(x, y, 1)
    elif model_type == "polynomial":
        if len(x) <= degree:
            return None
        coeffs = np.polyfit(x, y, degree)
    else:
        return None

    p = np.poly1d(coeffs)
    y_pred = p(x)

    residuals = y - y_pred
    abs_errors = np.abs(residuals)
    sq_errors = residuals ** 2

    mean_res = np.mean(residuals)
    std_res = np.std(residuals)
    min_res = np.min(residuals)
    max_res = np.max(residuals)
    mae = np.mean(abs_errors)
    rmse = np.sqrt(np.mean(sq_errors))

    return {
        "x_col": x_col,
        "y_col": y_col,
        "model_type": model_type,
        "degree": degree if model_type == "polynomial" else 1,
        "statistics": {
            "mean_residual": float(mean_res),
            "std_residual": float(std_res),
            "min_residual": float(min_res),
            "max_residual": float(max_res),
            "mae": float(mae),
            "rmse": float(rmse),
        },
        "data": {
            "x": x.tolist(),
            "actual": y.tolist(),
            "predicted": y_pred.tolist(),
            "residual": residuals.tolist(),
            "abs_error": abs_errors.tolist(),
            "sq_error": sq_errors.tolist(),
        }
    }