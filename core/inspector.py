import pandas as pd

def inspect_dataset(df: pd.DataFrame) -> dict:
    """
    Extracts the general information and ID of the DataFrame.
    """
    return{
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "columns": [str(col) for col in df.columns],
        "dtypes": {str(col): str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": {str(col): int(count) for col, count in df.isna().sum().items()},
        "total_missing": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }