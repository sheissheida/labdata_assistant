import pandas as pd
import numpy as np
from core.cleaning import run_pipeline
from core.inspector import inspect_dataset
from db.database import SessionLocal, Dataset, CleaningLog
from db.crud import create_dataset, create_cleaning_log

mock_data = {
    "Temperature": [25.0, np.nan, 30.0, 22.0, 25.0], 
    "Time": [2.0, 3.0, np.nan, 5.0, 2.0],            
    "Pressure": [np.nan, 1.2, 1.5, np.nan, np.nan]   
}
original_df = pd.DataFrame(mock_data)

operations_config = [
    {"name": "handle_missing_values", "strategy": "mean"},
    {"name": "remove_duplicates"}
]

print("Running Pipeline...")
final_df, all_reports = run_pipeline(original_df, operations_config)

db = SessionLocal()
try:
    inspection_report = inspect_dataset(original_df)
    saved_dataset = create_dataset(db, "pipeline_test.csv", inspection_report)
    print(f"\nDataset saved with ID: {saved_dataset.id}")

    for i, report in enumerate(all_reports, 1):
        saved_log = create_cleaning_log(db, saved_dataset.id, report)
        print(f"  -> Saved Log ID {saved_log.id} for operation: {saved_log.operation}")

finally:
    db.close()