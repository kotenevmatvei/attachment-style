import dash_bootstrap_components as dbc

Navbar = dbc.Row(
    dbc.Col(
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Test Yourself", href="#")),
                dbc.NavItem(dbc.NavLink("Test Your Partner", href="#")),
                dbc.NavItem(dbc.NavLink("About", href="#")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("English", header=True),
                        dbc.DropdownMenuItem("Russian", href="#"),
                        dbc.DropdownMenuItem("German", href="#"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Language"
                ),
            ],
            brand="Attachment Style Test",
            brand_href="#",
            color="primary",
            dark=True,
        ),
        className="mb-4",
    )
)
