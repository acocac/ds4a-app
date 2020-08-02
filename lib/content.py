# import dash related libraries
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# import local libraries
from lib import sidebar, map, model


def build_characterization():
    return [
        html.Div([
            dbc.Row([
                dbc.Col([
                    sidebar.characterization(),
                    map.map(),
                ]),
            ]),
            dbc.Row([
                html.Div([
                    dcc.Graph(id="characterization-barsentence")
                ],
                    className='col-lg-6 mt-5'
                ),
                html.Div([
                    dcc.Graph(id="characterization-barage")
                ],
                    className='col-lg-6 mt-5'
                ),
                html.Div([
                    dcc.Graph(id="characterization-line")
                ],
                    className='col-xl-12 col-lg-12 mt-5 charts_container'
                ),
                html.Div([
                    dcc.Graph(id="characterization-block")
                ],
                    className='col-xl-12 col-lg-12 mt-5 charts_container'
                ),
                # table.renderTable()
            ])

        ])
    ]


def build_network():
    return [
        html.Div([
            dbc.Row([
                dbc.Col([
                    sidebar.network(),
                ]),
            ]),
            dbc.Row([
                html.Div([
                    dcc.Graph(id='cluster_plot'),
                ], className='col-xl-12 col-lg-12 mt-5 charts_container'),
            ])
        ])
    ]


def build_prediction():
    return [
        html.Div([
            dbc.Row([
                dbc.Col([
                    sidebar.prediction(),
                ]),
            ]),
            dbc.Row([
                html.Div([
                    html.H6("The result of the prediction whether the intern would reoffend is: ",
                            style={'color': '#fefefe'}),
                    html.H2("Response: ", style={'color': '#fefefe'}),
                    html.H2('', id='outputTarget', style={'color': '#fefefe'}),
                    html.H6("with a probability of: ", style={'color': '#fefefe'}),
                    html.H3('', id="outputProbability", style={'color': '#fefefe'}),
                    model.plotImp(),
                ], className='col-xl-12 col-lg-12 mt-5 charts_container'),
            ])
        ])
    ]