import reflex as rx
import os
from pydantic import BaseModel
from core.data_loader import load_dataset
from core.inspector import inspect_dataset
from core.cleaning import remove_duplicates
from core.cleaning import handle_missing_values
from core.outliers import detect_outliers_iqr


class FreqItem(BaseModel):
    category: str
    count: str
    percentage: str


class CategoricalColumn(BaseModel):
    name: str
    total_rows: str
    non_null_count: str
    missing_count: str
    unique_count: str
    most_frequent: str
    most_frequent_percentage: str
    frequencies: list[FreqItem]


class AppState(rx.State):
    dataset_name: str = ""
    inspection_report: dict = {}
    is_loaded: bool = False
    raw_file_path: str = ""
    working_file_path: str = ""
    cleaning_report: dict = {}
    is_cleaned: bool = False
    missing_strategy: str = "drop"
    cleaning_history: list[dict] = []
    outlier_report: dict = {}
    selected_outlier_columns: list[str] = []
    selected_outlier_method: str = "iqr"
    outlier_multiplier: float = 1.5
    data_version: int = 0
    outlier_report_version: int = -1
    outlier_treatment_strategy: str = "nullify"
    numeric_analysis_report: dict[str, dict[str, str]] = {}
    categorical_analysis_report: dict = {}


    @rx.var
    def row_count(self) -> int:
        return int(self.inspection_report.get("rows", 0))

    @rx.var
    def column_count(self) -> int:
        return int(self.inspection_report.get("cols", 0))

    @rx.var
    def numeric_columns(self) -> list[str]:
        dtypes = self.inspection_report.get("dtypes", {})
        return [
            str(col) for col, dtype in dtypes.items()
            if "int" in str(dtype).lower() or "float" in str(dtype).lower()
        ]

    @rx.var
    def total_missing(self) -> int:
        return int(self.inspection_report.get("total_missing", 0))

    @rx.var
    def duplicate_rows(self) -> int:
        return int(self.inspection_report.get("duplicate_rows", 0))

    @rx.var
    def column_information(self) -> list[dict]:
        columns = self.inspection_report.get("columns", [])
        dtypes = self.inspection_report.get("dtypes", {})
        missing_values = self.inspection_report.get("missing_values", {})

        return [
            {
                "name": str(column),
                "dtypes": str(dtypes.get(column, "unknown")),
                "missing": int(missing_values.get(column, 0)),
            }
            for column in columns
        ]

    @rx.var
    def rows_before(self) -> int:
        return int(self.cleaning_report.get("rows_before", 0))

    @rx.var
    def rows_after(self) -> int:
        return int(self.cleaning_report.get("rows_after", 0))

    @rx.var
    def rows_removed(self) -> int:
        return int(self.cleaning_report.get("rows_removed", 0))

    @rx.var
    def cleaning_operation(self) -> str:
        return str(self.cleaning_report.get("operation", ""))

    @rx.var
    def has_valid_outlier_report(self) -> bool:
        if (self.outlier_report_version == self.data_version) and (len(self.outlier_report) > 0):
            return True
        return False
    
    @rx.var
    def outlier_total_found(self) -> int:
        return int(self.outlier_report.get("outlier_count", 0))

    @rx.var
    def outlier_table_data(self) -> list[list[str]]:
        cells = self.outlier_report.get("outlier_cells", [])

        return [
            [str(cell.get("row_index", "")), str(cell.get("column", "")), str(cell.get("value", ""))]
            for cell in cells
        ]
    
    async def handle_upload(self, files: list[rx.UploadFile]):
        if not files:
            return
        file = files[0]
        upload_data = await file.read()

        os.makedirs(".uploads", exist_ok=True)
        save_path = f".uploads/{file.filename}"
        with open(save_path, "wb") as f:
            f.write(upload_data)

        df = load_dataset(save_path)
        self.inspection_report = inspect_dataset(df)

        self.raw_file_path = save_path
        self.working_file_path = save_path

        self.dataset_name = str(file.filename)
        self.is_loaded = True
        self.is_cleaned = False
        self.cleaning_report = {}
        self.cleaning_history = []

        self.data_version = 0
        self.outlier_report = {}
        self.outlier_report_version = -1


    def remove_duplicate_rows(self):
        if not self.working_file_path:
            return

        df = load_dataset(self.working_file_path)
        result = remove_duplicates(df)

        cleaned_path = ".uploads/cleaned_dataset.csv"
        result.df.to_csv(cleaned_path, index=False)

        safe_report = {
            "operation": str(result.report.get("operation", "remove_duplicates")),
            "rows_before": int(result.report.get("rows_before", 0)),
            "rows_after": int(result.report.get("rows_after", 0)),
            "rows_removed": int(result.report.get("rows_removed", 0)),
        }
        self.add_history_entry(safe_report)

        self.working_file_path = cleaned_path
        self.cleaning_report = safe_report
        self.is_cleaned = True
        self.data_version += 1
        self.inspection_report = inspect_dataset(result.df)

    def set_missing_strategy(self, value: str):
        self.missing_strategy = value

    def apply_selected_missing_strategy(self):
        if not self.working_file_path:
            return

        df = load_dataset(self.working_file_path)

        result = handle_missing_values(df, strategy=self.missing_strategy)

        cleaned_path = ".uploads/cleaned_dataset.csv"
        result.df.to_csv(cleaned_path, index=False)

        safe_report = {
            "operation": str(result.report.get("operation", f"missing_values ({self.missing_strategy})")),
            "rows_before": int(result.report.get("rows_before", 0)),
            "rows_after": int(result.report.get("rows_after", 0)),
            "rows_removed": int(result.report.get("rows_removed", 0)),
        }
        self.add_history_entry(safe_report)


        self.working_file_path = cleaned_path
        self.cleaning_report = safe_report
        self.is_cleaned = True
        self.data_version += 1
        self.inspection_report = inspect_dataset(result.df)

    def download_cleaned_file(self):
        if not self.working_file_path:
            return

        with open(self.working_file_path, "r", encoding="utf-8") as file:
            file_data = file.read()

        return rx.download(
            data=file_data,
            filename="cleaned_dataset.csv"
        )

    def add_history_entry(self, report: dict):
        step_number = len(self.cleaning_history) + 1
        entry = {
            "step": step_number,
            "operation": str(report.get("operation", "Unknown operation")),
            "rows_before": int(report.get("rows_before", 0)),
            "rows_after": int(report.get("rows_after", 0)),
            "rows_removed": int(report.get("rows_removed", 0)),
        }
        self.cleaning_history.append(entry)

    def reset_to_raw(self):
        if not self.raw_file_path:
            return

        self.working_file_path = self.raw_file_path
        self.is_cleaned = False
        self.cleaning_report = {}

        df = load_dataset(self.raw_file_path)
        self.inspection_report = inspect_dataset(df)
        self.cleaning_history = []

        self.data_version = 0
        self.outlier_report = {}
        self.outlier_report_version = -1

    def set_outlier_columns(self, columns: list[str]):
        self.selected_outlier_columns = columns

    def toggle_outlier_column(self, col: str, checked: bool):
        if checked and col not in self.selected_outlier_columns:
            self.selected_outlier_columns.append(col)
        elif not checked and col in self.selected_outlier_columns:
            self.selected_outlier_columns.remove(col)

    def set_outlier_multiplier(self, value: str):
        try:
            self.outlier_multiplier = float(value)
        except ValueError:
            self.outlier_multiplier = 1.5

    def detect_outliers(self):
        if not self.working_file_path:
            return

        df = load_dataset(self.working_file_path)

        report = detect_outliers_iqr(
            df,
            columns=self.selected_outlier_columns if self.selected_outlier_columns else None,
            multiplier=self.outlier_multiplier
        )

        self.outlier_report = report
        self.outlier_report_version = self.data_version

    def set_outlier_treatment_strategy(self, value: str):
        self.outlier_treatment_strategy = value

    def apply_outlier_treatment(self):
        if not self.working_file_path or not self.has_valid_outlier_report:
            return

        from core.outliers import nullify_outliers, cap_outliers, drop_outliers

        df = load_dataset(self.working_file_path)

        if self.outlier_treatment_strategy == "nullify":
            result = nullify_outliers(df, self.outlier_report)
        elif self.outlier_treatment_strategy == "cap":
            result = cap_outliers(df, self.outlier_report)
        elif self.outlier_treatment_strategy == "drop":
            result = drop_outliers(df, self.outlier_report)
        else:
            return

        cleaned_path = ".uploads/cleaned_dataset.csv"
        result.df.to_csv(cleaned_path, index=False)

        self.working_file_path = cleaned_path
        self.cleaning_report = result.report
        self.is_cleaned = True
        self.data_version += 1
        self.inspection_report = inspect_dataset(result.df)
        self.add_history_entry(result.report)

        self.outlier_report = {}
        self.outlier_report_version = -1

    def generate_analysis_report(self):
        if not self.working_file_path:
            return

        from core.analysis import analyze_numeric_columns

        df = load_dataset(self.working_file_path)

        self.numeric_analysis_report = analyze_numeric_columns(df)

    @rx.var
    def analysis_table_data(self) -> list[list[str]]:
        if not self.numeric_analysis_report:
            return []

        data = []
        for col, stats in self.numeric_analysis_report.items():
            data.append([
                str(col),
                str(stats.get("count", "")),
                str(stats.get("mean", "")),
                str(stats.get("std", "")),
                str(stats.get("min", "")),
                str(stats.get("50%", "")),
                str(stats.get("max", ""))
            ])
        return data

    def generate_categorical_report(self):
        if not self.working_file_path:
            return

        import pandas as pd
        from core.analysis import analyze_categorical_columns

        df = pd.read_csv(self.working_file_path)

        self.categorical_analysis_report = analyze_categorical_columns(df)


    @rx.var
    def categorical_ui_data(self) -> list[CategoricalColumn]:
        if not self.categorical_analysis_report:
            return []

        ui_data = []
        for col, stats in self.categorical_analysis_report.items():
            freq_list = []
            for f in stats.get("frequencies", []):
                freq_list.append(
                    FreqItem(
                        category=f.get("category", ""),
                        count=f.get("count", ""),
                        percentage=f.get("percentage", "")
                    )
                )

            ui_data.append(
                CategoricalColumn(
                    name=str(col),
                    total_rows=str(stats.get("total_rows", "")),
                    non_null_count=str(stats.get("non_null_count", "")),
                    missing_count=str(stats.get("missing_count", "")),
                    unique_count=str(stats.get("unique_count", "")),
                    most_frequent=str(stats.get("most_frequent", "")),
                    most_frequent_percentage=str(stats.get("most_frequent_percentage", "")),
                    frequencies=freq_list
                )
            )
        return ui_data