import dash_mantine_components as dmc
from dash_iconify import DashIconify

DashboardFilters = dmc.Flex(
    gap="md",
    justify="center",
    align="center",
    direction="row",
    wrap="wrap",
    mb="md",
    visibleFrom="sm",
    children=[
        dmc.Button(
            "Refresh Data",
            leftSection=DashIconify(
                icon="tabler:refresh", width=16
            ),
            variant="light",
            id="refresh-data-button",
        ),
        dmc.Text("Select the dataset:", size="lg"),
        dmc.MultiSelect(
            # label="Select the dataset:",
            data=[
                {"label": "Assess Yourself", "value": "assess_yourself"},
                {"label": "Assess Others", "value": "assess_others"},
            ],
            value=["assess_yourself", "assess_others"],
            size="lg",
            comboboxProps={"shadow": "lg"},
            id="dataset-multiselect"
        ),
        dmc.Switch("Include test data", size="lg", mr="xs", id="include-test-data-switch"),
    ],
)

DashboardFiltersMobile = dmc.Flex(
    gap="md",
    justify="center",
    align="center",
    direction="row",
    wrap="wrap",
    mb="md",
    hiddenFrom="sm",
    children=[
        dmc.MultiSelect(
            # label="Select the dataset:",
            data=[
                {"label": "Assess Yourself", "value": "assess_yourself"},
                {"label": "Assess Others", "value": "assess_others"},
            ],
            value=["assess_yourself", "assess_others"],
            size="lg",
            comboboxProps={"shadow": "lg"},
            id="dataset-multiselect-mobile"
        ),
        dmc.Button(
            "Refresh Data",
            leftSection=DashIconify(
                icon="tabler:refresh", width=16
            ),
            variant="light",
            id="refresh-data-button-mobile",
        ),
        dmc.Switch("Include test data", size="lg", mr="xs", id="include-test-data-switch-mobile"),
    ],
)
