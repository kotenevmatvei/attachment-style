from dash import html

Footer = (
    html.Div(
        html.Footer(
            "Created by Matvei Kotenev. Contact via kotenev.matvei@gmail.com.",
        ),
        style={
            "position": "sticky",
            "textAlign": "center",
            "padding-top": "5px",
            "padding-bottom": "5px",
            "font-size": "12px",
        },
    )
)
