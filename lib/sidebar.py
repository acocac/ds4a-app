#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html


#Dash Bootstrap Components
import dash_bootstrap_components as dbc 

#data
import json
from datetime import datetime as dt


#Recall app
from app import app


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
                end_date=dt(2016, 1, 1).date()
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
        html.H5("Select dates"),
        date_picker,
        html.Hr(),
        html.H5("Select states"),
        dropdown,
        html.Hr(),



    ],className='ds4a-sidebar'

)