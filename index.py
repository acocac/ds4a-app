#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

#Dash Bootstrap Components
import dash_bootstrap_components as dbc 

#data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json
from sqlalchemy import create_engine

#Recall app
from app import app



###########################################################
#
#           APP LAYOUT:
#
###########################################################

#LOAD THE DIFFERENT FILES
from lib import title, sidebar, col_map, stats

#PLACE THE COMPONENTS IN THE LAYOUT
app.layout =html.Div(
    [ 
      col_map.map,
      stats.stats,
      title.title,
      sidebar.sidebar,
    ],
    className="ds4a-app", #You can also add your own css files by locating them into the assets folder
)

 
    
###############################################   
#
#           APP INTERACTIVITY:
#
###############################################

###############################################################
#Load and modify the data that will be used in the app.
#################################################################
# engine = create_engine()
# df = pd.read_sql(sql='select * from reincidentes', con=engine, parse_dates=['fecha_ingreso'])
df = pd.read_csv('data/data_full_preprocessed.csv', parse_dates=['fecha_ingreso']) #if local > faster loading

with open('data/departamentos.geojson') as geo:
    geojson = json.loads(geo.read())

with open('data/states_col.json') as f:
    states_dict = json.loads(f.read())

df['depto_abr'] = df['depto_establecimiento'].map(states_dict)
df['Ingreso_Month'] = pd.to_datetime(df['fecha_ingreso'].map(lambda x: "{}-{}".format(x.year, x.month)))


#############################################################
# SCATTER & LINE PLOT : Add sidebar interaction here
#############################################################
@app.callback(
    [Output("Line", "figure")],
    [
        Input("state_dropdown", "value"),
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date")
    ],
)
def make_line_plot(state_dropdown, start_date, end_date):
    ddf = df[df['depto_abr'].isin(state_dropdown)]
    ddf = ddf[(ddf['fecha_ingreso'] >= start_date) & (ddf['fecha_ingreso'] < end_date)]

    ddf1 = ddf.groupby(['interno', 'depto_establecimiento','Ingreso_Month']).count().reset_index()
    ddf1 = ddf1.groupby(['depto_establecimiento','Ingreso_Month']).count()
    ddf1 = ddf1.reset_index()

    Line_fig=px.line(ddf1,x="Ingreso_Month",y="interno", color="depto_establecimiento")
    Line_fig.update_layout(title='Montly Convicts in selected deparments',paper_bgcolor="#F8F9F9")

    return [Line_fig]


#############################################################
# MAP : Add interactions here
#############################################################

#MAP date interaction
@app.callback(
    Output("COL_map", "figure"),
    [
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date")
    ],
)
def update_map(start_date,end_date):
    dff = df[(df['Ingreso_Month'] >= start_date) & (df['Ingreso_Month'] < end_date)] # filter dataset by the daterange
    dff = dff.groupby(['interno', 'depto_abr']).count().reset_index() #count unique convict ID
    dff = dff.groupby(['depto_abr']).count().reset_index()

    fig_map2=px.choropleth_mapbox(dff,
        locations='depto_abr',
        color='interno',
        geojson=geojson,
        featureidkey="properties.depto_abr",
        zoom=4,
        mapbox_style="carto-positron", 
        center={"lat": 4.570868, "lon": -74.2973328},
        color_continuous_scale="Viridis",
        opacity=0.5,
        title='Colombia Convicts'
        )
    fig_map2.update_layout(title="COL Convicts",margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#F8F9F9", plot_bgcolor="#F8F9F9",)
    return fig_map2

#MAP click interaction

@app.callback(
    Output('state_dropdown','value'),
    [
        Input('COL_map','clickData')
    ],
    [
        State('state_dropdown','value')
    ]

)
def click_saver(clickData,state):
    if clickData is None:
        raise PreventUpdate

    state.append(clickData['points'][0]['location'])

    return state


if __name__ == "__main__":
    app.run_server(debug=True)