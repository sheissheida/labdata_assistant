import reflex as rx
from labdata_assistant.state import AppState


def render_comparison_row(row_data: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(row_data["model"], font_weight="bold", color="#ea580c"),
        rx.table.cell(row_data["r2"]),
        rx.table.cell(row_data["rmse"]),
        rx.table.cell(row_data["mae"]),
    )

def comparison_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Analysis v5: Model Comparison", size="4"),
        rx.text("Evaluate Linear and Polynomial models side-by-side to find the best fit.", color="gray"),

        rx.button(
            "Compare Models",
            on_click=AppState.compare_models,
            color_scheme="orange",
            size="3",
            margin_y="1em",
        ),

        rx.cond(
            AppState.model_comparison.length() > 0,
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Model"),
                            rx.table.column_header_cell("R² Score"),
                            rx.table.column_header_cell("RMSE"),
                            rx.table.column_header_cell("MAE"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            AppState.model_comparison,
                            render_comparison_row
                        )
                    ),
                    variant="surface",
                    size="3",
                    width="100%",
                ),
                rx.text("✨ Models are automatically sorted by best R² score.", color="gray", size="2", margin_top="0.8em"),
                width="100%"
            ),
            rx.text("Run a regression analysis first to select variables, then click Compare Models.", color="gray", size="2")
        ),

        padding="1.5em",
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_top="1em",
        width="100%"
    )