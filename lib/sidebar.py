# import data related libraries
import json
from datetime import datetime as dt

# import dash related libraries
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from controls import GEOGRAPHIC, POPULATION

with open('data/departamentos_col.json') as f:
    DEPTOS = json.loads(f.read())

with open('data/departamentos_col.json') as f:
    MUNIP = json.loads(f.read())

geographic_options = [
    {"label": str(GEOGRAPHIC[geo]), "value": str(geo)} for geo in GEOGRAPHIC
]

deparmentos_options = [
    {"label": key, "value": DEPTOS[key]} for key in DEPTOS.keys()
]

municipios_options = [
    {"label": key, "value": MUNIP[key]} for key in MUNIP.keys()
]

population_options = [
    {"label": str(POPULATION[pop]), "value": str(pop)} for pop in POPULATION
]

# logo
DS4A_Img = html.Div(
    children=[
        html.Img(
            src="assets/ds4a-img.svg",
            id="ds4a-image",
            style={
                "height": "auto",
                "width": "auto",
                # "margin-bottom": "10px",
            }
        )
    ],
)

##filters exploratory
dropdown = dcc.Dropdown(
    id="state_dropdown",
    options=deparmentos_options,
    value=["BOG", 'BOY'],
    multi=True,
    style={'color': '#242426', 'background-color': '#bfbfbf'}
)

date_picker = dcc.DatePickerRange(
    id='date_picker',
    min_date_allowed=dt(2010, 1, 2),
    max_date_allowed=dt(2020, 5, 31),
    start_date=dt(2010, 1, 1).date(),
    end_date=dt(2020, 1, 1).date(),
    style={'color': '#242426', 'background-color': '#bfbfbf'}
)

geography = dcc.Dropdown(
    id="geographic_dropdown",
    options=geographic_options,
    multi=False,
    value=GEOGRAPHIC['Department'],
    clearable=False,
    style={'color': '#242426', 'background-color': '#bfbfbf'}
)

checklist_r = dbc.Select(
    id="target_dropdown",
    options=population_options,
    value=POPULATION['Recidivist'],
    style={'color': '#242426', 'background-color': '#bfbfbf'},
)

sidebar = html.Div(
    [
        html.Div(children=
        [
            html.Div([DS4A_Img])
        ]),
        html.Div([
            html.Br(),
            html.H5("Target population", style={'color': '#fefefe'}),
            checklist_r,
            html.Hr(),
            html.H5("Select dates", style={'color': '#fefefe'}),
            date_picker,
            html.Br(),
            html.Hr(),
            html.H5("Geographic level", style={'color': '#fefefe'}),
            geography,
            html.Br(),
            html.H5("Select", style={'color': '#fefefe'}),
            dropdown,
        ],
            className='sidebar-menu'
        )
    ], className='ds4a-sidebar'
)