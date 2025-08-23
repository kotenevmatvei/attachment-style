from dash import html

DebugFooter = html.Div(
    html.Footer(
        "Created by Matvei Kotenev. Contact via kotenev.matvei@gmail.com.",
    ),
    style={
        "position": "sticky",
        "textAlign": "center",
        "padding-top": "5px",
        "padding-bottom": "5px",
        "font-size": "12px",
        "background-color": "#F5F5F4",
    },
)
