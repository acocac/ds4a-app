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
#from app import app




#############################
# Load map data
#############################
# engine = create_engine('postgresql://team_60:natesh@nicolasviana.chhlcoydquoi.us-east-2.rds.amazonaws.com/minjusticia')
# df = pd.read_sql(sql='select * from reincidentes left join municipios on reincidentes.ciudad=municipios.municipio', con=engine, parse_dates=['fecha_ingreso'])
# df = pd.read_sql(sql='select * from reincidentes', con=engine, parse_dates=['fecha_ingreso'])
df = pd.read_csv('data/data_full_preprocessed_municipios.csv', parse_dates=['fecha_ingreso']) #if local > faster loading

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
        color_continuous_scale="Viridis",         
        opacity=0.5,                              
        )

Map_Fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=4,
    mapbox_center={"lat": 4.570868, "lon": -74.2973328})

Map_Fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

##############################
#Map Layout
##############################
map = html.Div([
 #Place the main graph component here:
  dcc.Graph(figure=Map_Fig, id='COL_map')
], className="mini_container")

#
# ###municipios
# #Create the map:
#
# dff_municipios = df.groupby(['interno', 'municipio']).count().reset_index()  # count unique convict ID
# dff_municipios = dff_municipios.groupby(['municipio']).count().reset_index()
#
# municipio_geo = df[['municipio','x','y']]
# municipio_geo.drop_duplicates(inplace=True)
#
# municipio_x = municipio_geo.set_index('municipio')['x'].to_dict()
# municipio_y = municipio_geo.set_index('municipio')['y'].to_dict()
#
# dff_municipios['x'] = dff_municipios["municipio"].map(municipio_x)
# dff_municipios['y'] = dff_municipios["municipio"].map(municipio_y)
#
# def map_municipios(df):
#     Map_municipios = px.scatter_mapbox(
#             df,
#             lat="y",
#             lon="x",
#             # color="confirmed",
#             size="interno",
#             size_max=50,
#             hover_name="municipio",
#             hover_data=["interno"],
#             # color_continuous_scale=color_scale,
#     )
#
#     Map_municipios.update_layout(
#         mapbox_style="carto-positron",
#         mapbox_zoom=4,
#         mapbox_center={"lat": 4.570868, "lon": -74.2973328})
#
#     Map_municipios.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#     return(Map_municipios)
#
# ##############################
# #Map Layout
# ##############################
# map_municipios = html.Div([
#  #Place the main graph component here:
#   dcc.Graph(figure=Map_municipios, id='COL_adm1_map')
# ], className="mini_container")