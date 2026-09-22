import reflex as rx
from labdata_assistant.state import AppState


def render_heatmap_cell(cell) -> rx.Component:
    return rx.table.cell(
        cell.value,
        bg=cell.bg_color,
        color="black",
        font_weight=rx.cond(cell.is_header, "bold", "normal"),
        border="1px solid #e5e7eb",
        text_align="center"
    )

def render_corr_row(row_data) -> rx.Component:
    return rx.table.row(
        rx.foreach(
            row_data,
            render_heatmap_cell
        )
    )

def correlation_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Analysis v2: Correlation Matrix", size="4"),
        rx.text("Discover relationships between numeric variables (Pearson correlation).", color="gray"),
        
        rx.button(
            "Run Correlation Analysis",
            on_click=AppState.generate_correlation_report,
            color_scheme="indigo",
            size="3",
            margin_y="1em",
        ),
        
        rx.cond(
            AppState.correlation_table_headers.length() > 0,
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.foreach(
                                AppState.correlation_table_headers,
                                lambda header: rx.table.column_header_cell(
                                    header, color="black", bg="#f3f4f6", border="1px solid #e5e7eb", text_align="center"
                                )
                            )
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            AppState.correlation_heatmap_rows,  # متغیر جدید اینجاست
                            render_corr_row
                        )
                    ),
                    variant="surface",
                    size="2",
                    width="100%",
                ),
                overflow_x="auto",
                width="100%"
            ),
            rx.text("No correlation data yet. Click the button to generate the matrix.", color="gray", size="2")
        ),
        
        padding="1.5em",
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_top="1em",
        width="100%"
    )