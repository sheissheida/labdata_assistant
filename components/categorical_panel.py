import reflex as rx
from labdata_assistant.state import AppState


def render_categorical_column(col_data) -> rx.Component:
    return rx.box(
        rx.heading(f"Column: {col_data.name}", size="4", margin_bottom="0.5em"),
        rx.text(f"Total rows: {col_data.total_rows}"),
        rx.text(f"Non-null: {col_data.non_null_count}"),
        rx.text(f"Missing: {col_data.missing_count}"),
        rx.text(f"Unique categories: {col_data.unique_count}"),
        rx.text(f"Most frequent: {col_data.most_frequent} ({col_data.most_frequent_percentage}%)"),

        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Category", color="black"),
                    rx.table.column_header_cell("Count", color="black"),
                    rx.table.column_header_cell("Percentage", color="black"),
                )
            ),
            rx.table.body(
                rx.foreach(
                    col_data.frequencies,
                    lambda freq: rx.table.row(
                        rx.table.cell(freq.category, color="black"),
                        rx.table.cell(freq.count, color="black"),
                        rx.table.cell(freq.percentage + "%", color="black"),
                    )
                )
            ),
            variant="surface",
            size="1",
            width="100%",
            margin_top="1em"
        ),
        padding="1.5em",
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_bottom="1.5em",
        background_color="#f9fafb"
    )

def categorical_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Analysis v1: Categorical Summary", size="4"),
        rx.text("Analyze categorical and text-based columns in your dataset.", color="gray"),

        rx.button(
            "Run Categorical Analysis",
            on_click=AppState.generate_categorical_report,
            color_scheme="green",
            size="3",
            margin_y="1em",
        ),

        rx.cond(
            AppState.categorical_ui_data.length() > 0,
            rx.vstack(
                rx.foreach(
                    AppState.categorical_ui_data,
                    render_categorical_column
                ),
                width="100%"
            ),
            rx.text("No data yet. Load a dataset and run the analysis.", color="gray")
        ),

        padding="1.5em",
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_top="1em",
        width="100%"
    )