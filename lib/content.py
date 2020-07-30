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
                    html.Div(
                        [
                            dcc.Graph(id="characterization-line")
                        ],
                        className="charts_container",
                    ),
                    html.Div(
                        [
                            dcc.Graph(id="characterization-bar")
                        ],
                        className="charts_container",
                    ),
                    html.Div(
                        [
                            dcc.Graph(id="characterization-block")
                        ],
                        className="charts_container",
                    ),
                ]),
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