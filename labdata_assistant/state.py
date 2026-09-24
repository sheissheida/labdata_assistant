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


class CorrelationMatrix(BaseModel):
    variables: list[str]
    matrix: list[list[str]]


class HeatmapCell(BaseModel):
    value: str
    bg_color: str
    is_header: bool


class LinearRegressionReport(BaseModel):
    x_col: str
    y_col: str
    slope: str
    intercept: str
    equation: str
    r2: str
    rmse: str
    mae: str
    interpretation: str


class PolynomialRegressionReport(BaseModel):
    x_col: str
    y_col: str
    degree: int
    equation: str
    r2: str
    rmse: str
    mae: str
    interpretation: str


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
    correlation_report: CorrelationMatrix | None = None
    selected_categorical_column: str = ""
    chart_type: str = "bar"
    reg_x_column: str = ""
    reg_y_column: str = ""
    regression_report: LinearRegressionReport | None = None
    regression_chart_data: list[dict] = []
    poly_degree: str = "2"
    polynomial_report: PolynomialRegressionReport | None = None
    polynomial_chart_data: list[dict] = []


    def set_chart_type(self, value: str):
        self.chart_type = value

    def set_selected_categorical_column(self, value: str):
        self.selected_categorical_column = value

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

    @rx.var
    def categorical_chart_data(self) -> list[dict]:
        if not self.selected_categorical_column or not self.categorical_ui_data:
            return []

        colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#14b8a6", "#f97316", "#ec4899"]

        for col in self.categorical_ui_data:
            if col.name == self.selected_categorical_column:
                chart_data = []
                for i, freq in enumerate(col.frequencies):
                    chart_data.append({
                        "name": freq.category,
                        "count": int(freq.count),
                        "percentage": float(freq.percentage),
                        "fill": colors[i % len(colors)]
                    })
                return chart_data
        return []

    @rx.var
    def categorical_column_names(self) -> list[str]:
        if not self.categorical_ui_data:
            return []
        return [col.name for col in self.categorical_ui_data]

    def generate_correlation_report(self):
        if not self.working_file_path:
            return

        import pandas as pd
        from core.analysis import calculate_correlation_matrix

        df = pd.read_csv(self.working_file_path)
        corr_df = calculate_correlation_matrix(df)

        if corr_df is not None:
            variables = corr_df.columns.tolist()

            matrix_data = []
            for row_var in variables:
                row_values = []
                for col_var in variables:
                    val = corr_df.loc[row_var, col_var]
                    clean_val = "" if pd.isna(val) else str(val)
                    row_values.append(clean_val)
                matrix_data.append(row_values)

            self.correlation_report = CorrelationMatrix(
                variables=variables,
                matrix=matrix_data
            )
        else:
            self.correlation_report = None

    @rx.var
    def correlation_table_headers(self) -> list[str]:
        if self.correlation_report is None or not self.correlation_report.variables:
            return []

        return ["Variable"] + self.correlation_report.variables

    @rx.var
    def correlation_heatmap_rows(self) -> list[list[HeatmapCell]]:
        if self.correlation_report is None or not self.correlation_report.variables:
            return []

        def get_color(val_str: str) -> str:
            try:
                val = float(val_str)

                if val == 1.0: return "#60a5fa"
                elif val >= 0.7: return "#93c5fd"
                elif val >= 0.3: return "#bfdbfe"
                elif val > 0: return "#dbeafe"
                elif val <= -0.7: return "#f87171"
                elif val <= -0.3: return "#fca5a5"
                elif val < 0: return "#fee2e2"
                return "#ffffff"
            except:
                return "#ffffff"

        rows: list[list[HeatmapCell]] = []
        for i, var in enumerate(self.correlation_report.variables):
            current_row = [HeatmapCell(value=str(var), bg_color="f3f4f6", is_header=True)]

            for val in self.correlation_report.matrix[i]:
                current_row.append(
                    HeatmapCell(
                        value=str(val),
                        bg_color=get_color(str(val)),
                        is_header=False
                    )
                )
            rows.append(current_row)

        return rows

    def set_reg_x_column(self, value: str):
        self.reg_x_column = value

    def set_reg_y_column(self, value: str):
        self.reg_y_column = value

    def run_linear_regression(self):
        if not self.working_file_path or not self.reg_y_column:
            return

        import pandas as pd
        from core.regression import calculate_linear_regression

        df = pd.read_csv(self.working_file_path)
        result = calculate_linear_regression(df, self.reg_x_column, self.reg_y_column)

        if result:
            slope = result["slope"]
            intercept = result["intercept"]
            r2 = result["r2"]

            sign = "+" if intercept >= 0 else "-"
            eq = f"Y = {slope:.4f}X {sign} {abs(intercept):.4f}"

            if r2 > 0.8:
                interp = "Strong linear relationship. The model explains most of the variance in the data."
            elif r2 > 0.5:
                interp = "Moderate linear relationship. The model has some predictive power."
            else:
                interp = "Weak or no linear relationship. A linear model may not be suitable for these variables."

            self.regression_report = LinearRegressionReport(
                x_col=result["x_col"],
                y_col=result["y_col"],
                slope=f"{slope:.4f}",
                intercept=f"{intercept:.4f}",
                equation=eq,
                r2=f"{r2:.4f}",
                rmse=f"{result['rmse']:.4f}",
                mae=f"{result['mae']:.4f}",
                interpretation=interp
            )

            clean_df = df[[self.reg_x_column, self.reg_y_column]].dropna()
            chart_points = []
            for _, row in clean_df.iterrows():
                x_val = float(row[self.reg_x_column])
                y_val = float(row[self.reg_y_column])
                fit_val = slope * x_val + intercept

                chart_points.append({
                    "x": x_val,
                    "y": y_val,
                    "fit": fit_val
                })

            chart_points.sort(key=lambda p: p["x"])
            self.regression_chart_data = chart_points

        else:
            self.regression_report = None
            self.regression_chart_data = []

    def set_poly_degree(self, value: str):
        self.poly_degree = value

    def run_polynomial_regression(self):
        if not self.working_file_path or not self.reg_x_column or not self.reg_y_column:
            return

        import pandas as pd
        import numpy as np
        from core.regression import calculate_polynomial_regression

        df = pd.read_csv(self.working_file_path)
        deg = int(self.poly_degree)
        result = calculate_polynomial_regression(df, self.reg_x_column, self.reg_y_column, deg)

        if result:
            coeffs = result["coefficients"]
            r2 = result["r2"]

            eq_parts = []
            current_deg = deg
            for c in coeffs:
                if current_deg > 1:
                    eq_parts.append(f"{c:.4f}X^{current_deg}")
                elif current_deg == 1:
                    eq_parts.append(f"{c:.4f}X")
                else:
                    eq_parts.append(f"{c:.4f}")
                current_deg -= 1

            eq = "Y = " + " + ".join(eq_parts).replace("+ -", "- ")

            if r2 > 0.8:
                interp = f"Strong polynomial relationship (Degree {deg}). The curve fits the data well."
            elif r2 > 0.5:
                interp = f"Moderate polynomial relationship (Degree {deg})."
            else:
                interp = "Weak polynomial relationship. A different model might be needed."

            self.polynomial_report = PolynomialRegressionReport(
                x_col=result["x_col"],
                y_col=result["y_col"],
                degree=deg,
                equation=eq,
                r2=f"{r2:.4f}",
                rmse=f"{result['rmse']:.4f}",
                mae=f"{result['mae']:.4f}",
                interpretation=interp
            )

            clean_df = df[[self.reg_x_column, self.reg_y_column]].dropna()
            chart_points = []

            p=np.poly1d(coeffs)
            for _, row in clean_df.iterrows():
                x_val = float(row[self.reg_x_column])
                y_val = float(row[self.reg_y_column])
                fit_val = p(x_val)

                chart_points.append({
                    "x": x_val,
                    "y": y_val,
                    "poly_fit": fit_val
                })

            chart_points.sort(key=lambda item: item["x"])
            self.polynomial_chart_data = chart_points

        else:
            self.polynomial_report = None
            self.polynomial_chart_data = []



