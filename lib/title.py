#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html


#Dash Bootstrap Components
import dash_bootstrap_components as dbc 

#Recall app
from app import app

####################################################################################
# Add the DS4A_Img
####################################################################################

DS4A_Img = html.Div(
            children=[
                html.Img(
                    src=app.get_asset_url("ds4a-img.svg"),
                    id="ds4a-image",
                    style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                    },
                )
            ],
        )

title=html.Div(className="ds4a-title",
	children=[
        dbc.Row(
            dbc.Col(
                html.H1("MinJusticia Dashboard"),
                width={"size": 6, "offset": 3}
            )
        )],
	id="title")
