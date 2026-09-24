import reflex as rx
from labdata_assistant.state import AppState


def polynomial_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Analysis v4: Polynomial Regression", size="4"),
        rx.text("Fit a polynomial curve (Degree 2 to 5) to your data.", color="gray"),

        rx.hstack(
            rx.select(
                AppState.numeric_columns,
                placeholder="Select X (Predictor)...",
                value=AppState.reg_x_column,
                on_change=AppState.set_reg_x_column,
                size="3",
                flex="1"
            ),
            rx.select(
                AppState.numeric_columns,
                placeholder="Select Y (Response)...",
                value=AppState.reg_y_column,
                on_change=AppState.set_reg_y_column,
                size="3",
                flex="1"
            ),
            rx.select(
                ["2", "3", "4", "5"],
                value=AppState.poly_degree,
                on_change=AppState.set_poly_degree,
                size="3",
                width="120px"
            ),
            width="100%",
            spacing="4",
            margin_bottom="1em"
        ),

        rx.button(
            "Run Polynomial Regression",
            on_click=AppState.run_polynomial_regression,
            color_scheme="violet",
            size="3",
            margin_bottom="1em",
        ),

        rx.cond(
            AppState.polynomial_report,
            rx.box(
                rx.vstack(
                    rx.text(AppState.polynomial_report.equation, font_weight="bold", size="5", color="#5b21b6"),

                    rx.hstack(
                        rx.badge(f"R²: {AppState.polynomial_report.r2}", color_scheme="blue", size="3", radius="full"),
                        rx.badge(f"RMSE: {AppState.polynomial_report.rmse}", color_scheme="red", size="3", radius="full"),
                        rx.badge(f"MAE: {AppState.polynomial_report.mae}", color_scheme="orange", size="3", radius="full"),
                        spacing="4",
                        margin_y="0.5em"
                    ),

                    rx.text(AppState.polynomial_report.interpretation, color="gray", font_style="italic", margin_bottom="1.5em"),

                    rx.recharts.composed_chart(
                        rx.recharts.x_axis(data_key="x", type_="number", name=AppState.reg_x_column),
                        rx.recharts.y_axis(type_="number", name=AppState.reg_y_column),
                        rx.recharts.graphing_tooltip(),

                        rx.recharts.line(
                            data_key="y", 
                            stroke="#5b21b6", 
                            stroke_width=0, 
                            dot=True,
                            name="Actual Data"
                        ),
                        rx.recharts.line(
                            data_key="poly_fit",
                            stroke="#ec4899",
                            dot=False,
                            stroke_width=2,
                            name="Polynomial Curve"
                        ),

                        data=AppState.polynomial_chart_data,
                        width="100%",
                        height=350,
                    ),

                    spacing="3",
                    align_items="center",
                    width="100%"
                ),
                padding="1.5em",
                bg="#f5f3ff",
                border="1px solid #ddd6fe",
                border_radius="8px",
                width="100%",
                text_align="center"
            ),
            rx.text("Select variables and degree, then run the analysis.", color="gray", size="2")
        ),

        padding="1.5em",
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_top="1em",
        width="100%"
    )