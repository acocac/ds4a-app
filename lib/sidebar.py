#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
from controls import GEOGRAPHIC, POPULATION

#Dash Bootstrap Components
import dash_bootstrap_components as dbc

#data
import json
from datetime import datetime as dt

#Recall app
#from app import app

geographic_options = [
    {"label": str(GEOGRAPHIC[geo]), "value": str(geo)} for geo in GEOGRAPHIC
]

population_options = [
    {"label": str(POPULATION[pop]), "value": str(pop)} for pop in POPULATION
]

#############################################################################
# State Dropdown
#############################################################################
with open('data/states_col.json') as f:
    states = json.loads(f.read())

dropdown=dcc.Dropdown(
        id="state_dropdown",
        options=[{"label":key, "value":states[key]} for key in states.keys()],
        value=["BOG",'BOY'],
        multi=True
        )

##############################################################################
# Date Picker 
##############################################################################

date_picker=dcc.DatePickerRange(
                id='date_picker',
                min_date_allowed=dt(2010, 1, 2),
                max_date_allowed=dt(2020, 5, 31),
                start_date=dt(2010,1,1).date(),
                end_date=dt(2020, 1, 1).date()
            )

##############################################################################
# Geography
##############################################################################

geography = dcc.Dropdown(
                id="geographic_dropdown",
                options=geographic_options,
                multi=False,
                value=GEOGRAPHIC['Department'],
                clearable=False
            )

#############################################################################
# Recidivism Checklist
#############################################################################
checklist_r=dcc.RadioItems(
            id="checklist",
            options=population_options,
            value=POPULATION['Recidivist']
            )

#############################################################################
# Sidebar Layout
#############################################################################
sidebar = html.Div(
    [   #Add the DS4A_Img located in the assets folder
        html.Hr(), #Add an horizontal line
        ####################################################
        #Place the rest of Layout here
        ####################################################
        html.H5("Target population"),
        checklist_r,
        html.H5("Select dates"),
        date_picker,
        html.Br(),
        html.Hr(),
        html.H5("Geographic level"),
        geography,
        html.Br(),
        html.H5("Select"),
        dropdown,
    ],className='ds4a-sidebar'

)