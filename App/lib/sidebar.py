# import data related libraries
import json

# import dash related libraries
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# import local libraries
from controls import GEOGRAPHIC, POPULATION

with open('data/departamentos_col.json') as f:
    DEPTOS = json.loads(f.read())

population_options = [
    {"label": str(POPULATION[pop]), "value": str(pop)} for pop in POPULATION
]

geographic_options = [
    {"label": str(GEOGRAPHIC[geo]), "value": str(geo)} for geo in GEOGRAPHIC
]

deparmentos_options = [
    {"label": key, "value": key} for key in DEPTOS.keys()
]

# logo
logo_img = html.Div(
    children=[
        html.Img(
            src="assets/logo1.svg",
            style={
                "height": "auto",
                "width": "auto",
            }
        )
    ],
)


# filters exploratory
def target():
    return dbc.Select(
        id="target_dropdown",
        options=population_options,
        value=POPULATION['Recidivist'],
        style={'color': '#242426', 'background-color': '#bfbfbf'},
    )


def year_slider():
    return dcc.RangeSlider(
        id="year-slider",
        min=10,
        max=20,
        value=[10, 20],
        className="dcc_control",
    )


def month_slider():
    return dcc.RangeSlider(
        id="month-slider",
        min=1,
        max=12,
        value=[1, 11],
        className="dcc_control",
    )


def dates_slider():
    return html.Div(
        [
            # Year Slider
            html.P("Filter by year:", className="slider_title"),
            html.Div(id='year_range'),
            year_slider(),
            # Month Slider
            html.P("Filter by month:", className="slider_title"),
            html.Div(id='month_range'),
            month_slider(),
        ]
    )


def geography():
    return dbc.Select(
        id="geographic_dropdown",
        options=geographic_options,
        value=GEOGRAPHIC['Department'],
        style={'color': '#242426', 'background-color': '#bfbfbf'},
    )


def dropdown_depto():
    return dcc.Dropdown(
        id="state_dropdown",
        options=deparmentos_options,
        value=["BOGOTA D.C.", "ANTIOQUIA"],
        multi=True,
        style={'color': '#242426', 'background-color': '#bfbfbf'}
    )


def characterization():
    return html.Div(
        [
            html.Div(children=
            [
                html.Div([logo_img])
            ]),
            html.Div([
                html.Br(),
                html.H5("Target population", style={'color': '#fefefe'}),
                target(),
                html.Hr(),
                html.H5("Select dates", style={'color': '#fefefe'}),
                dates_slider(),
                html.H5("Geographic level", style={'color': '#fefefe'}),
                geography(),
                html.Br(),
                html.Br(),
                html.H5("Select", style={'color': '#fefefe'}),
                dropdown_depto(),
            ],
                className='sidebar-menu-exploratory'
            ),
        ], className='sidebar-exploratory'
    )


# filters cluster
clusters_options = [
    {'label': 'CLUSTER {}'.format(d), 'value': d} for d in range(12)
]


def dropdown_network():
    return dcc.Dropdown(
        id='cluster_dropdown',
        options=clusters_options,
        value=4,
        multi=False,
        clearable=False,
        style={'color': '#242426', 'background-color': '#bfbfbf'},
    )


def network():
    return html.Div(
        [
            html.Div(children=
            [
                html.Div([logo_img])
            ]),
            html.Div([
                html.Br(),
                html.H5("Cluster", style={'color': '#fefefe'}),
                dropdown_network(),
                html.Br(),
                html.Hr(),
                html.H5("Interpretation", style={'color': '#fefefe'}),
                html.Div([html.Label(
                    "Each network describes a group of similar crimes where each point represents a crime, and the points it is connected to represent the crimes that have the highest probability of being committed by a recidivist after his/her release")
                ], className='control_label')
            ],
                className='sidebar-menu-network'
            )
        ], className='sidebar-network'
    )


# filters prediction
def age_input():
    return dcc.Slider(id='edad-slider', min=18, max=100, step=1, value=30)


def gender_input():
    return dcc.Slider(id='genero-slider', min=0, max=1, step=1, value=1)


def sentence_input():
    return html.Div([
        dcc.Slider(id='sentencia-slider', min=0, max=50, step=1, value=5)
    ], style={'marginBottom': '0em'})


def study_input():
    return html.Div([
        dcc.Slider(id='estudio-slider', min=0, max=1, step=1, value=0)
    ], style={'marginBottom': '0em'})


def education_input():
    return html.Div([
        dcc.Slider(id='educativo-slider', min=0, max=11, step=1, value=4)
    ], style={'marginBottom': '0em'})


def work_input():
    return html.Div([
        dcc.Slider(id='trabajo-slider', min=0, max=1, step=1, value=1)
    ], style={'marginBottom': '0em'})


def intramuros_input():
    return html.Div([
        dcc.Slider(id='intramuros-slider', min=0, max=1, step=1, value=1)
    ], style={'marginBottom': '0em'})


def crimes_input():
    return html.Div([
        dcc.Slider(id='delitos-slider', min=0, max=20, step=1, value=3)
    ], style={'marginBottom': '0em'})


def calificado_input():
    return html.Div([
        dcc.Slider(id='calificado-slider', min=0, max=1, step=1, value=1)
    ], style={'marginBottom': '0em'})


def agravado_input():
    return html.Div([
        dcc.Slider(id='agravado-slider', min=0, max=1, step=1, value=1)
    ], style={'marginBottom': '0em'})


def cluster1_input():
    return html.Div([
        dcc.Slider(id='cluster1-slider', min=0, max=1, step=1, value=0)
    ], style={'marginBottom': '0em'})


def cluster4_input():
    return html.Div([
        dcc.Slider(id='cluster4-slider', min=0, max=1, step=1, value=1)
    ], style={'marginBottom': '0em'})


def cluster5_input():
    return html.Div([
        dcc.Slider(id='cluster5-slider', min=0, max=1, step=1, value=0)
    ], style={'marginBottom': '0em'})


predictors_slider = html.Div([
    html.Label(id='edad-range'),
    age_input(),
    html.Label(id='genero-range'),
    gender_input(),
    html.Label(id='sentencia-range'),
    sentence_input(),
    html.Label(id='estudio-range'),
    study_input(),
    html.Label(id='education-range'),
    education_input(),
    html.Label(id='trabajo-range'),
    work_input(),
    html.Label(id='intramuros-range'),
    intramuros_input(),
    html.Label(id='delitos-range'),
    crimes_input(),
    html.Label(id='calificado-range'),
    calificado_input(),
    html.Label(id='agravado-range'),
    agravado_input(),
    html.Label(id='cluster1-range'),
    cluster1_input(),
    html.Label(id='cluster4-range'),
    cluster4_input(),
    html.Label(id='cluster5-range'),
    cluster5_input()
],
    className='sliders-prediction',
)


def prediction():
    return html.Div(
        [
            html.Div(children=
            [
                html.Div([logo_img])
            ]),
            html.Br(),
            html.Div([
                html.Div([
                    html.Button('Predict', id='buttonPredict', className='btn btn-primary')
                ]),
                html.Br(),
                html.H5("Set Predictors", style={'color': '#fefefe'}),
                predictors_slider,
                html.Br(),
            ],
                className='sidebar-menu-prediction'
            ),
        ], className='sidebar-prediction'
    )
