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
                    html.H2('', id='outputTarget', style={'color': '#FFFF00', 'font-weight': 'bold'}),
                    html.H6("with a probability of: ", style={'color': '#fefefe'}),
                    html.H3('', id="outputProbability", style={'color': '#FFFF00', 'font-weight': 'bold'}),
                    model.plotImp(),
                    html.H5("Interpretation", style={'color': '#fefefe', 'font-weight': 'bold'}),
                    html.Div([html.Label(
                        "The above plot of XGBoost's model feature weights shows Age and Sentence length are by far the features that the sub-models inside XGB use the most to classify the recidivist/non-recidivist individuals. Other features like Education level and Intramuros state are also frequnetly used to predict the probability of recidivism.")
                    ], className='control_label'),
                ], className='col-xl-12 col-lg-12 mt-5 charts_container'),
            ])
        ])
    ]