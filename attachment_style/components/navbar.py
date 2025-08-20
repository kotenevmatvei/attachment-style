# import dash_bootstrap_components as dbc
# from dash import html, callback, Input, Output
#
#
# Navbar = (
#     html.Div(
#         html.Div(
#             [
#                 dbc.NavLink("Attachment Style Test", href="/", className="fs-4"),
#                 html.Div(
#                     [
#                         html.Div(
#                             dbc.Stack(
#                                 [
#                                     dbc.NavLink(
#                                         "Home",
#                                         href="/",
#                                         style={
#                                             "cursor": "pointer",
#                                             "margin-right": "4px",
#                                         },
#                                     ),
#                                     dbc.NavLink(
#                                         "Assess Yourself",
#                                         href="/assess-yourself",
#                                         id="assess-yourself",
#                                         style={"cursor": "pointer"},
#                                     ),
#                                     dbc.NavLink(
#                                         "Assess Others",
#                                         href="/asses-others",
#                                         id="asses-others",
#                                         style={"cursor": "pointer"},
#                                     ),
#                                     dbc.NavLink(
#                                         "Dashboard",
#                                         href="/dashboard",
#                                         style={"cursor": "pointer"},
#                                     ),
#                                     dbc.NavLink(
#                                         "About",
#                                         href="/about",
#                                         style={"cursor": "pointer"},
#                                     ),
#                                 ],
#                                 direction="horizontal",
#                                 gap=3,
#                             ),
#                             className="navbar-large",
#                         ),
#                         html.Button(
#                             html.I(className="bi bi-list", style={"font-size": "25px"}),
#                             className="border-0 d-sm-none bg-transparent",
#                             id="hamburger",
#                             n_clicks=0,
#                         ),
#                     ]
#                 ),
#             ],
#             className="d-flex justify-content-between align-items-center p-3",
#         )
#     )
# )
#
# NavbarMobile = html.Div(
#     [
#         dbc.NavLink(
#             "Home",
#             href="/",
#             id="home-sidenav",
#             style={"cursor": "pointer"},
#             className="sidenav-link pt-5",
#         ),
#         dbc.NavLink(
#             "Assess Yourself",
#             href="/assess-yourself",
#             id="assess-yourself-sidenav",
#             style={"cursor": "pointer"},
#             className="sidenav-link",
#         ),
#         dbc.NavLink(
#             "Assess Others",
#             href="/asses-others",
#             id="assess-others-sidenav",
#             style={"cursor": "pointer"},
#             className="sidenav-link",
#         ),
#         dbc.NavLink(
#             "Dashboard",
#             href="/dashboard",
#             id="dashboard-sidenav",
#             style={"cursor": "pointer"},
#             className="sidenav-link",
#         ),
#         dbc.NavLink(
#             "About",
#             href="/about",
#             id="about-sidenav",
#             style={"cursor": "pointer", "flex": "1"},
#             className="sidenav-link",
#         ),
#     ],
#     id="Sidenav",
# )
#
#
# @callback(
#     [
#         Output("Sidenav", "className"),
#         Output("opacity", "className"),
#     ],
#     Input("hamburger", "n_clicks"),
# )
# def open_sidenav(hamburger_click):
#     if hamburger_click:
#         return "open", "open"
#     return "", ""
#
#
# @callback(
#     [
#         Output("Sidenav", "className", allow_duplicate=True),
#         Output("opacity", "className", allow_duplicate=True),
#     ],
#     [
#         Input("home-sidenav", "n_clicks"),
#         Input("assess-yourself-sidenav", "n_clicks"),
#         Input("assess-others-sidenav", "n_clicks"),
#         Input("dashboard-sidenav", "n_clicks"),
#         Input("about-sidenav", "n_clicks"),
#     ],
#     prevent_initial_call=True,
# )
# def fold_sidenavbar(
#     close_home, close_yourself, close_others, close_dashboard, close_about
# ):
#     # if home_click or yourself_click or others_click or dashboard_click or about_click:
#     if close_home or close_yourself or close_others or close_dashboard or close_about:
#         return "", ""
