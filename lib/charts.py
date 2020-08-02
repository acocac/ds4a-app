#import data related libraries
import pandas as pd
from sqlalchemy import create_engine
from decouple import config

# import viz related libraries
import plotly.express as px

# import local libraries
from lib import features


#load data
#engine = create_engine(config('DATABASE_URL'))
#df = pd.read_sql(sql='select * from reincidentes', con=engine, parse_dates=['fecha_ingreso'])
df = pd.read_csv('data/data_full_preprocessed.csv', parse_dates=['fecha_ingreso']) #if local > faster loading


#add new features
df = features.add_features(df)


#line plot object
def line_Plot(df, geographicValue):
    if geographicValue == 'Department':
        ttext = f'Monthly convicts in selected selected {geographicValue}(s)'
    elif geographicValue == 'National':
        ttext = f'Monthly convicts in Colombia'

    if geographicValue == 'Department':
        fig = px.line(df, x="Ingreso_Month", y="interno", color="depto_establecimiento")
    elif geographicValue == 'National':
        fig = px.line(df, x="Ingreso_Month", y="interno", color="national")
    fig.update_layout(title=ttext,
                      paper_bgcolor="#2c2f38",
                      plot_bgcolor='#2c2f38',
                      font=dict(color='#fefefe'),
                      xaxis_title='Date',
                      yaxis_title='Number of convicts',
                      legend_title="",
                      legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=-0.3,
                          xanchor="right",
                          x=1
                      )

                      )
    fig.update_traces(showlegend=True)

    return fig


def getLine(geographicValue, target, states, startPeriod, endPeriod):
    if geographicValue == 'Department':
        tmp = df[(df['depto_establecimiento'].isin(states)) & (df['target'] == target)]
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)] # filter dataset by the daterange
        tmp = tmp.groupby(['interno', 'depto_establecimiento', 'Ingreso_Month']).count().reset_index()
        grouped = tmp.groupby(['depto_establecimiento', 'Ingreso_Month']).count().reset_index()
    elif geographicValue == 'National':
        tmp = df[df['target'] == target]
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)]  # filter dataset by the daterange
        grouped = tmp.groupby(['Ingreso_Month']).count().reset_index()  # count unique convict ID
        grouped['national'] = "Colombia"

    fig = line_Plot(grouped, geographicValue)

    for ser in fig['data']:
        ser['hovertemplate'] = '%{x}<br>%{y}'

    return fig


#bar plot object
def barage_Plot(df, geographicValue):
    if geographicValue == 'Department':
        ttext = f'Demographics Distribution in selected {geographicValue}(s)'
    elif geographicValue == 'National':
        ttext = f'Demographics Distribution in Colombia'

    fig = px.bar(df, y="age_range", x="interno", color='genero', orientation='h', color_discrete_sequence = ['#0075ee','#00b6cb'])

    fig.update_layout(title=ttext,
                      paper_bgcolor="#2c2f38",
                      plot_bgcolor='#2c2f38',
                      font=dict(color='#fefefe'),
                      # template="plotly_dark",
                      xaxis_title='Number of convicts',
                      yaxis_title='Age group',
                      legend_title="",
                      legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=-0.3,
                          xanchor="right",
                          x=1
                      )
                      )
    fig.update_traces(showlegend=True)

    return fig


