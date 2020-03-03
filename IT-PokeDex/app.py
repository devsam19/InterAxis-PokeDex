import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
import random
import csv
import json
import os

#Style Sheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
FONT_FAMILY =  "Arial"

app = dash.Dash(__name__ , external_stylesheets = external_stylesheets)
cssURL = "https://rawgit.com/richard-muir/uk-car-accidents/master/road-safety.css"
app.css.append_css({
    "external_url": cssURL
})
#Read CSV
#df = pd.read_csv('pokemon/pokemon_alopez247.csv')

# App Layout
app.layout = html.Div(children=[
    html.H1(children="PokeDex", style={
        'paddingLeft': '14em',
        'fontFamily': FONT_FAMILY
    }),

    html.Div(children = [
        html.Div(
            html.H3('Left Div'),
            style = {
                "height": 550,
                "width": '25%',
                "float" : 'left',
                "background-color":"white",
                "border":"solid black"

            }
        ),
        html.Div(
            html.H3('Middle Div'),
            style = {
                "height": 400,
                "width": '50%',
                "float" : 'left',
                "background-color":"white",
                "border":"solid black"


            }
        ),
        html.Div(
            html.H3('Right Div'),
            style = {
                "height": 550,
                "width": '20%',
                "float" : 'left',
                "background-color":"white",
                "border":"solid black"


            }
        ),


    ],
    style = {
            "width":"100%",
            "height":"600px",
            "background-color":"#CFD8DC",
            "padding-top":"20px",
            "padding-left":"15px",
            "padding-right":"15px"
    })

])

if __name__ == '__main__':
    app.run_server(debug=True)
