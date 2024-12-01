import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, callback, register_page, dcc
from attachment_style.utils.utils import get_data_from_db, aggregate_scores
import plotly.express as px

register_page(__name__, path="/dashboard_modal")


df1, df2 = get_data_from_db(test=True)
df1, df2 = aggregate_scores(df1, df2)
answers_df = df1
attachment_styles = ["avoidant_score", "secure_score", "anxious_score"]

distro = html.Div(
    [
        html.Label("Select Attachment Style:"),
        dcc.Dropdown(
            id="attachment-style-dropdown",
            options=[
                {
                    "label": style.split("_")[
                        0
                    ].capitalize(),
                    "value": style,
                }
                for style in attachment_styles
            ],
            value="avoidant_score",
        ),
        dcc.Graph(id="distribution-histogram-modal"),
    ]
)

def layout(**kwargs):
    return html.Div(
        [
            dbc.Button("Open modal", id="open", n_clicks=0),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Header")),
                    dbc.ModalBody(distro),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
                    ),
                ],
                id="modal",
                is_open=False,
            ),
        ]
    )


@callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Callbacks for interactivity
@callback(
    Output("distribution-histogram-modal", "figure"),
    [
        Input("attachment-style-dropdown", "value"),
        # Input("data_store", "data"),
    ]
)
def update_distribution(selected_style):#, data):
    # answers_df = pd.DataFrame(data)
    fig = px.histogram(  # type: ignore
        answers_df,
        x=selected_style,
        nbins=20,
        title=f'Distribution of {selected_style.split("_")[0].capitalize()} Attachment Scores',
    )
    fig.update_xaxes(
        title=selected_style.split("_")[0].capitalize() + " Attachment Score"
    )
    fig.update_yaxes(title="Count")
    return fig
