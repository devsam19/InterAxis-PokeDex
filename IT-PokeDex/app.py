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
import math

from sklearn.preprocessing import MinMaxScaler

#Style Sheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
FONT_FAMILY =  "Arial"

app = dash.Dash(__name__ , external_stylesheets = external_stylesheets)
cssURL = "https://rawgit.com/richard-muir/uk-car-accidents/master/road-safety.css"
app.css.append_css({
    "external_url": cssURL
})
#Read CSV
df = pd.read_csv('data/pokemon_alopez247.csv')

#Get names of all the attributes to populate the dropdown for both axes
axes_list = []
for col in df.columns:
    axes_list.append(col)

#Default axes

# App Layout
app.layout = html.Div(children=[
    html.H1(children="PokeDex", style={
        'paddingLeft': '14em',
        'fontFamily': FONT_FAMILY
    }),

    html.Div(children = [
        html.Div(
            #html.H3('Left Div'),
            children=[
                html.Div([
                    dcc.Dropdown(
                        id = 'xaxis-dropdown',
                        options = [
                            {'label': i, 'value': i} for i in axes_list
                        ],
                        value="Attack"
                    )
                ]),
                html.Div([
                    dcc.Dropdown(
                        id = 'yaxis-dropdown',
                        options = [
                            {'label': i, 'value': i} for i in axes_list
                        ],
                        value="Catch_Rate"
                    )
                ])
            ],
            style = {
                "height": 550,
                "width": '25%',
                "float" : 'left',


            }
        ),
        html.Div(
            #html.H3('Middle Div'),
            children=[
                html.Div(
                    id='scatter-plot',
                    style={

                        'width': '33%',
                        'display': 'inline-block',
                        'boxSizing': 'border-box',
                        'fontFamily': "Arial",
                        'float': 'left',
                        "height": "20em"

                    }
                ),


            ],
            style = {
                "height": 550,
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

@app.callback(
    Output(component_id='scatter-plot', component_property='children'),
    [Input(component_id='xaxis-dropdown', component_property='value'),
    Input(component_id='yaxis-dropdown', component_property='value')]
)

def updateScatterPlot(xAxis, yAxis):

    #Get DF
    print(xAxis)
    x_list = df[xAxis].values.tolist()
    y_list = df[yAxis].values.tolist()


    print(df.head())

    print(len(x_list),len(y_list))
    #Get Max and Min values for axes and normalize the points
    denum = math.sqrt(sum((i**2) for i in x_list))
    for index in range(len(x_list)):
        x_list[index] = x_list[index]/denum

    print(x_list)

    denum = math.sqrt(sum((i ** 2) for i in y_list))
    for index in range(len(y_list)):
        y_list[index] = y_list[index]/denum
        
    #Create graph and return
    return dcc.Graph(
        id='scatterPokemonGraph',
        figure={
            'data': [
                {'x': x_list, 'y': y_list,
                 'mode': 'markers',
                 'marker': {
                     'color': '#0277bd',
                     'size': 15,
                     'opacity': 0.5,
                     'line': {'width': 0.5, 'color': 'white'}
                 }
                 }
            ],
            'layout': {
                'title': 'Scatter Plot',
                'hovermode': 'closest',
                'paper_bgcolor': '#e1f5fe',
                'plot_bgcolor': '#e1f5fe',
                'height': 500,
                'width' : "75%"

            },

        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
