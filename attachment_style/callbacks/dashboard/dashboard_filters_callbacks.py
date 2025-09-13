import pandas as pd
from dash import callback, Input, Output, State

from utils.database import retrieve_scores_from_db


@callback(
    Output("data-store", "data"),
    Input("refresh-data-button", "n_clicks"),
    prevent_initial_call=True,
)
def refresh_data(n_clicks):
    scores = retrieve_scores_from_db()
    return scores


@callback(
    [
        Output("presented-data-store", "data"),
        Output("dataset-multiselect", "error"),
    ],
    [
        Input("dataset-multiselect", "value"),
        Input("include-test-data-switch", "checked"),
        Input("data-store", "data"),
    ],
    State("presented-data-store", "data"),
    prevent_initial_call=True,
)
def select_dataset(dataset_selection, include_test_data, data, presented_data):
    df = pd.DataFrame(data)

    dataset_selection_error = None
    if dataset_selection == ["assess_yourself"]:
        df = df[df["source"] == "AssessYourself"]
    elif dataset_selection == ["assess_others"]:
        df = df[df["source"] == "AssessOthers"]
    elif set(dataset_selection) != {"assess_yourself", "assess_others"}:
        # leave presented data as it is and return error
        df = pd.DataFrame(presented_data)
        dataset_selection_error = "Please select at least one dataset"

    if not include_test_data:
        df = df[df["test"] == False]

    filtered_data = df.to_dict(orient="list")

    return filtered_data, dataset_selection_error
