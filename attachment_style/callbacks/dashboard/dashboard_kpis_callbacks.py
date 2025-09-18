import pandas as pd
from dash import Output, Input, State, callback
from dash.exceptions import PreventUpdate

from utils.calculations import calculate_kpis


@callback(
    [
        Output("dominant-style-kpi", "children"),
        Output("dominant-gender-kpi", "children"),
        Output("dominant-therapy-experience-kpi", "children"),
        Output("total-submissions-kpi", "children"),
    ],
    Input("presented-data-store", "data"),
    State("url", "pathname"),
)
def update_kpi_cards(scores, pathname):
    print("calculating kpis")

    if pathname != "/dashboard":
        print("woopsi wrong page")
        PreventUpdate()

    df = pd.DataFrame(scores)

    (total_submissions, gender_label, gender_percentage, therapy_experience_label, therapy_experience_percentage,
     dominant_style_label, dominant_style_percentage) = calculate_kpis(df)
    print("calculated...")

    return (
        f"{dominant_style_label}: {dominant_style_percentage}%",
        f"{gender_label}: {gender_percentage}%",
        f"{therapy_experience_label}: {therapy_experience_percentage}%",
        f"{total_submissions}",
    )
