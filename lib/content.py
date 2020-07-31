import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from lib import title, sidebar, map, charts, model, tabs

dropdown_type = {
    "background-color": "white",
    "fontColor": "white",
    "font-family": "Helvetica Neue",
    "font-size": 12,
}

def build_characterization():
    return [
        html.Div([
            dbc.Row([
                dbc.Col([
                    sidebar.sidebar,
                    map.map(),
                ]),
            ]),
            dbc.Row([
                html.Div([
                    dcc.Graph(id="characterization-line")
                ],
                className='col-lg-6 mt-5'
                ),
                 html.Div([
                    dcc.Graph(id="characterization-bar")
                ],
                className='col-lg-6 mt-5'
                ),
                html.Div([
                    dcc.Graph(id="characterization-block")
                ],
                className='col-xl-12 col-lg-12 mt-5 charts_container'
                )
            ])

        ])
    ]

def build_network():
    return [
        html.Div(children=[
            html.Div(
                [
                    dcc.Dropdown(
                        id='cluster_dropdown',
                        options=[{'label': 'CLUSTER {}'.format(d), 'value': d} for d in range(12)],
                        value=4,
                        multi=False,
                        style=dropdown_type,
                    ),
                    dcc.Graph(id='cluster_plot'),
                ], className='col-xl-12 col-lg-12 mt-5 charts_container'),

        ])
    ]

def build_prediction():
    return [
        html.Div([
            html.Br(),
            html.H3('Predictive Modelling', style={'color': '#fefefe'}),
            html.Div([model.predictorUI], style={'color': '#fefefe'})
        ])
    ]