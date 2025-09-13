"""
These are components needed to avoid the "not found in layout" error when the original ones are hidden by dmc.Collapse.
Otherwise, dash looks for them when the user switches the color theme and throws an error since they are hidden when
another page is open or the collapses collapsed at that step in the test-flow.
"""

from dash import callback, Output, Input, dcc
import dash_mantine_components as dmc

DummyResultsChart = dmc.Collapse(
    dcc.Graph("results-chart", figure={}),
    id="dummy-results-chart-collapse"
)

@callback(
    Output("dummy-results-chart-collapse", "opened"),
    Input("results-board-collapse", "opened"),
)
def register_dummy_results_chart_in_layout(original_opened):
    return not original_opened
