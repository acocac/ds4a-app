#import data related libraries
import dash_bootstrap_components as dbc
# import dash related libraries
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# import local libraries
from lib.features import *

#engine = create_engine('postgresql://team_60:natesh@nicolasviana.chhlcoydquoi.us-east-2.rds.amazonaws.com/minjusticia')
#df = pd.read_sql(sql='select * from reincidentes', con=engine, parse_dates=['fecha_ingreso'])
df = pd.read_csv('data/data_full_preprocessed.csv', parse_dates=['fecha_ingreso']) #if local > faster loading

#add new features
df = features(df)

#line plot object
def line_Plot(df, geographicValue):
    if geographicValue == 'Department':
        fig = px.line(df, x="Ingreso_Month", y="interno", color="depto_establecimiento")
    elif geographicValue == 'City':
        fig = px.line(df, x="Ingreso_Month", y="interno", color="mpio_establecimiento")
    fig.update_layout(title=f'Monthly convicts in selected {geographicValue}(s)', paper_bgcolor="#F8F9F9")
    return fig

def getLine(geographicValue, states, startPeriod, endPeriod):
    if geographicValue == 'Department':
        tmp = df[df['depto_abr'].isin(states)]
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)] # filter dataset by the daterange
        tmp = tmp.groupby(['interno', 'depto_establecimiento', 'Ingreso_Month']).count().reset_index()
        grouped = tmp.groupby(['depto_establecimiento', 'Ingreso_Month']).count().reset_index()
    elif geographicValue == 'City':
        tmp = df[(df['Ingreso_Month'] >= startPeriod) & (df['Ingreso_Month'] < endPeriod)] # filter dataset by the daterange
        tmp = tmp.groupby(['interno', 'mpio_establecimiento', 'Ingreso_Month']).count().reset_index()  # count unique convict ID
        grouped = tmp.groupby(['mpio_establecimiento', 'Ingreso_Month']).count().reset_index()
    fig = line_Plot(grouped, geographicValue)
    return fig

#bar plot object
def bar_Plot(df, geographicValue):
    fig = px.bar(df, y="age_range", x="interno", color='genero', orientation='h')
    fig.update_layout(title=f'Demographics Distribution in selected {geographicValue}(s)', paper_bgcolor="#F8F9F9")
    return fig

def getBar(geographicValue, states, startPeriod, endPeriod):
    if geographicValue == 'Department':
        targetvar = "depto_establecimiento"
    elif geographicValue == 'City':
        targetvar = "mpio_establecimiento"

    tmp = df[df['depto_abr'].isin(states)]
    tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)] # filter dataset by the daterange
    tmp = tmp[["interno", "edad", "genero", targetvar]]
    tmp.drop_duplicates(subset="interno", keep='first', inplace=True)
    tmp = tmp.reset_index(drop=True)
    bins = [18, 25, 35, 45, 55, 65, 100]
    labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    tmp['age_range'] = pd.cut(tmp.edad, bins, labels=labels, include_lowest=True)
    grouped = tmp.groupby(["age_range", "genero", targetvar])["interno"].count().reset_index().sort_values("age_range")
    fig = bar_Plot(grouped, geographicValue)
    return fig