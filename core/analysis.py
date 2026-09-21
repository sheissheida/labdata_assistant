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

def analyze_categorical_columns(df: pd.DataFrame) -> dict:
    categorical_df = df.select_dtypes(include=["object", "category", "bool"])
    analysis_report = {}

    for col in categorical_df.columns:
        series = categorical_df[col]
        total_rows = int(len(series))
        missing_count = int(series.isna().sum())

        non_null = series.dropna()
        non_null_count = int(non_null.count())

        if non_null_count == 0:
            analysis_report[str(col)] = {
                "total_rows": str(total_rows),
                "non_null_count": "0",
                "missing_count": str(missing_count),
                "unique_count": "0",
                "most_frequent": "None",
                "most_frequent_count": "0",
                "most_frequent_percentage": "0.0",
                "frequencies": []
            }
            continue

        unique_count = int(non_null.nunique())
        counts = non_null.value_counts()
        percentages = (counts / non_null_count * 100).round(2)

        most_frequent = str(counts.index[0])
        most_frequent_count = int(counts.iloc[0])
        most_frequent_percentage = float(percentages.iloc[0])

        frequencies = []
        for cat, count in counts.items():
            frequencies.append({
                "category": str(cat),
                "count": str(int(count)),
                "percentage": str(float(percentages[cat]))
            })

        analysis_report[str(col)] = {
            "total_rows": str(total_rows),
            "non_null_count": str(non_null_count),
            "missing_count": str(missing_count),
            "unique_count": str(unique_count),
            "most_frequent": most_frequent,
            "most_frequent_count": str(most_frequent_count),
            "most_frequent_percentage": str(most_frequent_percentage),
            "frequencies": frequencies
        }

    return analysis_report