import dash_bootstrap_components as dbc

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
                    dbc.NavLink("Dashboard", href="/dashboard_modal"), style={"cursor": "pointer"}
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
