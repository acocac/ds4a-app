#import data related libraries
import json
import pandas as pd
from sqlalchemy import create_engine
from decouple import config

#import dash related libraries
import dash_core_components as dcc
import dash_html_components as html

# import viz related libraries
import plotly.express as px

#import local libraries
from lib import features


mapbox_token = config("MAPBOX_SECRET")
mapbox_style = config("MAPBOX_STYLE")
px.set_mapbox_access_token(mapbox_token)


#load data
# engine = create_engine(config('DATABASE_URL'))
# df = pd.read_sql(sql='select * from reincidentes', con=engine, parse_dates=['fecha_ingreso'])
df = pd.read_csv('data/data_full_preprocessed.csv', parse_dates=['fecha_ingreso']) #if local > faster loading


#load geojson
with open('data/national.geojson') as json_file:
    national = json.load(json_file)

with open('data/departamentos.geojson') as geo:
    departamentos = json.loads(geo.read())


#add new features
df = features.add_features(df)


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

    _min = min(df['normalized_count'])
    _max = max(df['normalized_count'])

    fig=px.choropleth_mapbox(df,
                             locations='depto_establecimiento',
                             color='normalized_count',
                             range_color=(_min, _max),
                             geojson=departamentos,
                             featureidkey="properties.NOMBRE_DPT",
                             color_continuous_scale=px.colors.sequential.deep,
                             opacity=0.5,
                             hover_data=['depto_establecimiento','interno', 'normalized_count'],
                             labels={'normalized_count': '% Convicts'}
                             )

    fig.update_layout(
        title_text="Convicts",
        paper_bgcolor="#2c2f38",
        plot_bgcolor='#2c2f38',
        mapbox_style=mapbox_style,
        mapbox_zoom=4,
        mapbox_center={"lat": 4.570868, "lon": -74.2973328},
        font=dict(color='#fefefe'))

    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"

    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br><i>Number of convicts: %{customdata[1]} <br><i>% of the national convicts: %{customdata[2]:.2f}"
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


##
def map_national(df):
    fig = px.choropleth_mapbox(df,
                               locations='National',
                               color='interno',
                               geojson=national,
                               featureidkey="properties.national",
                               color_discrete_map="Viridis",
                               opacity=0.5,
                               hover_data=['interno'],
                               labels={'interno': 'Total Convicts'},
                               )

    fig.update_layout(
        title_text="Convicts",
        paper_bgcolor="#2c2f38",
        plot_bgcolor='#2c2f38',
        mapbox_style=mapbox_style,
        mapbox_zoom=4,
        mapbox_center={"lat": 4.570868, "lon": -74.2973328})

    fig.update_layout(coloraxis_showscale=False)

    fig.update_traces(
        hovertemplate="<i>Number of convicts: %{customdata[0]}"
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


def get_map_data(geographicValue, target, startPeriod, endPeriod):
    if geographicValue == 'Department':
        tmp = df[df['target'] == target]
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)] # filter dataset by the daterange
        tmp = tmp.groupby(['interno', 'depto_establecimiento']).count().reset_index()  # count unique convict ID
        grouped = tmp.groupby(['depto_establecimiento']).count().reset_index()
        grouped['normalized_count'] = 100 * grouped['interno'] / grouped['interno'].sum()
        missing_depto = {'depto_establecimiento': ["VAUPES", "VICHADA", "GUAVIARE", "GUAINIA"], 'interno': [0, 0, 0, 0], 'normalized_count': [0, 0, 0, 0]}
        add_missing = pd.DataFrame(data=missing_depto)
        grouped_final = pd.concat([grouped, add_missing], ignore_index=True)
        grouped_final.fillna(0, inplace=True)
        figure = map_departamentos(grouped_final)

    elif geographicValue == 'National':
        tmp = df[df['target'] == target]
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)] # filter dataset by the daterange
        tmp[geographicValue] = "Colombia"
        tmp = tmp.groupby(['interno', geographicValue]).count().reset_index()  # count unique convict ID
        grouped = tmp.groupby([geographicValue]).count().reset_index()
        figure = map_national(grouped)

    return figure