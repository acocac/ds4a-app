import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate

#data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json
from sqlalchemy import create_engine

###############################################################
#Load and modify the data that will be used in the app.
#################################################################
# engine = create_engine('postgresql://team_60:natesh@nicolasviana.chhlcoydquoi.us-east-2.rds.amazonaws.com/minjusticia')
# df = pd.read_sql(sql='select * from reincidentes left join municipios on reincidentes.ciudad=municipios.municipio', con=engine, parse_dates=['fecha_ingreso'])
#df = pd.read_sql(sql='select * from reincidentes', con=engine, parse_dates=['fecha_ingreso'])
df = pd.read_csv('data/data_full_preprocessed_municipios.csv', parse_dates=['fecha_ingreso']) #if local > faster loading

with open('data/departamentos.geojson') as geo:
    geojson = json.loads(geo.read())

with open('data/states_col.json') as f:
    states_dict = json.loads(f.read())

df['depto_abr'] = df['depto_establecimiento'].map(states_dict)
df['Ingreso_Month'] = pd.to_datetime(df['fecha_ingreso'].map(lambda x: "{}-{}".format(x.year, x.month)))

def register_callbacks(app):

    # callback line plot
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

        ddf1 = ddf.groupby(['interno', 'depto_establecimiento', 'Ingreso_Month']).count().reset_index()
        ddf1 = ddf1.groupby(['depto_establecimiento', 'Ingreso_Month']).count()
        ddf1 = ddf1.reset_index()

        Line_fig = px.line(ddf1, x="Ingreso_Month", y="interno", color="depto_establecimiento")
        Line_fig.update_layout(title='Monthly Convicts in selected departments', paper_bgcolor="#F8F9F9")

        return [Line_fig]

    # callback bar plot
    @app.callback(
        [Output("Bar1", "figure")],
        [
            Input("state_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ],
    )

    def make_bar_plot(state_dropdown, start_date, end_date):
        ddf = df[df['depto_abr'].isin(state_dropdown)]
        ddf = ddf[(ddf['fecha_ingreso'] >= start_date) & (ddf['fecha_ingreso'] < end_date)]

        demo_df = ddf[["interno", "edad", "genero", "depto_establecimiento"]].copy()
        demo_df.drop_duplicates(subset="interno", keep='first', inplace=True)
        demo_df = demo_df.reset_index(drop=True)
        bins = [18, 25, 35, 45, 55, 65, 100]
        labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
        demo_df['age_range'] = pd.cut(demo_df.edad, bins, labels=labels, include_lowest=True)
        gb_df = demo_df.groupby(["age_range", "genero", "depto_establecimiento"])[
            "interno"].count().reset_index().sort_values("age_range")
        Bar_fig = px.bar(gb_df, y="age_range", x="interno", color='genero', orientation='h')
        Bar_fig.update_layout(title='Demographics Distribution', paper_bgcolor="#F8F9F9")

        return [Bar_fig]

    # callback map deparments
    @app.callback(
        Output("COL_map", "figure"),
        [
            # Input("geographic_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ],
    )
    def update_map(start_date, end_date):
        dff = df[(df['Ingreso_Month'] >= start_date) & (df['Ingreso_Month'] < end_date)] # filter dataset by the daterange
        dff = dff.groupby(['interno', 'depto_abr']).count().reset_index() #count unique convict ID
        dff = dff.groupby(['depto_abr']).count().reset_index()

        fig_map2 = px.choropleth_mapbox(dff,
            locations='depto_abr',
            color='interno',
            geojson=geojson,
            featureidkey="properties.depto_abr",
            color_continuous_scale="Viridis",
            opacity=0.5,
            title='Colombia Convicts'
            )

        fig_map2.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=4,
            mapbox_center={"lat": 4.570868, "lon": -74.2973328})

        fig_map2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return fig_map2

    # callback map municipios
    @app.callback(
        Output("COL_adm1_map", "figure"),
        [
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ],
    )

    def update_map_municipio(start_date, end_date):
        dff = df[(df['Ingreso_Month'] >= start_date) & (
                df['Ingreso_Month'] < end_date)]  # filter dataset by the daterange

        dff_municipios = dff.groupby(['interno', 'municipio']).count().reset_index()  # count unique convict ID
        dff_municipios = dff_municipios.groupby(['municipio']).count().reset_index()

        municipio_geo = df[['municipio', 'x', 'y']]
        municipio_geo.drop_duplicates(inplace=True)

        municipio_x = municipio_x.set_index('municipio')['x'].to_dict()
        municipio_y = municipio_x.set_index('municipio')['y'].to_dict()

        dff_municipios['x'] = dff_municipios["municipio"].map(municipio_x)
        dff_municipios['y'] = dff_municipios["municipio"].map(municipio_y)

        Map_municipios2 = px.scatter_mapbox(
            dff_municipios,
            lat="y",
            lon="x",
            # color="confirmed",
            size="interno",
            size_max=50,
            hover_name="municipio",
            hover_data=["interno"],
            # color_continuous_scale=color_scale,
        )

        Map_municipios2.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=4,
            mapbox_center={"lat": 4.570868, "lon": -74.2973328})

        Map_municipios2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return Map_municipios2

    #callback map interaction
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