# import dash_bootstrap_components as dbc
# from dash import html, dcc, Input, State, Output, callback
# from data.options import (
#     attachment_score_labels_values,
#     demographics_labels_values,
#     attachment_style_options,
# )
# import pandas as pd
# import plotly.express as px
# 
# ScatterModal = dbc.Modal(
#     [
#         dbc.ModalHeader(dbc.ModalTitle("Scatter Plot")),
#         dbc.ModalBody(
#             [
#                 html.Label("Select X-axis Variable:"),
#                 dcc.Dropdown(
#                     id="scatter-x-dropdown",
#                     options=({"label": "Age", "value": "age"},)
#                     + attachment_score_labels_values,
#                     value="age",
#                 ),
#                 html.Label("Select Y-axis Variable:"),
#                 dcc.Dropdown(
#                     id="scatter-y-dropdown",
#                     options=attachment_score_labels_values,
#                     value="avoidant_score",
#                 ),
#                 html.Div(
#                     "Please choose the Y variable different from X",
#                     id="scatter-y-warning",
#                     style={"color": "red"},
#                     hidden=True,
#                 ),
#                 html.Label("Color By:"),
#                 dcc.Dropdown(
#                     id="scatter-color-dropdown",
#                     options=({"label": "None", "value": "None"},)
#                     + demographics_labels_values,
#                     value="gender",
#                 ),
#                 dcc.Graph(id="scatter-graph"),
#             ]
#         ),
#         dbc.ModalFooter(
#             dbc.Button(
#                 "Close",
#                 id="close-scatter",
#                 className="ms-auto",
#                 n_clicks=0,
#             )
#         ),
#     ],
#     id="scatter-modal",
#     size="lg",
#     is_open=False,
# )
# 
# ScatterThumbnail = html.Div(
#     dcc.Graph(
#         id="scatter-thumbnail",
#         config={"staticPlot": True},
#         style={"cursor": "pointer"},
#     ),
#     id="scatter-container",
#     className="thumbnail",
# )
# 
# 
# # toggle modal
# @callback(
#     Output("scatter-modal", "is_open"),
#     [Input("scatter-container", "n_clicks"), Input("close-scatter", "n_clicks")],
#     State("scatter-modal", "is_open"),
# )
# def toggle_scatter_modal(open_modal, close_modal, is_open):
#     if open_modal or close_modal:
#         return not is_open
#     return is_open
# 
# 
# # update scatter thumbnail
# @callback(
#     Output("scatter-thumbnail", "figure"),
#     [
#         Input("scatter-x-dropdown", "value"),
#         Input("scatter-y-dropdown", "value"),
#         Input("scatter-color-dropdown", "value"),
#         Input("data-store", "data"),
#         Input("window-width", "data"),
#     ],
# )
# def update_scatter_thumbnail(x_var, y_var, color_var, data, window_width):
#     if window_width[0] > 500:
#         if color_var == "None":
#             fig = px.scatter(
#                 data,
#                 x=x_var,
#                 y=y_var,
#                 title="Scatter Plot by Demographics",
#                 width=300,
#                 height=250,
#             )
#         else:
#             fig = px.scatter(
#                 data,
#                 x=x_var,
#                 y=y_var,
#                 color=color_var,
#                 title="Scatter Plot by Demographics",
#                 width=300,
#                 height=250,
#             )
#         fig.update_layout(
#             title_x=0.55,
#             title_y=0.98,
#             xaxis_title="",
#             yaxis_title="",
#             margin=dict(t=30, r=0, l=0),
#             showlegend=False,
#             paper_bgcolor="#F5F5F4",
#         )
#     else:
#         if color_var == "None":
#             fig = px.scatter(
#                 data,
#                 x=x_var,
#                 y=y_var,
#                 title="Scatter Plot",
#                 width=175,
#                 height=175,
#             )
#         else:
#             fig = px.scatter(
#                 data,
#                 x=x_var,
#                 y=y_var,
#                 color=color_var,
#                 title="Scatter Plot",
#                 width=175,
#                 height=175,
#             )
#         fig.update_layout(
#             title_font_size=15,
#             title_x=0.57,
#             title_y=0.95,
#             xaxis_title="",
#             yaxis_title="",
#             margin=dict(t=30, r=0, l=0),
#             showlegend=False,
#             paper_bgcolor="#F5F5F4",
#         )
#         fig.update_xaxes(showticklabels=False)
#         fig.update_yaxes(showticklabels=False)
#     return fig
# 
# 
# # don't let the dummies choose the same attachment style for x and y axes
# @callback(Output("scatter-y-dropdown", "options"), Input("scatter-x-dropdown", "value"))
# def update_scatter_y_options(x_value):
#     not_used_options = [
#         {"label": key, "value": val}
#         for key, val in attachment_style_options.items()
#         if val != x_value
#     ]
#     return not_used_options
# 
# 
# # update scatter graph
# @callback(
#     [Output("scatter-graph", "figure"), Output("scatter-y-warning", "hidden")],
#     [
#         Input("scatter-x-dropdown", "value"),
#         Input("scatter-y-dropdown", "value"),
#         Input("scatter-color-dropdown", "value"),
#         Input("data-store", "data"),
#     ],
# )
# def update_scatter_graph(x_var, y_var, color_var, data):
#     if y_var is None:
#         return px.scatter([]), False
#     if color_var == "None":
#         fig = px.scatter(
#             data,
#             x=x_var,
#             y=y_var,
#             title=f'{y_var.split("_")[0].capitalize()} vs {x_var.capitalize()}',
#         )
#     else:
#         fig = px.scatter(
#             data,
#             x=x_var,
#             y=y_var,
#             color=color_var,
#             title=f'{y_var.split("_")[0].capitalize()} vs {x_var.capitalize()} Colored '
#             f'by {color_var.replace("_", " ").title()}',
#         )
#     fig.update_xaxes(title=x_var.replace("_", " ").title())
#     fig.update_yaxes(title=y_var.replace("_", " ").title())
#     return fig, True
