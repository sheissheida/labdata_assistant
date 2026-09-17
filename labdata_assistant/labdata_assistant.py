import reflex as rx
from .state import AppState
from components.outlier_panel import outlier_panel
from components.analysis_panel import analysis_panel


def header() -> rx.Component:
    return rx.vstack(
        rx.heading("LabData Assistant", size="8"),
        rx.text("Turn raw laboratory data into clear, useful insights.", color="gray"),
        align_items="start"
    )

def upload_section() -> rx.Component:
    return rx.vstack(
        rx.upload(
            rx.text("Drop or click your CSV file here"),
            id="dataset_upload",
            border="1px dashed #ccc",
            padding="2em",
            width="100%",
            accept={"text/csv": [".csv"]},
        ),
        rx.button(
            "Analyze Dataset",
            on_click=AppState.handle_upload(rx.upload_files(upload_id="dataset_upload"))
        ),
        spacing="4",
        margin_top="2em"
    )

def column_informations_table() -> rx.Component:
    return rx.vstack(
        rx.heading("Column information", size="5"),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Column"),
                    rx.table.column_header_cell("Data type"),
                    rx.table.column_header_cell("Missing values"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    AppState.column_information,
                    lambda column: rx.table.row(
                        rx.table.cell(column["name"]),
                        rx.table.cell(column["dtypes"]),
                        rx.table.cell(column["missing"]),
                    ),
                ),
            ),
            width="100%",
            variant="surface",
        ),
        margin_top="2em",
        width="100%",
    )

def dataset_summary() -> rx.Component:
    return rx.cond(
        AppState.is_loaded,
        rx.vstack(
            rx.heading("Dataset Summary", size="5"),
            rx.grid(
                summary_card("Rows", AppState.row_count),
                summary_card("Columns", AppState.column_count),
                summary_card("Missing cells", AppState.total_missing),
                summary_card("Duplicate rows", AppState.duplicate_rows),
                columns="repeat(auto-fit, minmax(160px, 1fr))",
                spacing="4",
                width="100%",
            ),

            column_informations_table(),

            margin_top="2em",
            width="100%",
        )
    )

def duplicate_cleaning_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Duplicate rows", size="4"),
            rx.text("Remove duplicated rows from the working dataset.", color="gray"),
            rx.button(
                "Remove duplicate rows",
                on_click=AppState.remove_duplicate_rows,
                disabled=AppState.is_loaded == False,
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        width="100%",
    )

def cleaning_result_card() -> rx.Component:
    return rx.cond(
        AppState.is_cleaned,
        rx.card(
            rx.vstack(
                rx.heading("Cleaning result", size="4"),
                rx.text(AppState.cleaning_operation, font_weight="bold"),
                rx.text("Rows before: ", AppState.rows_before),
                rx.text("Rows after: ", AppState.rows_after),
                rx.text("Rows removed: ", AppState.rows_removed),
                spacing="2",
                align="start",
            ),
            width="100%",
            background_color="#f0fdf4",
            border="1px solid #bbf7d0"
        ),
    )

def missing_cleaning_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Missing values", size="4"),
            rx.text("Choose how missing values should be handled.", color="gray"),
            rx.select(
                ["drop", "mean", "median", "mode"],
                value=AppState.missing_strategy,
                on_change=AppState.set_missing_strategy,
            ),
            rx.button(
                "Apply strategy",
                on_click=AppState.apply_selected_missing_strategy,
                disabled=AppState.is_loaded == False,
            ),

            spacing="3",
            align="start",
            width="100%",
        ),
        width="100%",
    )

def cleaning_section() -> rx.Component:
    return rx.vstack(
        rx.heading("Cleaning Operations", size="5"),
        rx.grid(
            duplicate_cleaning_card(),
            missing_cleaning_card(),
            columns="repeat(auto-fit, minmax(280px, 1fr))",
            spacing="4",
            width="100%",
        ),
        cleaning_result_card(),
        margin_top="2em",
        spacing="4",
        width="100%",
    )

def export_section() -> rx.Component:
    return rx.cond(
        AppState.is_cleaned,
        rx.vstack(
            rx.heading("Export & Reset", size="5"),
            rx.text("Your data is processed. You can download it or revert to the original datadet.", color="gray"),

            rx.hstack(
                rx.button(
                    "Download Cleaned Data",
                    on_click=AppState.download_cleaned_file,
                    size="3",
                    color_scheme="green",
                ),
                rx.button(
                    "Reset to Raw Data",
                    on_click=AppState.reset_to_raw,
                    size="3",
                    color_scheme="gray",
                    variant="outline",
                ),
                spacing="4",
            ),

            padding="1em",
            border="1px dashed #22c55e",
            border_radius="md",
            width="100%",
            align_items="start",
            margin_top="1em"
        )
    )

def history_item(item) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(f"Step {item['step']} — {item['operation']}", font_weight="bold", color="#2563eb"),
            rx.text(f"Rows before: {item['rows_before']}", size="2"),
            rx.text(f"Rows after: {item['rows_after']}", size="2"),
            rx.text(f"Rows removed: {item['rows_removed']}", size="2"),
            spacing="1",
            align="start",
        ),
        width="100%",
        border_left="4px solid #3b82f6",
        margin_bottom="1em"
    )

def history_section() -> rx.Component:
    return rx.cond(
        AppState.is_loaded,
        rx.vstack(
            rx.heading("Cleaning History", size="5"),
            rx.cond(
                AppState.cleaning_history.length() > 0,
                rx.vstack(
                    rx.foreach(
                        AppState.cleaning_history,
                        history_item
                    ),
                    width="100%",
                ),
                rx.text("No cleaning operations performed yet.", color="gray"),
            ),
            width="100%",
            margin_top="2em",
            spacing="4",
        )
    )

def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            header(),
            upload_section(),
            rx.cond(
                AppState.is_loaded,
                rx.vstack(
                    dataset_summary(),
                    cleaning_section(),
                    outlier_panel(),
                    analysis_panel(),
                    export_section(),
                    history_section(),
                    spacing="6",
                    width="100%",
                ),
            ),
            padding="50px",
            max_width="800px",
            margin="0 auto"
        )
    )

def summary_card(label: str, value):
    return rx.card(
        rx.vstack(
            rx.text(label, size="2", color="gray"),
            rx.heading(value, size="7"),
            spacing="2",
            align="start",
        ),
        width="100%",
    )

app = rx.App()
app.add_page(index)