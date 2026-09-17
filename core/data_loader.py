import pandas as pd
from pathlib import Path

def load_dataset(file_path):
    path = Path(file_path)

    if not path.exists():   # Checks if this file even exists on the hard drive
        raise FileNotFoundError(f"No file found at {path}. Please check the path.")

    if path.suffix.lower() != '.csv':   # Checks file format
        raise ValueError("The file format is invalid. Please upload only the CSV file.")

    try:   # Attempting to read file
        df = pd.read_csv(path)
        return df
    except pd.errors.EmptyDataError:
        raise ValueError("The uploaded file is completely empty and contains no data.")
    
