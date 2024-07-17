import dash_bootstrap_components as dbc

Navbar = dbc.Row(
    dbc.Col(
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Test Yourself", href="/test-yourself", id="test-yourself"), style={'cursor': 'pointer'}),
                dbc.NavItem(dbc.NavLink("Test Your Partner", href="/", id="test-your-partner"), style={'cursor': 'pointer'}),
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
