#import data related libraries
import pandas as pd
from sqlalchemy import create_engine

#import dash related libraries
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

#import local libraries
from lib.map import *
from lib.charts import *
from lib.features import *


def register_callbacks(app):

    # callback update_map
    @app.callback(
        [
            Output('map', 'figure'),
        ],
        [
            Input("geographic_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ]
    )
    def update_map(geographicValue, start_date, end_date):
        figure = get_map_data(geographicValue, start_date, end_date)
        return [figure]

    #callback map interaction
    @app.callback(
        Output('state_dropdown','value'),
        [
            Input('map','clickData')
        ],
        [
            State('state_dropdown','value')
        ]

    )
    def click_saver(clickData,state):
        if clickData is None:
            raise PreventUpdate

        state.append(clickData['points'][0]['location'])

        return state

    #callback line plot
    @app.callback(
        [
            Output('characterization-line', 'figure')
        ],
        [
            Input("geographic_dropdown", "value"),
            Input("state_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ]
    )
    def update_line(geographicValue, state_dropdown, start_date, end_date):
        figure = getLine(geographicValue, state_dropdown, start_date, end_date)
        return [figure]

    #callback bar plot
    @app.callback(
        [
            Output('characterization-bar', 'figure')
        ],
        [
            Input("geographic_dropdown", "value"),
            Input("state_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ]
    )
    def update_bar(geographicValue, state_dropdown, start_date, end_date):
        figure = getBar(geographicValue, state_dropdown, start_date, end_date)
        return [figure]