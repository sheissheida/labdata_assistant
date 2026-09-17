import reflex as rx
from labdata_assistant.state import AppState


def analysis_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Analysis v1: Descriptive Statistics", size="4"),
        rx.text("Generate statistical summaries for all numeric columns in your cleaned dataset.", color="gray"),

        rx.button(
            "Generate Report",
            on_click=AppState.generate_analysis_report,
            color_scheme="blue",
            size="3",
            margin_bottom="1em",
            margin_top="1em",
        ),

        rx.cond(
            AppState.analysis_table_data.length() > 0,
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Column", color="black"),
                        rx.table.column_header_cell("Count", color="black"),
                        rx.table.column_header_cell("Mean", color="black"),
                        rx.table.column_header_cell("Std Dev", color="black"),
                        rx.table.column_header_cell("Min", color="black"),
                        rx.table.column_header_cell("Median", color="black"),
                        rx.table.column_header_cell("Max", color="black"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        AppState.analysis_table_data,
                        lambda row: rx.table.row(
                            rx.foreach(row, lambda cell: rx.table.cell(cell, color="black"))
                        )
                    )
                ),
                variant="surface",
                size="2",
                width="100%",
            )
        ),

        padding="1.5em",
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_top="1em",
        width="100%"
    )