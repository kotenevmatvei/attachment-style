import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, html

app = Dash(__name__)

app.layout = dmc.MantineProvider(
    children = [dmc.Button("toggle button", id='toggle-button'),
    dmc.Text(id='my-text', children='This is some text'),
    dmc.Text("More Text yoo")
    ]
)

@app.callback(
    Output('my-text', 'style'),
    Input('toggle-button', 'n_clicks'),
)
def toggle_text(n_clicks):
    if n_clicks is None or n_clicks % 2 == 0:
        return {'display': 'block'}  # Show the text
    else:
        return {'display': 'none'}  # Hide the text

if __name__ == "__main__":
    app.run_server(debug=True)