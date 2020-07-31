#import data related libraries
import json
import pandas as pd
from sqlalchemy import create_engine
from decouple import config

#import dash related libraries
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

#import local libraries
from lib.features import *

mapbox_token = config("MAPBOX_SECRET")
mapbox_style = config("MAPBOX_STYLE")

px.set_mapbox_access_token(mapbox_token)

#############################
# Load map data
#############################
# engine = create_engine(config('DATABASE_URL'))
# df = pd.read_sql(sql='select * from reincidentes', con=engine, parse_dates=['fecha_ingreso'])
df = pd.read_csv('data/data_full_preprocessed.csv', parse_dates=['fecha_ingreso']) #if local > faster loading

#geojson
with open('data/municipios.geojson') as json_file:
    municipios = json.load(json_file)

with open('data/departamentos.geojson') as geo:
    departamentos = json.loads(geo.read())

#add new features
df = features(df)

#map object
def map():
    return html.Div(
        [
            dcc.Graph(id="map", figure={})
        ],
        id="pretty_container seven columns",
        className="pretty_container",
    )

###departamentos
def map_departamentos(df):
    fig=px.choropleth_mapbox(df,
                             locations='depto_abr',
                             color='interno',
                             geojson=departamentos,
                             featureidkey="properties.depto_abr",
                             # color_continuous_scale="Viridis",
                             color_continuous_scale=px.colors.sequential.deep,
                             opacity=0.5,
                             )

    fig.update_layout(mapbox_style = "open-street-map")

    fig.update_layout(
        # template="plotly_dark",
        title_text="Convicts",
        paper_bgcolor="#2c2f38",
        plot_bgcolor='#2c2f38',
        mapbox_style=mapbox_style,
        mapbox_zoom=4,
        mapbox_center={"lat": 4.570868, "lon": -74.2973328},
        font=dict(color='#fefefe'))

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

###municipios
def map_municipios(df):
    fig = px.choropleth_mapbox(df,
                               locations='mpio_establecimiento',
                               color='interno',
                               geojson=municipios,
                               featureidkey="properties.NOMBRE_MPI",
                               color_continuous_scale="Viridis",
                               opacity=0.5,
                               )

    fig.update_layout(
        template="plotly_dark",
        mapbox_style="carto-positron",
        mapbox_zoom=4,
        mapbox_center={"lat": 4.570868, "lon": -74.2973328})

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

def get_map_data(geographicValue, target, startPeriod, endPeriod):
    if geographicValue == 'Department':
        tmp = df[df['target'] == target]
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)] # filter dataset by the daterange
        tmp = tmp.groupby(['interno', 'depto_abr']).count().reset_index()  # count unique convict ID
        grouped = tmp.groupby(['depto_abr']).count().reset_index()
        figure = map_departamentos(grouped)

    elif geographicValue == 'City':
        tmp = df[df['target'] == target]
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)] # filter dataset by the daterange
        tmp = tmp.groupby(['interno', 'mpio_establecimiento']).count().reset_index()  # count unique convict ID
        grouped = tmp.groupby(['mpio_establecimiento']).count().reset_index()
        figure = map_municipios(grouped)

    return figure