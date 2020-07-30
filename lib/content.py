import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from lib import title, sidebar, map, charts, model, tabs

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
        html.Div([
            html.H3('Crime Network Analysis'),
            html.P('clustering of crimes according to similarity')
        ])
    ]

def build_prediction():
    return [
        html.Div([
            html.H3('Predictive Modelling'),
            html.P('used models logistic regression, random forest and XGBOOST'),
            html.Div([model.getVariables])
        ])
    ]