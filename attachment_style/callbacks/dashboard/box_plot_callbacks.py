from dash import callback, Output, Input
import plotly.express as px
import dash_mantine_components as dmc

import constants
from data.options import demographics_radio_options, demographics_values


# update box plot graph
@callback(
    Output("box-graph", "figure"),
    [
        Input("demographic-radio", "value"),
        Input("attachment-style-dropdown-demographics", "value"),
        Input("presented-data-store", "data"),
        Input("mantine-provider", "forceColorScheme"),
    ],
)
def update_box_graph(demographic, selected_style, data, theme):
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



    if theme == "light":
        fig.update_layout(template="mantine_light")
    else:
        fig.update_layout(template="mantine_dark")

    return fig
