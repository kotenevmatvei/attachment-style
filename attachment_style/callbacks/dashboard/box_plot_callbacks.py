from dash import callback, Output, Input
import plotly.express as px

# update box plot graph
@callback(
    Output("box-graph", "figure"),
    [
        Input("demographic-radio", "value"),
        Input("attachment-style-dropdown-demographics", "value"),
        Input("data-store", "data"),
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
