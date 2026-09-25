import pandas as pd


def export_to_excel(
        raw_df: pd.DataFrame,
        cleaning_history: list[dict],
        statistics: list[dict],
        model_comparison: list[dict],
        output_path: str
):
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

        if not raw_df.empty:
            raw_df.to_excel(writer, sheet_name="Raw Data", index=False)
        else:
            pd.DataFrame({"Message": ["No data available."]}).to_excel(writer, sheet_name="Raw Data", index=False)

        if cleaning_history:
            pd.DataFrame(cleaning_history).to_excel(writer, sheet_name="Cleaning History", index=False)
        else:
            pd.DataFrame({"Message": ["No cleaning operations performed."]}).to_excel(writer, sheet_name="Cleaning History", index=False)

        if statistics:
            pd.DataFrame(statistics).to_excel(writer, sheet_name="Statistics", index=False)
        else:
            pd.DataFrame({"Message": ["No statistics available."]}).to_excel(writer, sheet_name="Statistics", index=False)

        if model_comparison:
            pd.DataFrame(model_comparison).to_excel(writer,sheet_name="Model Comparison", index=False)
        else:
            pd.DataFrame({"Message": ["No models compared."]}).to_excel(writer, sheet_name="Model Comparison", index=False)