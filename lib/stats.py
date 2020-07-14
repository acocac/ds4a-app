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

# engine = create_engine()
# df = pd.read_sql(sql='select * from reincidentes', con=engine, parse_dates=['fecha_ingreso'])
df = pd.read_csv('data/data_full_preprocessed.csv', parse_dates=['fecha_ingreso']) #if local > faster loading

###############################################################
# LINE PLOT
###############################################################

df['Ingreso_Month'] = pd.to_datetime(df['fecha_ingreso'].map(lambda x: "{}-{}".format(x.year, x.month)))

#Next, we filter the data by month and selected states
states=['BOGOTA D.C.', 'ATLANTICO']

ddf=df[df['depto_establecimiento'].isin(states)]
ddf=ddf.groupby(['interno','depto_establecimiento','Ingreso_Month']).count().reset_index()
ddf=ddf.groupby(['depto_establecimiento','Ingreso_Month']).count().reset_index()

Line_fig=px.line(ddf,x="Ingreso_Month",y="interno", color="depto_establecimiento")
Line_fig.update_layout(title='Montly Convicts in selected deparments',paper_bgcolor="#F8F9F9")


#################################################################################
# Here the layout for the plots to use.
#################################################################################
stats=html.Div([ 
	#Place the different graph components here.
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=Line_fig, id='Line')
        )
    ]),
	],className="ds4a-body")