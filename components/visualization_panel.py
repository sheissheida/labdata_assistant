import reflex as rx
from labdata_assistant.state import AppState


def visualization_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Visualization v1: Categorical Distribution", size="4"),
        rx.text("Interactive charts for your categorical data.", color="gray"),

        rx.cond(
            AppState.categorical_column_names.length() > 0,
            rx.vstack(
                rx.hstack(
                    rx.select(
                        AppState.categorical_column_names,
                        placeholder="Select a column...",
                        value=AppState.selected_categorical_column,
                        on_change=AppState.set_selected_categorical_column,
                        size="3",
                        width="100%",
                    ),
                    rx.radio(
                        ["bar", "pie"],
                        value=AppState.chart_type,
                        on_change=AppState.set_chart_type,
                        direction="row",
                        size="3",
                    ),
                    width="100%",
                    margin_bottom="1em",
                    align_items="center"
                ),

                rx.cond(
                    AppState.categorical_chart_data.length() > 0,
                    rx.cond(
                        AppState.chart_type == "bar",
                        rx.recharts.bar_chart(
                            rx.recharts.bar(
                                data_key="count",
                                fill="#3b82f6",
                                radius=[4, 4, 0, 0]
                            ),
                            rx.recharts.x_axis(data_key="name"),
                            rx.recharts.y_axis(),
                            rx.recharts.graphing_tooltip(),
                            data=AppState.categorical_chart_data,
                            width="100%",
                            height=350,
                        ),
                        rx.recharts.pie_chart(
                            rx.recharts.pie(
                                data=AppState.categorical_chart_data,
                                data_key="count",
                                name_key="name",
                                cx="50%",
                                cy="50%",
                                outer_radius=120,
                                label=True,
                            ),
                            rx.recharts.graphing_tooltip(),
                            width="100%",
                            height=350,
                        )
                    ),
                    rx.text("Please select a column from the dropdown above.", color="gray", size="2")
                ),
                width="100%"
            ),
            rx.text("Run Categorical Analysis first to unlock visualizations.", color="orange", size="2")
        ),

        padding="1.5em",
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_top="1em",
        width="100%"
    )