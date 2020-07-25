#######################################################
# Main APP definition.
#
# Dash Bootstrap Components used for main theme and better
# organization. 
#######################################################

#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import warnings
warnings.filterwarnings('ignore')

#Dash Bootstrap Components
import dash_bootstrap_components as dbc

from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server

#We need this for function callbacks not present in the app.layout
app.config.suppress_callback_exceptions = True

###########################################################
#
#           APP LAYOUT:
#
###########################################################

#LOAD THE DIFFERENT FILES
from lib import title, sidebar, col_map, stats, model

#
#LOGO
DS4A_Img = html.Div(
            children=[
                html.Img(
                    src=app.get_asset_url("ds4a-img.svg"),
                    id="ds4a-image",
                    style={
                            "height": "60px",
                            "width": "auto",
                            #"margin-bottom": "10px",
                    }
                )
            ],
        )
#
#PLACE THE COMPONENTS IN THE LAYOUT
app.layout = html.Div(
         [
                html.Div(className="title_wrap", children=
                [
                dbc.Row([
                    # html.Div([title.title])
                    dbc.Col([
                        html.Div([DS4A_Img])
                    ]),
                    dbc.Col([
                        html.Div([title.title])
                    ])
                ])
                ]
                ),
             html.Div(className="ds4a-body", children=
                [
                    html.Div([
                        dcc.Tabs(id='tabs-header', value='tab-1', parent_className='custom-tabs', className='custom-tabs-container', children=[
                                dcc.Tab(value='tab-1', label='Characterization', className='custom-tab', selected_className='custom-tab--selected', children=[
                                    html.Div([
                                        dbc.Row([
                                            dbc.Col([
                                                sidebar.sidebar,
                                                col_map.map,
                                                # col_map.map_municipios,
                                                stats.stats,
                                                ])
                                            #dbc.Col([
                                            #    col_map.map
                                            #    ]),
                                            #dbc.Col([
                                            #    stats.stats
                                            ])
                                        ])
                                    ]),

                                dcc.Tab(value='tab-2', label='Prediction', className='custom-tab', selected_className='custom-tab--selected', children=[
                                    html.Div([
                                        html.H3('Predictive Modelling'),
                                        html.P('used models logistic regression, random forest and XGBOOST'),
                                        html.Div([model.getVariables])
                                            ])
                                    ]
                                ),

                                dcc.Tab(value='tab-3', label='Crime Network', className='custom-tab', selected_className='custom-tab--selected', children=[
                                    html.Div([
                                        html.H3('Crime Network Analysis'),
                                        html.P('clustering of crimes according to similarity')
                                            ])
                                    ]
                                )
                         ])
                    ])
                ])
         ]
)

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
