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




#############################
# Load map data
#############################
# engine = create_engine()
# df = pd.read_sql(sql='select * from reincidentes', con=engine, parse_dates=['fecha_ingreso'])
df = pd.read_csv('data/data_full_preprocessed.csv', parse_dates=['fecha_ingreso'])  #if local > faster loading

with open('data/departamentos.geojson') as geo:
    geojson = json.loads(geo.read())

with open('data/states_col.json') as f:
    states_dict = json.loads(f.read())

df['depto_abr'] = df['depto_establecimiento'].map(states_dict)

#Create the map:
dff = df.groupby(['interno', 'depto_abr']).count().reset_index()  # count unique convict ID
dff = dff.groupby(['depto_abr']).count().reset_index()

Map_Fig=px.choropleth_mapbox(dff,
        locations='depto_abr',
        color='interno',
        geojson=geojson,
        featureidkey="properties.depto_abr",
        zoom=4,
        mapbox_style="carto-positron",            
        center={"lat": 4.570868, "lon": -74.2973328},
        color_continuous_scale="Viridis",         
        opacity=0.5,                              
        )
Map_Fig.update_layout(title='Colombia map',paper_bgcolor="#F8F9F9")


##############################
#Map Layout
##############################
map=html.Div([
 #Place the main graph component here:
  dcc.Graph(figure=Map_Fig, id='COL_map')
], className="ds4a-body")