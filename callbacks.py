# import dash related libraries
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# import local libraries
from lib.map import *
from lib.charts import *
from lib.cluster import *
from lib.tabs import *


def register_callbacks(app):
    # callback update_map
    @app.callback(
        [
            Output('map', 'figure'),
        ],
        [
            Input("geographic_dropdown", "value"),
            Input("target_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ]
    )
    def update_map(geographicValue, target_dropdown, start_date, end_date):
        figure = get_map_data(geographicValue, target_dropdown, start_date, end_date)
        return [figure]

    # callback map interaction
    @app.callback(
        Output('state_dropdown', 'value'),
        [
            Input('map', 'clickData')
        ],
        [
            State('state_dropdown', 'value')
        ]

    )
    def click_saver(clickData, state):
        if clickData is None:
            raise PreventUpdate

        state.append(clickData['points'][0]['location'])

        return state

    # callback line plot
    @app.callback(
        [
            Output('characterization-line', 'figure')
        ],
        [
            Input("geographic_dropdown", "value"),
            Input("target_dropdown", "value"),
            Input("state_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ]
    )
    def update_line(geographicValue, target_dropdown, state_dropdown, start_date, end_date):
        figure = getLine(geographicValue, target_dropdown, state_dropdown, start_date, end_date)
        return [figure]

    # callback bar plot
    @app.callback(
        [
            Output('characterization-bar', 'figure')
        ],
        [
            Input("geographic_dropdown", "value"),
            Input("target_dropdown", "value"),
            Input("state_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ]
    )
    def update_bar(geographicValue, target_dropdown, state_dropdown, start_date, end_date):
        figure = getBar(geographicValue, target_dropdown, state_dropdown, start_date, end_date)
        return [figure]

    # callback block plot
    @app.callback(
        [
            Output('characterization-block', 'figure')
        ],
        [
            Input("geographic_dropdown", "value"),
            Input("target_dropdown", "value"),
            Input("state_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ]
    )
    def update_block(geographicValue, target_dropdown, state_dropdown, start_date, end_date):
        figure = getBlock(geographicValue, target_dropdown, state_dropdown, start_date, end_date)
        return [figure]

    # callback network
    @app.callback(
        [Output('cluster_plot', 'figure')],
        [Input('cluster_dropdown', 'value')])
    def update_crime(cluster):
        figure = get_nplot(cluster)
        # return go.Figure(network_plot(cluster, complete_graph))
        return [figure]