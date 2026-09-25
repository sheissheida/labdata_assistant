import pandas as pd
from core.exporter import export_to_excel

mock_raw_df = pd.DataFrame({
    "Temperature_C": [100, 110, 120, 130, 200],
    "Pressure_atm": [1.1, 1.2, 1.3, 1.4, 2.5]
})

mock_cleaning = [
    {"Operation": "Missing Values", "Details": "Mean imputation", "Rows Before": 5, "Rows After": 5},
    {"Operation": "Outlier Treatment", "Details": "Capped Temperature_C", "Rows Before": 5, "Rows After": 5}
]

mock_stats = [
    {"Column": "Temperature_C", "Mean": 132.0, "Median": 120.0, "Std": 39.6, "Min": 100, "Max": 200},
    {"Column": "Pressure_atm", "Mean": 1.5, "Median": 1.3, "Std": 0.57, "Min": 1.1, "Max": 2.5}
]

mock_comparison = [
    {"Model": "Polynomial (Degree 2)", "R2 Score": 0.99, "RMSE": 0.01, "MAE": 0.005},
    {"Model": "Linear", "R2 Score": 0.85, "RMSE": 0.15, "MAE": 0.10}
]

output_file = "test_report.xlsx"

print("Generating Excel Report...")
export_to_excel(
    raw_df=mock_raw_df,
    cleaning_history=mock_cleaning,
    statistics=mock_stats,
    model_comparison=mock_comparison,
    output_path=output_file
)
print(f"✅ Report generated successfully at: {output_file}")