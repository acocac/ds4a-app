# import dash related libraries
import dash_html_components as html
import dash_bootstrap_components as dbc


#title
title=html.Div(className="ds4a-title",
	children=[
        dbc.Row(
            dbc.Col(
                html.H1("Recidivism in Colombia", style={'color': '#fefefe'}),
                width={"size": 10, "offset": 3}
            )
        )],
	id="title")