# TODO:
# - Add dynamic dropdown menu for the field Geographic level
# - Fix CSS
# -

# import dash related libraries
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import warnings

warnings.filterwarnings('ignore')

# import local libraries
from callbacks import register_callbacks
from lib.tabs import *
from lib.title import *

# create dash app server
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config['suppress_callback_exceptions'] = True

# logo
DS4A_Img = html.Div(
    children=[
        html.Img(
            src=app.get_asset_url("ds4a-img.svg"),
            id="ds4a-image",
            style={
                "height": "60px",
                "width": "auto",
                # "margin-bottom": "10px",
            }
        )
    ],
)

# layout
app.layout = html.Div(
    [
        html.Div(className="title_wrap", children=
        [
            dbc.Row([
                dbc.Col([
                    html.Div([DS4A_Img])
                ]),
                dbc.Col([
                    html.Div([title])
                ])
            ])
        ]
                 ),
        html.Div(className="ds4a-body", children=
        [
            html.Div([
                build_tabs()
            ])
        ])
    ]
)

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8080)