def getBarage(geographicValue, target, states, startPeriod, endPeriod):
    tmp = df[df['target'] == target]

    if geographicValue == 'Department':
        targetgeo = "depto_establecimiento"
        tmp = tmp[tmp['depto_establecimiento'].isin(states)]
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)]  # filter dataset by the daterange
        tmp = tmp[["interno", "edad", "genero", targetgeo]]
    elif geographicValue == 'National':
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)]  # filter dataset by the daterange
        tmp = tmp[["interno", "edad", "genero"]]

    tmp.drop_duplicates(subset="interno", keep='first', inplace=True)
    tmp = tmp.reset_index(drop=True)
    bins = [18, 25, 35, 45, 55, 65, 100]
    labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    tmp['age_range'] = pd.cut(tmp.edad, bins, labels=labels, include_lowest=True)
    # grouped = tmp.groupby(["age_range", "genero", targetgeo])["interno"].count().reset_index().sort_values("age_range")
    grouped = tmp.groupby(["age_range", "genero"])["interno"].count().reset_index().sort_values("age_range")
    fig = barage_Plot(grouped, geographicValue)
    fig.data[0].hovertemplate = '%{label}<br>%{value}'
    fig.data[1].hovertemplate = '%{label}<br>%{value}'
    return fig


#bar plot object
def block_Plot(df, geographicValue):
    if geographicValue == 'Department':
        ttext = f'Top 50 offenses types in the selected {geographicValue}(s)'
    elif geographicValue == 'National':
        ttext = f'Top 50 offenses types in Colombia'

    fig = px.treemap(df, path=['delito'], values='count', color_discrete_sequence = px.colors.sequential.Plotly3)
    fig.data[0].hovertemplate = '%{label}<br>Record Count: %{value}'
    fig.update_layout(title=ttext,
                      # template="plotly_dark",
                      paper_bgcolor="#2c2f38",
                      font=dict(color='#fefefe'),
                      )
    return fig


def getBlock(geographicValue, target, states, startPeriod, endPeriod):
    tmp = df[df['target'] == target]

    if geographicValue == 'Department':
        tmp = tmp[tmp['depto_establecimiento'].isin(states)]

    tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)]  # filter dataset by the daterange
    # tmp = tmp[["interno", "delito", "fecha_ingreso", "regional", targetgeo]].copy()
    grouped = tmp.groupby(["delito"]).size().reset_index(name="count").sort_values(by="count", ascending=False)
    
    if grouped.shape[0] > 50:
        grouped = grouped.iloc[:50]
    else:
        grouped

    fig = block_Plot(grouped, geographicValue)
    return fig

#bar plot object
def barsentence_Plot(df, geographicValue):
    if geographicValue == 'Department':
        ttext = f'Sentence Length Distribution in selected {geographicValue}(s)'
    elif geographicValue == 'National':
        ttext = f'Sentence Length Distribution in Colombia'

    fig = px.bar(df, y="sentence_group", x="interno", orientation='h', color_discrete_sequence = ['#cca9dd'])
    fig.update_layout(title=ttext,
                      paper_bgcolor="#2c2f38",
                      plot_bgcolor='#2c2f38',
                      font=dict(color='#fefefe'),
                      xaxis_title='Number of convicts',
                      yaxis_title='Sentence length (years)',
                      )
    fig.update_traces(showlegend=False)

    return fig


def getBarsentence(geographicValue, target, states, startPeriod, endPeriod):
    tmp = df[df['target'] == target]

    if geographicValue == 'Department':
        targetgeo = "depto_establecimiento"
        tmp = tmp[tmp['depto_establecimiento'].isin(states)]
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)]  # filter dataset by the daterange
        tmp = tmp[["interno", "sentencia", targetgeo]]
    elif geographicValue == 'National':
        tmp = tmp[(tmp['Ingreso_Month'] >= startPeriod) & (tmp['Ingreso_Month'] < endPeriod)]  # filter dataset by the daterange
        tmp = tmp[["interno", "sentencia"]]

    tmp.drop_duplicates(subset="interno", keep='first', inplace=True)
    tmp = tmp.reset_index(drop=True)
    bins = range(0,13)
    labels = range(1, 13, 1)
    tmp['sentence_group'] = pd.cut(tmp.sentencia, bins, labels=labels, include_lowest=True)
    grouped = tmp.groupby(["sentence_group"])["interno"].count().reset_index().sort_values("sentence_group")
    fig = barsentence_Plot(grouped, geographicValue)
    fig.data[0].hovertemplate = '%{label}<br>%{value}'
    return fig

