import reflex as rx
from labdata_assistant.state import AppState


def outlier_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Outlier Detection", size="4"),
        rx.text(
            "Configure the columns and sensitivity used to detect potential outliers.",
            color="gray",
        ),
        
        rx.vstack(
            rx.text("Select columns to inspect", font_weight="bold", size="2"),
            rx.hstack(
                rx.foreach(
                    AppState.numeric_columns,
                    lambda col: rx.checkbox(
                        col,
                        on_change=lambda checked: AppState.toggle_outlier_column(col, checked)
                    )
                ),
                wrap="wrap",
                spacing="4",
            ),
            margin_top="1em",
            margin_bottom="1em",
        ),
        rx.divider(),
        
        rx.hstack(
            rx.vstack(
                rx.text("Method", font_weight="bold", size="2"),
                rx.select(
                    ["IQR"], 
                    value="IQR",
                ),
                align_items="start",
            ),
            rx.vstack(
                rx.text("Sensitivity (Multiplier)", font_weight="bold", size="2"),
                rx.input(
                    default_value="1.5",
                    on_change=AppState.set_outlier_multiplier,
                ),
                align_items="start",
            ),
            spacing="4",
            margin_top="1em",
        ),

        rx.button(
            "Detect Outliers",
            on_click=AppState.detect_outliers,
            color_scheme="orange",
            size="3",
            margin_top="1em",
        ),

        rx.cond(
            AppState.has_valid_outlier_report,
            rx.box(
                rx.text("Detection Results", font_weight="bold", margin_bottom="0.5em", color="black"),
                rx.text("Total outlier cells found: ", AppState.outlier_total_found, color="black", margin_bottom="1em"),
                
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Row Index", color="black"),
                            rx.table.column_header_cell("Column", color="black"),
                            rx.table.column_header_cell("Outlier Value", color="black"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            AppState.outlier_table_data,
                            lambda row_data: rx.table.row(
                                rx.table.cell(row_data[0], color="black"),
                                rx.table.cell(row_data[1], color="black"),
                                rx.table.cell(row_data[2], color="black"),
                            )
                        )
                    ),
                    variant="surface",
                    size="2",
                    width="100%",
                ),

                rx.divider(margin_top="1em", margin_bottom="1em", border_color="#fecdd3"),
                rx.heading("Outlier Treatment", size="3", color="black", margin_bottom="0.5em"),
                rx.text("Treatment method:", font_weight="bold", color="black", size="2"),
                rx.select(
                    ["nullify", "cap"],
                    value=AppState.outlier_treatment_strategy,
                    on_change=AppState.set_outlier_treatment_strategy,
                    margin_bottom="1em",
                ),
                rx.button(
                    "Apply Treatment",
                    on_click=AppState.apply_outlier_treatment,
                    color_scheme="red",
                    size="2",
                ),
                
                padding="1em",
                background_color="#fff1f2",
                border="1px solid #fecdd3",
                border_radius="8px",
                margin_top="1em",
                width="100%",
            )
        ),

        spacing="4",
        width="100%",
        padding="1.5em",
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_top="1em"
    )