import dash_bootstrap_components as dbc
from dash import html

Navbar = dbc.Row(
    dbc.Col(
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(
                    dbc.NavLink(
                        "Assess Yourself", href="/assess-yourself", id="assess-yourself"
                    ),
                    style={"cursor": "pointer"},
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "Assess Others",
                        href="/asses-others",
                        id="asses-others",
                    ),
                    style={"cursor": "pointer"},
                ),
                dbc.NavItem(
                    dbc.NavLink("Dashboard", href="/dashboard"),
                    style={"cursor": "pointer"},
                ),
                dbc.NavItem(dbc.NavLink("About", href="/about")),
                # dbc.DropdownMenu(
                #     children=[
                #         dbc.DropdownMenuItem("English", header=True),
                #         dbc.DropdownMenuItem("Russian", href="#"),
                #         dbc.DropdownMenuItem("German", href="#"),
                #     ],
                #     nav=True,
                #     in_navbar=True,
                #     label="Language"
                # ),
            ],
            brand="Attachment Style Test",
            brand_href="/",
            color="primary",
            dark=True,
        ),
        className="mb-4",
    )
)

NavbarCustom = html.Div(
    [
        dbc.NavLink("Attachment Style Test", href="/"),
        html.Div(
            [
                html.Div(
                    dbc.Stack(
                        [
                            dbc.NavLink(
                                "Assess Yourself",
                                href="/assess-yourself",
                                id="assess-yourself",
                                style={"cursor": "pointer"},
                            ),
                            dbc.NavLink(
                                "Assess Others",
                                href="/asses-others",
                                id="asses-others",
                                style={"cursor": "pointer"},
                            ),
                            dbc.NavLink(
                                "Dashboard",
                                href="/dashboard",
                                style={"cursor": "pointer"},
                            ),
                            dbc.NavLink(
                                "About",
                                href="/about",
                                style={"cursor": "pointer"},
                            ),
                        ],
                        direction="horizontal",
                        gap=3,
                    ),
                    hidden=True,
                ),
                html.Button(
                    html.I(className="bi bi-list"),
                    className="border-0",
                    hidden=False,
                ),
            ]
        ),
    ],
    className="d-flex justify-content-between bg-light p-3 mb-4",
)
