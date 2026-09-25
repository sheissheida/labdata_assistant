from core.pdf_report import generate_pdf_report

mock_snapshot = {
    "total_rows": 2450,
    "total_columns": 14,
    "cleaning_history": [
        {"Operation": "Drop Missing", "Details": "Removed 12 rows with NaNs"},
        {"Operation": "Remove Duplicates", "Details": "Removed 3 duplicate rows"}
    ],
    "statistics": [
        {"Column": "Temperature", "Mean": 150.4, "Std": 12.3, "Min": 100, "Max": 200},
        {"Column": "Pressure", "Mean": 1.2, "Std": 0.1, "Min": 1.0, "Max": 1.5}
    ],
    "model_comparison": [
        {"Model": "Polynomial (Degree 3)", "R² Score": "0.9850", "RMSE": "0.01", "MAE": "0.005", "raw_r2": 0.9850},
        {"Model": "Linear", "R² Score": "0.8500", "RMSE": "0.15", "MAE": "0.10", "raw_r2": 0.8500}
    ]
}

output_file = "test_report.pdf"

print("Generating Expanded PDF Report...")
generate_pdf_report(report_data=mock_snapshot, output_path_or_stream=output_file)
print(f"✅ Expanded PDF generated successfully at: {output_file}")