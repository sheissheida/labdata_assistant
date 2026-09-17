import pandas as pd
from dataclasses import dataclass


@dataclass
class CleaningResult:
    """
    A capsule to store the results of a cleaning operation.
    """
    df: pd.DataFrame
    report: dict


def remove_duplicates(df: pd.DataFrame) -> CleaningResult:
    """
    Removes duplicate rows from the dataset and returns a clean copy along with the report.
    """
    rows_before = len(df)

    cleaned_df = df.copy()   # Creating a copy to preserve the original data (obeying the Immutability rule)
    cleaned_df = cleaned_df.drop_duplicates()   # Removing duplicate rows with the standard PANDAS command

    rows_after = len(cleaned_df)
    rows_removed = rows_before - rows_after

    report = {
        "operation": "remove_duplicates",
        "rows_before": rows_before,
        "rows_after": rows_after,
        "rows_removed": rows_removed
    }

    return CleaningResult(df=cleaned_df, report=report)


def handle_missing_values(df: pd.DataFrame, strategy: str = "drop") -> CleaningResult:
    """
    Handles missing values ​​and returns a clean copy along with the report.
    Strategies:
    'drop': Deletes rows with empty data
    'mean': Fills in the blank with the average of the numbers in the same column
    'median': Fills in the blank with median (noise-resistant - numeric only)
    'mode': Fills in the blank with the most frequent value (suitable for text and categorical data)
    """
    missing_before = int(df.isna().sum().sum())   # Counts the total number of empty cells in the entire table before starting the operation.
    
    cleaned_df = df.copy()

    if strategy == "drop":
        cleaned_df = cleaned_df.dropna()   # Removes the rows that contains NULL values

    elif strategy == "mean":
        numeric_cols = cleaned_df.select_dtypes(include='number').columns   
        # Separating numeric columns from non-numeric ones
        # numeric_only=True is important because averaging is only performed on numeric columns.
        if len(numeric_cols) > 0:   # Fills in missing values ​​only in numeric columns
            cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(cleaned_df[numeric_cols].mean())
            # If a text column has a missing value, it is left untouched in this strategy.

    elif strategy == "median":
        numeric_cols = cleaned_df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(cleaned_df[numeric_cols].median())

    elif strategy == "mode":   # Selects the first row [0] of the mode output to avoid errors in multiple modes.
        mode_df = cleaned_df.mode()
        if not mode_df.empty:
            modes = mode_df.iloc[0]
            cleaned_df = cleaned_df.fillna(modes)

    else:   # Avoids implementing invalid strategies
        raise ValueError(
            f"Strategy '{strategy}' is invalid. "
            "Allowed strategies: 'drop', 'mean', 'median', 'mode'"
        )

    missing_after = int(cleaned_df.isna().sum().sum())

    report = {
        "operation": "handle_missing_values",
        "strategy": strategy,
        "missing_before": missing_before,
        "missing_after": missing_after,
        "cells_fixed": missing_before - missing_after
    }

    return CleaningResult(df=cleaned_df, report=report)


_CLEANING_REGISTRY = {
    "remove_duplicates": remove_duplicates,
    "handle_missing_values": handle_missing_values
}


def run_pipeline(df: pd.DataFrame, operations: list[dict]) -> tuple[pd.DataFrame, list[dict]]:
    """
    Gets a list of operation settings, execute them sequentially on the dataframe, and return the final dataframe along with a list of logs.
    """
    working_df = df.copy()
    reports = []

    for op in operations:   # Copying the dictionary to prevent changing the original version
        op_kwargs = op.copy()
        op_name = op_kwargs.pop("name")

        if op_name not in _CLEANING_REGISTRY:
            raise ValueError(f"Unknown operation in pipeline: '{op_name}'")

        func = _CLEANING_REGISTRY[op_name]   # Dynamic function calling using a mapping dictionary

        result = func(working_df, **op_kwargs)   # op_kwargs now only includes parameters like strategy

        working_df = result.df
        reports.append(result.report)

    return working_df, reports


