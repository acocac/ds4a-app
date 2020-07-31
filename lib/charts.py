#import data related libraries
import pandas as pd
from sqlalchemy import create_engine
from decouple import config

# import dash related libraries
import plotly.express as px

# import local libraries
from lib.features import *

#engine = create_engine(config('DATABASE_URL'))
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
    fig.update_layout(title=f'Monthly convicts in selected {geographicValue}(s)',
                      paper_bgcolor="#2c2f38",
                      plot_bgcolor='#2c2f38',
                      font=dict(color='#fefefe'),
                      xaxis_title='Date',
                      yaxis_title='Convicts',
                      # legend_title="",
                      # legend=dict(
                      #     orientation="h",
                      #     yanchor="bottom",
                      #     y=-0.3,
                      #     xanchor="right",
                      #     x=1
                      # )

                      )
    fig.update_traces(showlegend=False)

    return fig

def getLine(geographicValue, target, states, startPeriod, endPeriod):
    if geographicValue == 'Department':
        tmp = df[(df['depto_abr'].isin(states)) & (df['target'] == target)]
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)] # filter dataset by the daterange
        tmp = tmp.groupby(['interno', 'depto_establecimiento', 'Ingreso_Month']).count().reset_index()
        grouped = tmp.groupby(['depto_establecimiento', 'Ingreso_Month']).count().reset_index()
    elif geographicValue == 'City':
        tmp = df[df['target'] == target]
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)] # filter dataset by the daterange
        tmp = tmp.groupby(['interno', 'mpio_establecimiento', 'Ingreso_Month']).count().reset_index()  # count unique convict ID
        grouped = tmp.groupby(['mpio_establecimiento', 'Ingreso_Month']).count().reset_index()
    fig = line_Plot(grouped, geographicValue)

    for ser in fig['data']:
        ser['hovertemplate'] = '%{x}<br>%{y}'

    # fig.data[0].hovertemplate = '%{x}<br>%{y}'
    return fig

#bar plot object
def bar_Plot(df, geographicValue):
    fig = px.bar(df, y="age_range", x="interno", color='genero', orientation='h', color_discrete_sequence = ['#0075ee','#00b6cb'])
    fig.update_layout(title=f'Demographics Distribution in selected {geographicValue}(s)',
                      paper_bgcolor="#2c2f38",
                      plot_bgcolor='#2c2f38',
                      font=dict(color='#fefefe'),
                      # template="plotly_dark",
                      xaxis_title='Convicts',
                      yaxis_title='Age group',
                      # legend_title="",
                      # legend=dict(
                      #     orientation="h",
                      #     yanchor="bottom",
                      #     y=1.02,
                      #     xanchor="right",
                      #     x=1
                      # )
                      )
    fig.update_traces(showlegend=False)

    return fig

def getBar(geographicValue, target, states, startPeriod, endPeriod):
    tmp = df[df['target'] == target]

    if geographicValue == 'Department':
        targetgeo = "depto_establecimiento"
        tmp = tmp[tmp['depto_abr'].isin(states)]
    elif geographicValue == 'City':
        targetgeo = "mpio_establecimiento"

    tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)] # filter dataset by the daterange
    tmp = tmp[["interno", "edad", "genero", targetgeo]]
    tmp.drop_duplicates(subset="interno", keep='first', inplace=True)
    tmp = tmp.reset_index(drop=True)
    bins = [18, 25, 35, 45, 55, 65, 100]
    labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    tmp['age_range'] = pd.cut(tmp.edad, bins, labels=labels, include_lowest=True)
    # grouped = tmp.groupby(["age_range", "genero", targetgeo])["interno"].count().reset_index().sort_values("age_range")
    grouped = tmp.groupby(["age_range", "genero"])["interno"].count().reset_index().sort_values("age_range")
    fig = bar_Plot(grouped, geographicValue)
    fig.data[0].hovertemplate = '%{label}<br>%{value}'
    fig.data[1].hovertemplate = '%{label}<br>%{value}'
    return fig

#bar plot object
def block_Plot(df, geographicValue):
    fig = px.treemap(df, path=['delito'], values='count', color_discrete_sequence = px.colors.sequential.Plotly3)
    fig.data[0].hovertemplate = '%{label}<br>Record Count: %{value}'
    fig.update_layout(title=f'Top 50 offenses types in the selected {geographicValue}(s)',
                      # template="plotly_dark",
                      paper_bgcolor="#2c2f38",
                      font=dict(color='#fefefe'),
                      )
    return fig

def getBlock(geographicValue, target, states, startPeriod, endPeriod):
    tmp = df[df['target'] == target]

    if geographicValue == 'Department':
        targetgeo = "depto_establecimiento"
        tmp = tmp[tmp['depto_abr'].isin(states)]
    elif geographicValue == 'City':
        targetgeo = "mpio_establecimiento"

    tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)]  # filter dataset by the daterange
    tmp = tmp[["interno", "delito", "fecha_ingreso", "regional", targetgeo]].copy()
    grouped = tmp.groupby(["delito"]).size().reset_index(name="count").sort_values(by="count", ascending=False)
    
    if grouped.shape[0] > 50:
        grouped = grouped.iloc[:50]
    else:
        grouped

    fig = block_Plot(grouped, geographicValue)
    return fig