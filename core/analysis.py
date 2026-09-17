import pandas as pd
import numpy as np

def analyze_numeric_columns(df: pd.DataFrame) -> dict:
    numeric_df = df.select_dtypes(include=[np.number])
    analysis_report = {}

    for col in numeric_df.columns:
        col_data = numeric_df[col].dropna()
        
        if col_data.empty:
            continue

        std_val = col_data.std()
        std_val = 0.0 if pd.isna(std_val) else float(std_val)

        analysis_report[str(col)] = {
            "count": str(int(col_data.count())),
            "mean": str(round(float(col_data.mean()), 2)),
            "median": str(round(float(col_data.median()), 2)),
            "std": str(round(std_val, 2)),
            "min": str(round(float(col_data.min()), 2)),
            "25%": str(round(float(col_data.quantile(0.25)), 2)),
            "50%": str(round(float(col_data.quantile(0.50)), 2)),
            "75%": str(round(float(col_data.quantile(0.75)), 2)),
            "max": str(round(float(col_data.max()), 2)),
        }

    return analysis_report