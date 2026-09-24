import reflex as rx
from labdata_assistant.state import AppState


def residual_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Analysis v6: Residual Diagnostics", size="4"),
        rx.text("Analyze prediction errors to evaluate model validity and detect hidden patterns.", color="gray"),
        
        rx.hstack(
            rx.select(
                ["linear", "polynomial"],
                placeholder="Select Model to Evaluate...",
                value=AppState.res_model_type,
                on_change=AppState.set_res_model_type,
                size="3",
                flex="1"
            ),
            rx.button(
                "Run Residual Analysis",
                on_click=AppState.run_residual_analysis,
                color_scheme="cyan",
                size="3",
            ),
            width="100%",
            spacing="4",
            margin_bottom="1em"
        ),
        
        rx.cond(
            AppState.residual_report,
            rx.box(
                rx.vstack(
                    rx.text(AppState.residual_report.model_name, font_weight="bold", size="5", color="#0891b2"),
                    
                    rx.hstack(
                        rx.badge(f"Mean: {AppState.residual_report.mean_residual}", color_scheme="gray", size="3", radius="full"),
                        rx.badge(f"Std: {AppState.residual_report.std_residual}", color_scheme="gray", size="3", radius="full"),
                        rx.badge(f"Min: {AppState.residual_report.min_residual}", color_scheme="red", size="3", radius="full"),
                        rx.badge(f"Max: {AppState.residual_report.max_residual}", color_scheme="blue", size="3", radius="full"),
                        spacing="4",
                        margin_y="1em"
                    ),
                    
                    rx.heading("Residuals vs Predicted", size="3", margin_top="1em", color="#164e63"),
                    rx.recharts.composed_chart(
                        rx.recharts.x_axis(data_key="predicted", type_="number", name="Predicted Y"),
                        rx.recharts.y_axis(data_key="residual", type_="number", name="Residual"),
                        rx.recharts.graphing_tooltip(),
                        rx.recharts.reference_line(y=0, stroke="red", stroke_dasharray="3 3"), # خط مبدأ صفر
                        rx.recharts.line(
                            data_key="residual",
                            stroke="#0891b2",
                            stroke_width=0,
                            dot=True,
                            name="Residual"
                        ),
                        data=AppState.residual_chart_data,
                        width="100%",
                        height=300,
                    ),
                    
                    rx.heading("Residuals vs Original X", size="3", margin_top="1.5em", color="#164e63"),
                    rx.recharts.composed_chart(
                        rx.recharts.x_axis(data_key="x", type_="number", name="Original X"),
                        rx.recharts.y_axis(data_key="residual", type_="number", name="Residual"),
                        rx.recharts.graphing_tooltip(),
                        rx.recharts.reference_line(y=0, stroke="red", stroke_dasharray="3 3"),
                        rx.recharts.line(
                            data_key="residual",
                            stroke="#8b5cf6",
                            stroke_width=0,
                            dot=True,
                            name="Residual"
                        ),
                        data=AppState.residual_chart_data,
                        width="100%",
                        height=300,
                    ),
                    
                    width="100%",
                    align_items="center"
                ),
                padding="1.5em",
                bg="#ecfeff",
                border="1px solid #cffafe",
                border_radius="8px",
                width="100%",
                text_align="center"
            ),
            rx.text("Select a model type and run the diagnostic check.", color="gray", size="2")
        ),
        
        padding="1.5em",
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_top="1em",
        width="100%"
    )