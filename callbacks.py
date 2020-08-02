# import dash related libraries
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# import local libraries
from lib import charts, network, map, model


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
        figure = map.get_map_data(geographicValue, target_dropdown, start_date, end_date)
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
        if None in state_dropdown:
            state_dropdown = ['BOGOTA D.C.']
        figure = charts.getLine(geographicValue, target_dropdown, state_dropdown, start_date, end_date)
        return [figure]

    # callback bar plot
    @app.callback(
        [
            Output('characterization-barage', 'figure')
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
        if None not in state_dropdown:
            state_dropdown = ['BOGOTA D.C.']
        figure = charts.getBarage(geographicValue, target_dropdown, state_dropdown, start_date, end_date)
        return [figure]

    # callback bar plot
    @app.callback(
        [
            Output('characterization-barsentence', 'figure')
        ],
        [
            Input("geographic_dropdown", "value"),
            Input("target_dropdown", "value"),
            Input("state_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ]
    )
    def update_barsentence(geographicValue, target_dropdown, state_dropdown, start_date, end_date):
        if None not in state_dropdown:
            state_dropdown = ['BOGOTA D.C.']
        figure = charts.getBarsentence(geographicValue, target_dropdown, state_dropdown, start_date, end_date)
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
        if None not in state_dropdown:
            state_dropdown = ['BOGOTA D.C.']
        figure = charts.getBlock(geographicValue, target_dropdown, state_dropdown, start_date, end_date)
        return [figure]

    # callback network
    @app.callback(
        [Output('cluster_plot', 'figure')],
        [Input('cluster_dropdown', 'value')])
    def update_crime(cluster):
        figure = network.get_nplot(cluster)
        return [figure]

    # callback prediction
    @app.callback(
        [Output('outputTarget', 'children'),
         Output('outputProbability', 'children')],
        [Input('buttonPredict', 'n_clicks')],
        [State('edad-input', 'value'),
         State('genero-input', 'value'),
         State('sentencia-input', 'value'),
         State('estudio-input', 'value'),
         State('educativo-input', 'value'),
         State('trabajo-input', 'value'),
         State('intramuros-input', 'value'),
         State('delitos-input', 'value'),
         State('calificado-input', 'value'),
         State('agravado-input', 'value'),
         State('cluster1-input', 'value'),
         State('cluster4-input', 'value'),
         State('cluster5-input', 'value')
         ])
    def update_output(n_clicks, age, gender, sentence, study, education, work, intramuros, crimes, calificado, agravado, cluster1, cluster4, cluster5):
        target, probability = model.get_pred(age, gender, sentence, study, education, work, intramuros, crimes, calificado, agravado, cluster1, cluster4, cluster5)
        return [target, probability]