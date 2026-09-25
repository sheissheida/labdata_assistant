import reflex as rx
from labdata_assistant.state import AppState

def export_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Analysis v7: Report Generation", size="4"),
        rx.text("Export your complete data pipeline to an Excel workbook or a Presentation-Ready PDF.", color="gray"),
        
        rx.hstack(
            rx.button(
                rx.icon("file-spreadsheet", size=20),
                " Download Excel Report",
                on_click=AppState.download_excel_report,
                color_scheme="green",
                size="3",
                disabled=AppState.working_file_path == "",
            ),
            rx.button(
                rx.icon("file-text", size=20),
                " Download PDF Report",
                on_click=AppState.download_pdf_report,
                color_scheme="ruby",
                size="3",
                disabled=AppState.working_file_path == "",
            ),
            spacing="4",
            margin_top="1em"
        ),
        
        padding="1.5em",
        border="1px solid #e2e8f0",
        bg="#f8fafc", 
        border_radius="8px",
        margin_top="1em",
        width="100%",
        align_items="center"
    )