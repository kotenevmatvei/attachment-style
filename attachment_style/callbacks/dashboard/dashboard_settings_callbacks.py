import pandas as pd
from dash import callback, Input, Output, State

from utils.database import retrieve_scores_from_db


# refresh data
@callback(
    Output("data-store", "data"),
    Input("refresh-data-button", "n_clicks")
)
def refresh_data(n_clicks):
    scores = retrieve_scores_from_db()
    return scores

# include/exclude test data
@callback(
    Output("presented-data-store", "data"),
    Input("include-test-data-button", "checked"),
    State("data-store", "data")
)
def filter_test_data(checked, data):
    if checked:
        return data
    else:
        df = pd.DataFrame(data)
        df_test = df[df["test"] == False]
        data_test = df_test.to_dict(orient="list")
        return data_test