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
            # id="ds4a-image",
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

def characterization():
    return html.Div(
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
            className='sidebar-menu-exploratory'
        )
    ], className='sidebar-exploratory'
)


##filters cluster
clusters_options = [
    {'label': 'CLUSTER {}'.format(d), 'value': d} for d in range(12)
]

dropdown_network = dcc.Dropdown(
    id="cluster_dropdown",
    options=clusters_options,
    value=4,
    multi=False,
    style={'color': '#242426', 'background-color': '#bfbfbf'}
)

def network():
    return html.Div(
    [
        html.Div(children=
        [
            html.Div([DS4A_Img])
        ]),
        html.Div([
            html.Br(),
            html.H5("Cluster", style={'color': '#fefefe'}),
            dropdown_network,
        ],
            className='sidebar-menu-network'
        )
    ], className='sidebar-network'
)


##filters prediction
age_input = dcc.Input(id='edad-input', type='number', min=18, max=100, step=1, value=30)
gender_input = dcc.Input(id='genero-input', type='number', min=0, max=1, step=1, value=1)
sentence_input = dcc.Input(id='sentencia-input', type='number', min=0, max=50, step=1, value=5)
study_input = dcc.Input(id='estudio-input', type='number', min=0, max=1, step=1, value=0)
education_input = dcc.Input(id='educativo-input', type='number', min=0, max=11, step=1, value=4)
work_input = dcc.Input(id='trabajo-input', type='number', min=0, max=1, step=1, value=1)
intramuros_input = dcc.Input(id='intramuros-input', type='number', min=0, max=1, step=1, value=1)
crimes_input = dcc.Input(id='delitos-input', type='number', min=0, max=20, step=1, value=3)
calificado_input = dcc.Input(id='calificado-input', type='number', min=0, max=1, step=1, value=1)
agravado_input = dcc.Input(id='agravado-input', type='number', min=0, max=1, step=1, value=1)
cluster1_input = dcc.Input(id='cluster1-input', type='number', min=0, max=1, step=1, value=0)
cluster4_input = dcc.Input(id='cluster4-input', type='number', min=0, max=1, step=1, value=1)
cluster5_input = dcc.Input(id='cluster5-input', type='number', min=0, max=1, step=1, value=0)

def prediction():
    return html.Div(
    [
        html.Div(children=
        [
            html.Div([DS4A_Img])
        ]),
        html.Div([
            html.Br(),
            html.H5("Predict Recidivism", style={'color': '#fefefe'}),
            html.Div(children=[
                html.Div([
                    # html.P("Age", className="control_label"),
                    html.Abbr("Age", title="[min:18, max:100]", className="control_label"),
                    age_input,
                ], className="flex-display",
                ),
                # html.Br(),
                html.Div([
                    # html.P("Gender", className="control_label"),
                    html.Abbr("Gender", title="[min:0, max:1]", className="control_label"),
                    gender_input,
                ], className="flex-display",
                ),
                # html.Br(),
                html.Div([
                    # html.P("Sentence", className="control_label"),
                    html.Abbr("Sentence", title="[min:0, max:50]", className="control_label"),
                    sentence_input,
                ], className="flex-display",
                ),
                # html.Br(),
                html.Div([
                    # html.P("Study activities", className="control_label"),
                    html.Abbr("Study activities", title="[min:0, max:1]", className="control_label"),
                    study_input,
                ], className="flex-display",
                ),
                html.Div([
                    # html.P("Education Level", className="control_label"),
                    html.Abbr("Education Level", title="[min:0, max:11]", className="control_label"),
                    education_input,
                ], className="flex-display",
                ),
                # html.Br(),
                html.Div([
                    # html.P("Work Activities", className="control_label"),
                    html.Abbr("Work Activities", title="[min:0, max:1]", className="control_label"),
                    work_input,
                ], className="flex-display",
                ),
                # html.Br(),
                html.Div([
                    # html.P("Intramuros state", className="control_label"),
                    html.Abbr("Intramuros state", title="[min:0, max:1]", className="control_label"),
                    intramuros_input,
                ], className="flex-display",
                ),
                # html.Br(),
                html.Div([
                    # html.P("Crimes count", className="control_label"),
                    html.Abbr("Crimes count", title="[min:0, max:20]", className="control_label"),
                    crimes_input,
                ], className="flex-display",
                ),
                # html.Br(),
                html.Div([
                    # html.P("Crime(s) Calificado", className="control_label"),
                    html.Abbr("Crime(s) Calificado", title="[min:0, max:1]", className="control_label"),
                    calificado_input,
                ], className="flex-display",
                ),
                # html.Br(),
                html.Div([
                    # html.P("Crime(s) Agravado:", className="control_label"),
                    html.Abbr("Crime(s) Agravado", title="[min:0, max:1]", className="control_label"),
                    agravado_input,
                ], className="flex-display",
                ),
                # html.Br(),
                html.Div([
                    # html.P("Belongs to crime group 1", className="control_label"),
                    html.Abbr("Belongs to crime group 1", title="[min:0, max:1]", className="control_label"),
                    cluster1_input,
                ], className="flex-display",
                ),
                # html.Br(),
                html.Div([
                    # html.P("Belongs to crime group 4", className="control_label"),
                    html.Abbr("Belongs to crime group 4", title="[min:0, max:1]", className="control_label"),
                    cluster4_input,
                ], className="flex-display",
                ),
                # html.Br(),
                html.Div([
                    # html.P("Belongs to crime group 5", className="control_label"),
                    html.Abbr("Belongs to crime group 5", title="[min:0, max:1]", className="control_label"),
                    cluster5_input,
                ], className="flex-display",
                ),
                html.Div([
                    html.Button('Predict', id='buttonPredict', className='btn btn-primary')
                ], className='mx-auto', style={'paddingTop': '20px', 'paddingBottom': '20px'})
            ], className='row'),
            ],
            className='sidebar-menu-prediction',
        )
    ], className='sidebar-prediction'
)