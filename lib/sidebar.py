#import data related libraries
import json
from datetime import datetime as dt

#import dash related libraries
import dash_core_components as dcc
import dash_html_components as html
from controls import GEOGRAPHIC, POPULATION

with open('data/departamentos_col.json') as f:
    DEPTOS = json.loads(f.read())

with open('data/departamentos_col.json') as f:
    MUNIP = json.loads(f.read())

geographic_options = [
    {"label": str(GEOGRAPHIC[geo]), "value": str(geo)} for geo in GEOGRAPHIC
]

deparmentos_options = [
    {"label":key, "value":DEPTOS[key]} for key in DEPTOS.keys()
]

municipios_options = [
    {"label":key, "value":MUNIP[key]} for key in MUNIP.keys()
]

population_options = [
    {"label": str(POPULATION[pop]), "value": str(pop)} for pop in POPULATION
]

#############################################################################
# Departamentos Dropdown
#############################################################################

dropdown=dcc.Dropdown(
        id="state_dropdown",
        options=deparmentos_options,
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