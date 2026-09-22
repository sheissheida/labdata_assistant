import reflex as rx
from labdata_assistant.state import AppState


def regression_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Analysis v3: Linear Regression", size="4"),
        rx.text("Model the relationship between two numeric variables.", color="gray"),
        
        rx.hstack(
            rx.select(
                AppState.numeric_columns,
                placeholder="Select X (Independent / Predictor)...",
                value=AppState.reg_x_column,
                on_change=AppState.set_reg_x_column,
                size="3",
                flex="1"
            ),
            rx.select(
                AppState.numeric_columns,
                placeholder="Select Y (Dependent / Response)...",
                value=AppState.reg_y_column,
                on_change=AppState.set_reg_y_column,
                size="3",
                flex="1"
            ),
            width="100%",
            spacing="4",
            margin_bottom="1em"
        ),
        
        rx.button(
            "Run Regression",
            on_click=AppState.run_linear_regression,
            color_scheme="teal",
            size="3",
            margin_bottom="1em",
        ),
        
        rx.cond(
            AppState.regression_report,
            rx.box(
                rx.vstack(
                    rx.text(AppState.regression_report.equation, font_weight="bold", size="5", color="#0f766e"),
                    
                    rx.hstack(
                        rx.badge(f"R²: {AppState.regression_report.r2}", color_scheme="blue", size="3", radius="full"),
                        rx.badge(f"RMSE: {AppState.regression_report.rmse}", color_scheme="red", size="3", radius="full"),
                        rx.badge(f"MAE: {AppState.regression_report.mae}", color_scheme="orange", size="3", radius="full"),
                        spacing="4",
                        margin_y="0.5em"
                    ),
                    
                    rx.text(AppState.regression_report.interpretation, color="gray", font_style="italic", margin_bottom="1.5em"),
                    
                    rx.recharts.composed_chart(
                        rx.recharts.x_axis(data_key="x", type_="number", name=AppState.reg_x_column),
                        rx.recharts.y_axis(type_="number", name=AppState.reg_y_column),
                        rx.recharts.graphing_tooltip(),
                        rx.recharts.line(
                            data_key="y",
                            stroke="#0f766e",
                            stroke_width=0,
                            dot=True,
                            name="Actual Data"
                        ),

                        rx.recharts.line(
                            data_key="fit",
                            stroke="#f97316",
                            dot=False,
                            stroke_width=2,
                            name="Regression Line"
                        ),
                        
                        data=AppState.regression_chart_data,
                        width="100%",
                        height=350,
                    ),
                    
                    spacing="3",
                    align_items="center",
                    width="100%"
                ),
                padding="1.5em",
                bg="#f0fdf4",
                border="1px solid #bbf7d0",
                border_radius="8px",
                width="100%",
                text_align="center"
            ),
            rx.text("Select X and Y columns and run the analysis.", color="gray", size="2")
        ),
        
        padding="1.5em",
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_top="1em",
        width="100%"
    )