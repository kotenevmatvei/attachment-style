from dash import callback, Output, Input, State
import plotly.express as px
import dash_mantine_components as dmc

import constants
from data.options import demographics_radio_options, demographics_values


# update box plot graph
@callback(
    Output("box-graph", "figure"),
    [
        Input("demographic-radio", "value"),
        Input("demographic-box-select-mobile", "value"), # mobile

        Input("attachment-style-dropdown-demographics", "value"),
        Input("attachment-style-box-select-mobile", "value"), # mobile

        Input("presented-data-store", "data"),
        Input("mantine-provider", "forceColorScheme"),
        Input("window-width", "data"),
    ],
)
def update_box_graph(demographic, demographic_mobile, selected_style, selected_style_mobile, data, theme, window_width):
    if window_width > 500:
        fig = px.box(
            data,
            x=demographic,
            y=selected_style,
            title=f'{selected_style.split("_")[0].capitalize()} '
                  f'Attachment Scores by {demographic.replace("_", " ").title()}',
            category_orders={demographic: demographics_values[demographic]}
        )
        fig.update_xaxes(title=demographic.replace("_", " ").title())
        fig.update_yaxes(
            title=selected_style.split("_")[0].capitalize() + " Attachment Score"
        )
    else:
        print(f"\ndemographic: {demographic_mobile}")
        print(f"\nattachment_style: {selected_style_mobile}")
        fig = px.box(
            data,
            x=demographic_mobile,
            y=selected_style_mobile,
            title=f'{selected_style_mobile.split("_")[0].capitalize()} '
                  f'Attachment Scores by {demographic_mobile.replace("_", " ").title()}',
            category_orders={demographic_mobile: demographics_values[demographic_mobile]}
        )
        fig.update_xaxes(title=demographic_mobile.replace("_", " ").title())
        fig.update_yaxes(
            title=selected_style_mobile.split("_")[0].capitalize() + " Attachment Score"
        )


    if window_width < 500:
        fig.update_layout(
            title="",
            width=350,
            height=330,
            margin=dict(l=0, r=0, t=20, b=0)
        )

    if theme == "light":
        fig.update_layout(template="mantine_light")
    else:
        fig.update_layout(template="mantine_dark")

    return fig

@callback(
    Output("box-info-modal", "opened"),
    Input("box-info-modal-button", "n_clicks"),
    State("box-info-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_box_info_modal(n_clicks, opened):
    return not opened