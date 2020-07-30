import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
import pickle

modelo_dash = pickle.load(open("model/Model_dash.pickle", "rb"))

# Predictor Function
def pred_reincidente(model , x):
    pred = model.predict_proba(x)
    print("Model Response:")
    if pred[:, 0] > pred[:, 1]:
        return print("NON-RECIDIVIST with a probability of: ", pred[:, 0]) #Probabilities of non recidivist [0]
    else:
        return print("RECIDIVIST with a probability of: ", pred[:, 1]) #Probabilities of non recidivist [0]

#Ejemplo de datos ( se reemplazaria cada valor con el input que ingresa el usuario en el dash)
test_r = pd.DataFrame({'edad' :[30],
                        'sentencia':[5.5],
                        'actividades_estudio':[0],
                        'CLUSTER_4':[1],
                        'actividades_trabajo':[1],
                        'calificado':[1],
                        'nivel_educativo':[4],
                        'estado_ingreso_Intramuros':[1],
                        'cuenta_delitos':[3],
                        'agravado':[1],
                        'CLUSTER_5':[0],
                        'CLUSTER_1':[0],
                        'genero':[1]}
                       )

response = pred_reincidente(modelo_dash, test_r)

# layout
predictorUI = dbc.Row([
                dbc.Col([
                     html.Div([
                        html.Div([
                            html.P("Age:", className="control_label"),
                            dcc.Input(id='edad-input', type='number', min=18, max=100, step=1),
                            ], className="flex-display",
                        ),
                        # html.Br(),
                        html.Div([
                            html.P("Genre:", className="control_label"),
                            dcc.Input(id='genero-input', type='number', min=0, max=1, step=1),
                            ], className="flex-display",
                        ),
                        #html.Br(),
                        html.Div([
                            html.P("Sentence:", className="control_label"),
                            dcc.Input(id='sentencia-input', type='number', min=0, max=50, step=1),
                            ], className="flex-display",
                        ),
                        #html.Br(),
                        html.Div([
                            html.P("Study activities:", className="control_label"),
                            dcc.Input(id='estudio-input', type='number', min=0, max=1, step=1),
                            ], className="flex-display",
                        ),
                        # html.Br(),
                        html.Div([
                            html.P("Education Level:", className="control_label"),
                            dcc.Input(id='educativo-input', type='number', min=0, max=11, step=1),
                            ], className="flex-display",
                        ),
                        # html.Br(),
                        html.Div([
                            html.P("Work Activities:", className="control_label"),
                            dcc.Input(id='trabajo-input', type='number', min=0, max=1, step=1),
                            ], className="flex-display",
                        ),
                        # html.Br(),
                        html.Div([
                            html.P("Intramuros state:", className="control_label"),
                            dcc.Input(id='intramuros-input', type='number', min=0, max=1, step=1),
                            ], className="flex-display",
                        ),
                        # html.Br(),
                        html.Div([
                            html.P("Crimes count:", className="control_label"),
                            dcc.Input(id='delitos-input', type='number', min=0, max=20, step=1),
                            ], className="flex-display",
                        ),
                        # html.Br(),
                        html.Div([
                            html.P("Crime(s) Calificado:", className="control_label"),
                            dcc.Input(id='calificado-input', type='number', min=0, max=1, step=1),
                            ], className="flex-display",
                        ),
                        # html.Br(),
                        html.Div([
                            html.P("Crime(s) Agravado:", className="control_label"),
                            dcc.Input(id='agravdo-input', type='number', min=0, max=1, step=1),
                            ], className="flex-display",
                        ),
                        # html.Br(),
                        html.Div([
                            html.P("Belongs to crime group 1:", className="control_label"),
                            dcc.Input(id='cluster1-input', type='number', min=0, max=1, step=1),
                        ], className="flex-display",
                        ),
                        # html.Br(),
                        html.Div([
                            html.P("Belongs to crime group 4:", className="control_label"),
                            dcc.Input(id='cluster4-input', type='number', min=0, max=1, step=1),
                            ], className="flex-display",
                        ),
                        # html.Br(),
                        html.Div([
                            html.P("Belongs to crime group 5:", className="control_label"),
                            dcc.Input(id='cluster5-input', type='number', min=0, max=1, step=1),
                        ], className="flex-display",
                        ),

                        html.Br(),
                        html.Hr(),
                        html.Div([
                            html.Button('Predict', id='predict-button')
                        ])
                    ]
                    , className="mini-container", id="variables_predictor"
                    )
                ]),

                dbc.Col([
                    html.Div([
                        html.H6("The result of the prediction whether the intern would reoffend is: "),
                        html.H2("Response: "),
                        html.Div([response], id="predictor_output"),
                        html.H6("with a probability of: "),
                        html.H3(children="75%", id="predictor_proba")
                    ])
                ], className="mini_container", id="output_predictor")
            ])