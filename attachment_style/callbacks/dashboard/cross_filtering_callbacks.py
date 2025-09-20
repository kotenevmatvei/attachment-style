import pandas as pd
import numpy as np
from dash import callback, Output, Input, State
from data.options import demographics_values


@callback(
    Output("presented-data-store", "data", allow_duplicate=True),
    [
        Input("scatter-graph", "relayoutData"),
        Input("scatter-x-dropdown", "value"),
        Input("scatter-y-dropdown", "value"),
    ],
    [
        State("data-store", "data"),
        State("presented-data-store", "data"),
    ],
    prevent_initial_call=True,
)
def crossfilter_by_scatter_zoom(relayoutData, x_var, y_var, data, presented_data):
    df = pd.DataFrame(data)

    if relayoutData and "xaxis.range[0]" in relayoutData:
        x_var_min = relayoutData["xaxis.range[0]"]
        x_var_max = relayoutData["xaxis.range[1]"]
        y_var_min = relayoutData["yaxis.range[0]"]
        y_var_max = relayoutData["yaxis.range[1]"]

        df = df[(df[x_var] >= x_var_min) & (df[x_var] <= x_var_max)]
        df = df[(df[y_var] >= y_var_min) & (df[y_var] <= y_var_max)]
        filtered_data = df.to_dict()

        return filtered_data

    return presented_data

@callback(
    Output("presented-data-store", "data", allow_duplicate=True),
    [
        Input("box-graph", "relayoutData"),
        Input("demographic-radio", "value"),
        Input("attachment-style-dropdown-demographics", "value"),
    ],
    [
        State("data-store", "data"),
        State("presented-data-store", "data"),
    ],
    prevent_initial_call=True,
)
def crossfilter_by_box_zoom(relayoutData, x_var, y_var, data, presented_data):
    df = pd.DataFrame(data)

    if relayoutData and "xaxis.range[0]" in relayoutData:
        x_var_min = relayoutData["xaxis.range[0]"]
        x_var_max = relayoutData["xaxis.range[1]"]
        y_var_min = relayoutData["yaxis.range[0]"]
        y_var_max = relayoutData["yaxis.range[1]"]

        if x_var_min > 0 or x_var_max < 0:
            df = df[df[x_var] != demographics_values[x_var][0]]
        if x_var_min > 1 or x_var_max < 1:
            df = df[df[x_var] != demographics_values[x_var][1]]
        if x_var_min > 2 or x_var_max < 2:
            df = df[df[x_var] != demographics_values[x_var][2]]

        df = df[(df[y_var] >= y_var_min) & (df[y_var] <= y_var_max)]

        filtered_data = df.to_dict()
        return filtered_data

    return presented_data
