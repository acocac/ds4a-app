import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

from datetime import datetime as dt
import json
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

#Recall app
from app import app

engine = create_engine('postgresql://team_60:natesh@nicolasviana.chhlcoydquoi.us-east-2.rds.amazonaws.com/minjusticia')
df = pd.read_sql(sql='select * from reincidentes', con=engine, parse_dates=['fecha_ingreso'])
# df = pd.read_csv('data/data_full_preprocessed.csv', parse_dates=['fecha_ingreso']) #if local > faster loading

getVariables = html.Div([
                    html.Div([
                        html.P("Edad:", className="control_label"),
                        dcc.Input(id='edad-input', type='number',
                                  min=18, max=100, step=1),
                        ],
                    className="flex-display",
                    ),
                    html.Br(),
                    html.Div(
                        [
                            html.P("Delito Calificado:", className="control_label"),
                            dcc.Input(id='calificado-input', type='number',
                                      min=0, max=1, step=1),
                        ],
                    className="flex-display",
                    ),
                    html.Br(),
                    html.Div(
                    [
                        html.P("Agravado:", className="control_label"),
                        dcc.Input(id='agravado-input', type='number',
                                  min=0, max=1, step=1),
                    ],
                    className="flex-display",
                    )
                ]
                , className="mini-container", id="variables_predictor"
                )