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

###############################################################
# BAR PLOT
###############################################################

# def plot_demographics(dataset, age, genre):
#       bins = [18, 25, 35, 45, 55, 65, 100]
#       labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
#       dataset["age_range"] = pd.cut(dataset[age], bins, labels = labels, include_lowest = True)
#       gb_df = dataset.groupby(["age_range", genre])["interno"].count().reset_index().sort_values("interno", ascending = False)
#       # plot_demographics(gb_df["edad"], gb_df["genero"])
#       f, ax = plt.subplots(figsize=(6, 6))
#       ax = sns.barplot(x="interno", y="age_range", data=gb_df[gb_df["genero"] == "MASCULINO"], color='skyblue', label="Men", orient='h', lw=0)
#       ax = sns.barplot(x="interno", y="age_range", data=gb_df[gb_df["genero"] == "FEMENINO"], color='pink', label="Women", orient='h', lw=0)
#       sns.despine(left=True, bottom=True)
#       ax.set_xlabel("Convicts")
#       ax.set_title("Demographics")
#       return ax

# ax = plot_demographics(df, "edad", "genero")

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

#stats2=html.Div([
	#Place the different graph components here.
#    dbc.Row([
#        dbc.Col(
 #           dcc.Graph(figure=ax, id='Bar')
  #      )
   # ]),
	#],className="ds4a-body")