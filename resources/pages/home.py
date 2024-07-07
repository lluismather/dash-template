import dash
import dash_bootstrap_components as dbc
from dash import dcc, html


def title():
    return "Home | Dash"


dash.register_page(__name__, title=title(), path="/")


def layout():
    return dbc.Container(
        [
            html.H1("Home"),
            html.P("Welcome to the home page."),
            html.Div(id="output"),
            dcc.Input(id="input", type="text", placeholder="Enter text"),
        ]
    )
