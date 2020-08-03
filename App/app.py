# import dash related libraries
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import warnings

warnings.filterwarnings('ignore')

# import local libraries
from callbacks import register_callbacks
from lib import tabs
from lib import title

# create dash App server
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config['suppress_callback_exceptions'] = True

# layout
app.layout = html.Div(className="body-bk", children=
[
    html.Div(className="title_wrap", children=
    [
        dbc.Row([
            dbc.Col([
                html.Div([title.title])
            ])
        ])
    ]),

    html.Div(className="ds4a-body", children=
    [
        html.Div([
            tabs.build_tabs()
        ])
    ])
]
                      )

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=False, port=8181)