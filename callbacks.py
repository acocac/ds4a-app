# import dash related libraries
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_html_components as html

# import local libraries
from lib import charts, network, map, model
from controls import YEARS, MONTHS


def register_callbacks(app):
    # callback update_map
    @app.callback(
        [
            Output('map', 'figure'),
        ],
        [
            Input("geographic_dropdown", "value"),
            Input("target_dropdown", "value"),
            Input("year-slider", "value"),
            Input("month-slider", "value")
        ]
    )
    def update_map(geographicValue, target_dropdown, year, month):
        figure = map.get_map_data(geographicValue, target_dropdown, year, month)
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
            Input("year-slider", "value"),
            Input("month-slider", "value")
        ]
    )
    def update_line(geographicValue, target_dropdown, state_dropdown, year, month):
        if None in state_dropdown:
            state_dropdown = ['BOGOTA D.C.']
        figure = charts.getLine(geographicValue, target_dropdown, state_dropdown, year, month)
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
            Input("year-slider", "value"),
            Input("month-slider", "value")
        ]
    )
    def update_bar(geographicValue, target_dropdown, state_dropdown, year, month):
        if None in state_dropdown:
            state_dropdown = ['BOGOTA D.C.']
        figure = charts.getBarage(geographicValue, target_dropdown, state_dropdown, year, month)
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
            Input("year-slider", "value"),
            Input("month-slider", "value")
        ]
    )
    def update_barsentence(geographicValue, target_dropdown, state_dropdown, year, month):
        if None in state_dropdown:
            state_dropdown = ['BOGOTA D.C.']
        figure = charts.getBarsentence(geographicValue, target_dropdown, state_dropdown, year, month)
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
            Input("year-slider", "value"),
            Input("month-slider", "value")
        ]
    )
    def update_block(geographicValue, target_dropdown, state_dropdown, year, month):
        if None in state_dropdown:
            state_dropdown = ['BOGOTA D.C.']
        figure = charts.getBlock(geographicValue, target_dropdown, state_dropdown, year, month)
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

    # callback slider years
    @app.callback(
        Output('year_range', 'children'),
        [
            Input("year-slider", "value")
        ]
    )
    def slider_value(value):
        start = YEARS[value[0]]
        end = YEARS[value[1]]
        selected = '{} - {}'.format(start, end)
        return [
            html.P(
                selected,
                className="slider_label",
                id='year-selected'
            )
        ]

    # callback slider months
    @app.callback(
        Output('month_range', 'children'),
        [
            Input("month-slider", "value")
        ]
    )
    def slider_value(value):
        start = MONTHS[value[0]]
        end = MONTHS[value[1]]
        selected = '{} - {}'.format(start, end)
        return [
            html.P(
                selected,
                className="slider_label",
                id='month-selected'
            )
        ]

    # callback slider predictors
    @app.callback(
        [
            Output('edad-range', 'children'),
            Output('genero-range', 'children'),
            Output('sentencia-range', 'children'),
            Output('estudio-range', 'children'),
            Output('education-range', 'children'),
            Output('trabajo-range', 'children'),
            Output('intramuros-range', 'children'),
            Output('delitos-range', 'children'),
            Output('calificado-range', 'children'),
            Output('agravado-range', 'children'),
            Output('cluster1-range', 'children'),
            Output('cluster4-range', 'children'),
            Output('cluster5-range', 'children')
        ],
        [
            Input("edad-slider", "value"),
            Input("genero-slider", "value"),
            Input("sentencia-slider", "value"),
            Input("estudio-slider", "value"),
            Input("educativo-slider", "value"),
            Input("trabajo-slider", "value"),
            Input("intramuros-slider", "value"),
            Input("delitos-slider", "value"),
            Input("calificado-slider", "value"),
            Input("agravado-slider", "value"),
            Input("cluster1-slider", "value"),
            Input("cluster4-slider", "value"),
            Input("cluster5-slider", "value")
        ]
    )
    def slider_value(age, gender, sentence, estudio, education,
                     work, intramuros, crimes, calificado, agravado,
                     cluster1, cluster4, cluster5):
        return [
            html.Label(
                'Age: {}'.format(age),
                className="control_label",
                id='edad-selected'
            ),
            html.Label(
                'Gender: {}'.format(gender),
                className="control_label",
                id='genero-selected'
            ),
            html.Label(
                'Sentence length (years): {}'.format(sentence),
                className="control_label",
                id='sentencia-selected'
            ),
            html.Label(
                'Study activities: {}'.format(estudio),
                className="control_label",
                id='estudio-selected'
            ),
            html.Label(
                'Education level: {}'.format(education),
                className="control_label",
                id='educativo-selected'
            ),
            html.Label(
                'Work activities: {}'.format(work),
                className="control_label",
                id='trabajo-selected'
            ),
            html.Label(
                'Intramuros state: {}'.format(intramuros),
                className="control_label",
                id='intramuros-selected'
            ),
            html.Label(
                'Crimes count: {}'.format(crimes),
                className="control_label",
                id='delitos-selected'
            ),
            html.Label(
                'Crime(s) Calificado: {}'.format(calificado),
                className="control_label",
                id='calificado-selected'
            ),
            html.Label(
                'Crime(s) Agravado: {}'.format(agravado),
                className="control_label",
                id='agravado-selected'
            ),
            html.Label(
                'Belongs to crime group 1: {}'.format(cluster1),
                className="control_label",
                id='cluster1-selected'
            ),
            html.Label(
                'Belongs to crime group 4: {}'.format(cluster4),
                className="control_label",
                id='cluster4-selected'
            ),
            html.Label(
                'Belongs to crime group 5: {}'.format(cluster5),
                className="control_label",
                id='cluster5-selected'
            ),
        ]

    ##old slider single variables
    # # callback slider prediction age
    # @app.callback(
    #     [
    #         Output('edad-range', 'children')
    #     ],
    #     [
    #         Input("edad-slider", "value")
    #     ]
    # )
    # def slider_value(value):
    #     selected = 'Age: {}'.format(value)
    #     return [
    #         html.P(
    #             selected,
    #             className="control_label",
    #             id='age-selected',
    #             style={'font-weight': 'bold'}
    #         )
    #     ]
    #
    ##old callbacks using DatePicker
    # # callback bar plot
    # @app.callback(
    #     [
    #         Output('characterization-barsentence', 'figure')
    #     ],
    #     [
    #         Input("geographic_dropdown", "value"),
    #         Input("target_dropdown", "value"),
    #         Input("state_dropdown", "value"),
    #         Input("date_picker", "start_date"),
    #         Input("date_picker", "end_date")
    #     ]
    # )
    # def update_barsentence(geographicValue, target_dropdown, state_dropdown, start_date, end_date):
    #     if None in state_dropdown:
    #         state_dropdown = ['BOGOTA D.C.']
    #     figure = charts.getBarsentence(geographicValue, target_dropdown, state_dropdown, start_date, end_date)
    #     return [figure]

    # # callback bar plot
    # @app.callback(
    #     [
    #         Output('characterization-barage', 'figure')
    #     ],
    #     [
    #         Input("geographic_dropdown", "value"),
    #         Input("target_dropdown", "value"),
    #         Input("state_dropdown", "value"),
    #         Input("date_picker", "start_date"),
    #         Input("date_picker", "end_date")
    #     ]
    # )
    # def update_bar(geographicValue, target_dropdown, state_dropdown, start_date, end_date):
    #     if None in state_dropdown:
    #         state_dropdown = ['BOGOTA D.C.']
    #     figure = charts.getBarage(geographicValue, target_dropdown, state_dropdown, start_date, end_date)
    #     return [figure]

    # # callback line plot
    # @app.callback(
    #     [
    #         Output('characterization-line', 'figure')
    #     ],
    #     [
    #         Input("geographic_dropdown", "value"),
    #         Input("target_dropdown", "value"),
    #         Input("state_dropdown", "value"),
    #         Input("date_picker", "start_date"),
    #         Input("date_picker", "end_date")
    #     ]
    # )
    # def update_line(geographicValue, target_dropdown, state_dropdown, start_date, end_date):
    #     if None in state_dropdown:
    #         state_dropdown = ['BOGOTA D.C.']
    #     figure = charts.getLine(geographicValue, target_dropdown, state_dropdown, start_date, end_date)
    #     return [figure]
    #
    # # callback block plot
    # @app.callback(
    #     [
    #         Output('characterization-block', 'figure')
    #     ],
    #     [
    #         Input("geographic_dropdown", "value"),
    #         Input("target_dropdown", "value"),
    #         Input("state_dropdown", "value"),
    #         Input("date_picker", "start_date"),
    #         Input("date_picker", "end_date")
    #     ]
    # )
    # def update_block(geographicValue, target_dropdown, state_dropdown, start_date, end_date):
    #     if None in state_dropdown:
    #         state_dropdown = ['BOGOTA D.C.']
    #     figure = charts.getBlock(geographicValue, target_dropdown, state_dropdown, start_date, end_date)
    #     return [figure]