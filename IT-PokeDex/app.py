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
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, scale
from dash.exceptions import PreventUpdate
from sklearn.preprocessing import MinMaxScaler
from collections import defaultdict
from sklearn import preprocessing


#Style Sheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
FONT_FAMILY =  "Arial"

app = dash.Dash(__name__ , external_stylesheets = external_stylesheets)
cssURL = "https://rawgit.com/richard-muir/uk-car-accidents/master/road-safety.css"
app.css.append_css({
    "external_url": cssURL
})
#Read CSV
df1 = pd.read_csv('data/pokemon_alopez247.csv')

#Get names of all the attributes to populate the dropdown for both axes
axes_list = ['Total', 'HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed', 'Height_m', 'Weight_kg', 'Catch_Rate']
# for col in df.columns:
#     axes_list.append(col)

df = df1[axes_list]

df_scaled_prev = df[axes_list]
#print("rrrrrr", df_scaled_prev)

df_scaled_mid = StandardScaler().fit_transform(df_scaled_prev)
df_scaled = pd.DataFrame(df_scaled_mid, columns = df_scaled_prev.columns)
#print("eeeeee", df_scaled)
#print(df)
#Default axes

def is_any_non_zero(list_of_values):
    for i in list_of_values:
        if i is not 0:
            return True
    return False

# App Layout
app.layout = html.Div(children=[
    html.H1(children="PokeDex", style={
        'paddingLeft': '14em',
        'fontFamily': FONT_FAMILY
    }),

    # The memory store reverts to the default on every page refresh


    html.Div(children = [
        html.Div(
            #html.H3('Left Div'),
            children=[
                html.Div([

                    html.H2("X-Attributes"),
                    html.P("Total"),
                    dcc.Slider(
                        id='slider-Totalx',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },

                    ),

                    html.Br(),
                    html.P("HP"),
                    dcc.Slider(
                        id='slider-HPx',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.P("Attack"),
                    dcc.Slider(
                        id='slider-Attackx',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.P("Defense"),
                    dcc.Slider(
                        id='slider-Defencex',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.P("Special-Attack"),
                    dcc.Slider(
                        id='slider-spAttackx',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.P("Special-Defense"),
                    dcc.Slider(
                        id='slider-spDefencex',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.P("Speed"),
                    dcc.Slider(
                        id='slider-Speedx',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.P("Height"),
                    dcc.Slider(
                        id='slider-Heightx',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.P("Weight"),
                    dcc.Slider(
                        id='slider-Weightx',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.P("Catch Rate"),
                    dcc.Slider(
                        id='slider-CatchRatex',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.H2("Y-Attributes"),
                    html.P("Total"),
                    dcc.Slider(
                            id='slider-Total',
                            min=-1,
                            max=1,
                            step=0.1,
                            value=0,
                            marks={
                                    -1: '-1',
                                    -0.5 : '-0.5',
                                    0: '0',
                                    0.5 : '0.5',
                                    1: '1',
                                },
                        ),
                    html.Br(),
                    html.P("HP"),
                    dcc.Slider(
                            id='slider-HP',
                            min=-1,
                            max=1,
                            step=0.1,
                            value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                        ),
                    html.Br(),
                    html.P("Attack"),
                    dcc.Slider(
                            id='slider-Attack',
                            min=-1,
                            max=1,
                            step=0.1,
                            value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                        ),
                    html.Br(),
                    html.P("Defense"),
                    dcc.Slider(
                            id='slider-Defence',
                            min=-1,
                            max=1,
                            step=0.1,
                            value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                        ),
                    html.Br(),
                    html.P("Special-Attack"),
                    dcc.Slider(
                            id='slider-spAttack',
                            min=-1,
                            max=1,
                            step=0.1,
                            value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                        ),
                    html.Br(),
                    html.P("Special-Defense"),
                    dcc.Slider(
                            id='slider-spDefence',
                            min=-1,
                            max=1,
                            step=0.1,
                            value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                        ),
                    html.Br(),
                    html.P("Speed"),
                    dcc.Slider(
                        id='slider-Speed',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.P("Height"),
                    dcc.Slider(
                        id='slider-Height',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.P("Weight"),
                    dcc.Slider(
                        id='slider-Weight',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),
                    html.Br(),
                    html.P("Catch Rate"),
                    dcc.Slider(
                        id='slider-CatchRate',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=0,
                        marks={
                            -1: '-1',
                            -0.5: '-0.5',
                            0: '0',
                            0.5: '0.5',
                            1: '1',
                        },
                    ),


                ]),

            ],
            style = {
                "height": 550,
                "width": '25%',
                "float" : 'left',
                "overflow" : "scroll",
                "padding-left" : "5px"
            }
        ),
        html.Div(
            #html.H3('Middle Div'),
            children=[
                html.Div([
                    dcc.Graph(
                        id='scatter-plot',
                    ),
                html.Div([
                    #html.Br(),
                    #html.P("Select X-Axis "),
                    dcc.Dropdown(
                        id = 'xaxis-dropdown',
                        options = [
                            {'label': i, 'value': i} for i in axes_list
                        ],
                        placeholder="Select X Axis",
                        style = {"bottom" : "100%", },

                        value="Attack"
                    ),
                    #html.Br(),
                    #html.P("Select Y-Axis "),

                ],
                    style={ "float" : "left", "display" : "inline-block", "width" : "40%" , "padding-right" : "5px",
                            "padding-top" : "5px"

                    }
                    
                ),

                html.Div([
                        dcc.Dropdown(
                        id = 'yaxis-dropdown',
                        options = [
                            {'label': i, 'value': i} for i in axes_list
                        ],
                        placeholder="Select Y Axis",
                        #style={ "display" : "inline-block"}
                        value="Catch_Rate"
                    )
                ],
                    style={"float": "right", "display": "inline-block", "width": "40%", "padding-top" : "5px"},
                )
                ],

                    style={

                        #'width': '33%',
                        'display': 'inline-block',
                        'boxSizing': 'border-box',
                        'fontFamily': "Arial",
                        'float': 'left',
                        "height": "20em",
                        "padding-left": "5px"

                    }
                ),
            ],
            style = {
                "height": 600,
                "width": '50%',
                "float" : 'left',
                "background-color":"white",
                "border":"solid black",
                "margin-left": "12px"
            }
        ),
        html.Div(children = [
            html.Div([
            html.H3('Pokemon Information'),
            html.Pre(id='click-data'),
        ],
            style = {
                "height": 445,
                "width": '20%',
                "float" : 'left',
                "background-color":"white",
                "border":"solid black"
            }

        ),

        html.Div([
            #html.H4('Click here'),

            dcc.ConfirmDialogProvider(children= html.Button('X -ve', id='xnbutton', style = {
                "z-index": "0",
                "margin-top" : "15px",
                "margin" : "1px",
                "outline": "0",
                "background": "#03A9F4",
                "width": "49%",
                "border": "0",
                "padding": "5px",
                "color": "#FFFFFF",
                "font-size": "14px",
                "float" : "left"
            }),
                message="Sent to X -VE"),

            dcc.ConfirmDialogProvider(children= html.Button('X +ve', id='xpbutton', style = {
                "z-index": "0",
                "margin-top" : "15px",
                "margin" : "1px",
                "outline": "0",
                "background": "#03A9F4",
                "width": "49%",
                "border": "0",
                "padding": "5px",
                "color": "#FFFFFF",
                "font-size": "14px",
                "float" : "left"
            }),
                message= "Sent to X +VE"),

            dcc.ConfirmDialogProvider(children=html.Button('Y -ve', id='ynbutton', style = {
                "z-index": "0",
                "margin" : "1px",
                "outline": "0",
                "background": "#03A9F4",
                "width": "49%",
                "border": "0",
                "padding": "5px",
                "color": "#FFFFFF",
                "font-size": "14px",
                "float" : "left"
            }),
                message="Sent to Y -VE"),

            dcc.ConfirmDialogProvider(children=html.Button('Y +ve', id='ypbutton', style = {
                "z-index": "0",
                "margin" : "1px",
                "outline": "0",
                "background": "#03A9F4",
                "width": "49%",
                "border": "0",
                "padding": "5px",
                "color": "#FFFFFF",
                "font-size": "14px",
                "float" : "left"
            }),
                message="Sent to Y +VE"),

            html.Button('Transform', id='transform', style = {
                "z-index": "0",
                "margin-top" : "15px",
                "margin" : "1px",
                "outline": "0",
                "background": "#4CAF50",
                "width": "100%",
                "border": "0",
                "padding": "5px",
                "color": "#FFFFFF",
                "font-size": "14px"
            }),


            html.Div(id='output3',
             children='Enter a value and press submit'),
            html.Div(id='output2',
             children='Enter a value and press submit'),
            html.Div(id='output1',
             children='Enter a value and press submit'),
            html.Div(id='output4',
             children='Enter a value and press submit')
        ],
            style = {
                "height": 155,
                "width": '20%',
                "float" : 'left',
                "background-color":"white",
                "border":"solid black"
            }

        ),


        
        ]
            
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


#Add Input to the callback for each slider (y and x) and subseequently add a parameter to the function
#slider values are directly accessible from arguments. Make sure to check range of each slider attribute

@app.callback(
    Output(component_id='scatter-plot', component_property='figure'),
    [Input(component_id='xaxis-dropdown', component_property='value'),
    Input(component_id='yaxis-dropdown', component_property='value'),
    Input('transform', 'n_clicks'),
    Input(component_id='slider-Total', component_property='value'),
    Input(component_id='slider-HP', component_property='value'),
    Input(component_id='slider-Attack', component_property='value'),
    Input(component_id='slider-Defence', component_property='value'),
    Input(component_id='slider-spAttack', component_property='value'),
    Input(component_id='slider-spDefence', component_property='value'),
    Input(component_id='slider-Speed', component_property='value'),
    Input(component_id='slider-Height', component_property='value'),
    Input(component_id='slider-Weight', component_property='value'),
    Input(component_id='slider-CatchRate', component_property='value'),
    Input(component_id='slider-Totalx', component_property='value'),
    Input(component_id='slider-HPx', component_property='value'),
    Input(component_id='slider-Attackx', component_property='value'),
    Input(component_id='slider-Defencex', component_property='value'),
    Input(component_id='slider-spAttackx', component_property='value'),
    Input(component_id='slider-spDefencex', component_property='value'),
    Input(component_id='slider-Speedx', component_property='value'),
    Input(component_id='slider-Heightx', component_property='value'),
    Input(component_id='slider-Weightx', component_property='value'),
    Input(component_id='slider-CatchRatex', component_property='value')
    ]
)

def updateScatterPlot(xAxis, yAxis,n_clicks, yTotal, yHP, yAttack, yDefence, yspAttack, yspDefence, ySpeed, yHeight, yWeight, yCatchRate, 
                                             xTotal, xHP, xAttack, xDefence, xspAttack, xspDefence, xSpeed, xHeight, xWeight, xCatchRate):

    # print("\n"+ str(yAttack )+ "\n"+str( yDefence)+ "\n"+str(yspAttack)+ "\n"+ str(yspDefence)+ "\n"+ str(ySpeed)+ "\n"+ str(yHeight)+ "\n"+ str(yWeight)+ "\n"+str(yCatchRate)+ "\n"+str(xTotal)+ "\n"+ str(xHP)+ "\n"+str(xAttack)+ "\n"+str(xDefence)+ "\n"+str(xspAttack)+ "\n"+str(xspDefence)+ "\n"+str(xSpeed)+ "\n"+str(xHeight)+ "\n"+str(xWeight)+ "\n"+str(xCatchRate))
    list_of_slider_values = [yTotal, yHP, yAttack, yDefence, yspAttack, yspDefence, ySpeed, yHeight, yWeight, yCatchRate, 
                             xTotal, xHP, xAttack, xDefence, xspAttack, xspDefence, xSpeed, xHeight, xWeight, xCatchRate]

    x = df.loc[:, axes_list].values
    y = df1.loc[:,['Name']].values

    #initial scatter plot using PCA
    if not xAxis and not yAxis and not n_clicks and not is_any_non_zero(list_of_slider_values):
        x = StandardScaler().fit_transform(x)
        pca = PCA(n_components=2)
        principalComponents = pca.fit_transform(x)
        principalDf = pd.DataFrame(data = principalComponents, columns = ['principal_component_1', 'principal_component_2'])
        finalDf = pd.concat([principalDf, df1[['Name']]], axis = 1)
        x_list = finalDf['principal_component_1']
        y_list = finalDf['principal_component_2']
    #whenever transform button is pushed
    elif not xAxis and not yAxis and (n_clicks or is_any_non_zero(list_of_slider_values)):
        x_dict_p=defaultdict(int)
        y_dict_p=defaultdict(int)
        x_dict_n=defaultdict(int)
        y_dict_n=defaultdict(int)
        x_transform=defaultdict(int)
        y_transform=defaultdict(int)
        x_list = []
        y_list = []
        #sleep(1)
        if n_clicks:
            with open('x-positive.csv') as csvfile:
                no_of_points_xp = len(csvfile.readlines())
            with open('x-positive.csv') as csvfile:
                test = list(csvfile)
                if no_of_points_xp > 0:
                    
                    for row in test:
                        row = row.split(',')    
                        i=1
                        for col in axes_list:
                            x_dict_p[col] += float(row[i])
                            i+=1
                    for col in axes_list:
                        x_dict_p[col] = x_dict_p[col]/no_of_points_xp
            
            print("sums1 {}".format(x_dict_p))
            
            with open('x-negative.csv') as csvfile:
                no_of_points_xn = len(csvfile.readlines())
            with open('x-negative.csv') as csvfile:
                test = list(csvfile)
                
                if no_of_points_xn > 0:
                    
                    for row in test:
                        row = row.split(',')    
                        i=1
                        for col in axes_list:
                            x_dict_n[col] += float(row[i])
                            i+=1
                    for col in axes_list:
                        x_dict_n[col] = x_dict_n[col]/no_of_points_xn
            print("sums2 {}".format(x_dict_n))

            for col in axes_list:
                x_transform[col] = x_dict_p[col] - x_dict_n[col]
            x_transform_list = []
            for col in axes_list:
                x_transform_list.append(x_transform[col]) 
            #x_transform_list.reshape(-1, 1)
            #x_transform_scaled = StandardScaler().fit_transform(x_transform_list)
            x_transform_list = scale(x_transform_list)
            list_of_x_values = list_of_slider_values[10:]
            if is_any_non_zero(list_of_x_values):
                i=-1
                for x_vals in list_of_x_values:
                    i+=1
                    if x_vals is not 0:
                        x_transform_list[i] = x_vals
                        

            for index,row in df_scaled.iterrows():
                val=0
                i=0
                for col in x_transform:
                    val+=x_transform_list[i]*row[col]
                    i+=1
                x_list.append(val)
            
            #x_list = preprocessing.normalize([x_list]).tolist()
            print("xxxxxxx", x_list)
            #print("ppppppp", type(x_list))


    #=======================================================================

            with open('y-positive.csv') as csvfile:
                no_of_points_yp = len(csvfile.readlines())
            with open('y-positive.csv') as csvfile:
                test = list(csvfile)
                
                if no_of_points_yp > 0:
                    
                    for row in test:
                        row = row.split(',')    
                        i=1
                        for col in axes_list:
                            y_dict_p[col] += float(row[i])
                            i+=1
                    for col in axes_list:
                        y_dict_p[col] = y_dict_p[col]/no_of_points_yp
            
            print("sums1 {}".format(y_dict_p))
            
            with open('y-negative.csv') as csvfile:
                no_of_points_yn = len(csvfile.readlines())
            with open('y-negative.csv') as csvfile:
                test = list(csvfile)
                
                if no_of_points_yn > 0:
                    
                    for row in test:
                        row = row.split(',')    
                        i=1
                        for col in axes_list:
                            y_dict_n[col] += float(row[i])
                            i+=1
                    for col in axes_list:
                        y_dict_n[col] = y_dict_n[col]/no_of_points_yn
            print("sums2 {}".format(y_dict_n))

            for col in axes_list:
                y_transform[col] = y_dict_p[col] - y_dict_n[col]

            y_transform_list = []
            for col in axes_list:
                y_transform_list.append(y_transform[col]) 
            #x_transform_list.reshape(-1, 1)
            #x_transform_scaled = StandardScaler().fit_transform(x_transform_list)
            y_transform_list = scale(y_transform_list)
            list_of_y_values = list_of_slider_values[:10]
            if is_any_non_zero(list_of_y_values):
                i=-1
                for y_vals in list_of_y_values:
                    i+=1
                    if y_vals is not 0:
                        y_transform_list[i] = y_vals

            for index,row in df_scaled.iterrows():
                val=0
                i=0
                for col in y_transform:
                    val+=y_transform_list[i]*row[col]
                    i+=1
                y_list.append(val)
            print("yyyyyy {}".format(y_list))
        
        else:
            x_transform_list = [0 for i in range(10)]
            y_transform_list = [0 for i in range(10)]
            list_of_x_values = list_of_slider_values[10:]
            if is_any_non_zero(list_of_x_values):
                i=-1
                for x_vals in list_of_x_values:
                    i+=1
                    if x_vals is not 0:
                        x_transform_list[i] = x_vals
                        
            for index,row in df_scaled.iterrows():
                val=0
                i=0
                for col in axes_list:
                    val+=x_transform_list[i]*row[col]
                    i+=1
                x_list.append(val)
            
            print("xxxxxxx", x_list)

            list_of_y_values = list_of_slider_values[:10]
            if is_any_non_zero(list_of_y_values):
                i=-1
                for y_vals in list_of_y_values:
                    i+=1
                    if y_vals is not 0:
                        y_transform_list[i] = y_vals

            for index,row in df_scaled.iterrows():
                val=0
                i=0
                for col in axes_list:
                    val+=y_transform_list[i]*row[col]
                    i+=1
                y_list.append(val)
            print("yyyyyy {}".format(y_list))

    # when xaxis and yaxis is given and transform button is not pushed
    elif xAxis and yAxis:
        # TODO
        a=2
        x_list = df_scaled[xAxis].tolist()
        y_list = df_scaled[yAxis].tolist()
    
    elif xAxis or yAxis:
        x = StandardScaler().fit_transform(x)
        pca = PCA(n_components=2)
        principalComponents = pca.fit_transform(x)
        principalDf = pd.DataFrame(data = principalComponents, columns = ['principal_component_1', 'principal_component_2'])
        finalDf = pd.concat([principalDf, df1[['Name']]], axis = 1)
        x_list = finalDf['principal_component_1']
        y_list = finalDf['principal_component_2']
    x_list = scale(x_list)
    y_list = scale(y_list)
    figure = {
        'data': [
            {'x': x_list, 'y': y_list,
             'mode': 'markers',
             'marker': {
                 'color': '#0277bd',
                 'size': 10,
                 'opacity': 0.5,
                 'line': {'width': 0.5, 'color': 'white'},
                }
             }
        ],
        'layout': {
            'title': 'Scatter Plot',
            'hovermode': 'closest',
            'paper_bgcolor': '#e1f5fe',
            'plot_bgcolor': '#e1f5fe',
            'height': 500,
            'width': "75%",
            'clickmode': 'event+select'

        },

    }
    #Create graph and return
    return figure

@app.callback(
    Output('click-data', 'children'),
    [Input('scatter-plot', 'clickData')])

def display_click_data(clickData):
    #print(clickData)
    #print(type(clickData))
    data_point = dict()
    if clickData != None:
        #Point Number gives us the row from the dataframe
        point = clickData['points'][0]['pointNumber']
        filtered_df = df1[(df1.Number == point)]
        #print(filtered_df.head())

        #
        data_point = dict()
        data_point['points'] = []
        value_dict = {}
        value_dict['Name'] = str(filtered_df.Name.item())

        value_dict['Total'] = str(filtered_df.Total.item())

        value_dict['HP'] = str(filtered_df.HP.item())

        value_dict['Attack'] = str(filtered_df.Attack.item())

        value_dict['Defense'] = str(filtered_df.Defense.item())

        value_dict['Sp_Attack'] = str(filtered_df.Sp_Atk.item())

        value_dict['Sp_Defence'] = str(filtered_df.Sp_Def.item())

        value_dict['Speed'] = str(filtered_df.Speed.item())

        value_dict['Height (m)'] = str(filtered_df.Height_m.item())

        value_dict['Weight (kg)'] = str(filtered_df.Weight_kg.item())

        value_dict['Catch Rate'] = str(filtered_df.Catch_Rate.item())

        data_point['points'].append(value_dict)

    return json.dumps(data_point, indent=2)


@app.callback(
    
    Output('output1', 'children'),
    [Input('scatter-plot', 'clickData'),
    Input('xnbutton', 'n_clicks')])

#x-negative
def update_output(clickData,n_clicks):
    import csv
    import os
    x = open('x-negative.csv','a')
    x.close()
    if n_clicks == None and open('x-negative.csv'):
        os.remove('x-negative.csv')
    
    xnegative = open('x-negative.csv','a')
    count = 0
    if open('x-negative.csv'):
        countcsv = len(list(csv.reader(open('x-negative.csv'))))
    #xnegative = open('x-negative.csv','a')
    #print(clickData)
    #print(n_clicks)
    filtered_df = 're' 
    if n_clicks == None:
        count = 0
    else:
        count = int(n_clicks)
    if clickData != None and countcsv == count - 1:
        #Point Number gives us the row from the dataframe
        point = clickData['points'][0]['pointNumber']
        filtered_df = df_scaled.iloc[point]

        data_point = dict()
        data_point['points'] = []
        value_dict = {}

        value_dict['Total'] = str(filtered_df.Total.item())

        value_dict['HP'] = str(filtered_df.HP.item())

        value_dict['Attack'] = str(filtered_df.Attack.item())

        value_dict['Defense'] = str(filtered_df.Defense.item())

        value_dict['Sp_Attack'] = str(filtered_df.Sp_Atk.item())

        value_dict['Sp_Defence'] = str(filtered_df.Sp_Def.item())

        value_dict['Speed'] = str(filtered_df.Speed.item())

        value_dict['Height (m)'] = str(filtered_df.Height_m.item())

        value_dict['Weight (kg)'] = str(filtered_df.Weight_kg.item())

        value_dict['Catch Rate'] = str(filtered_df.Catch_Rate.item())
        
        data_point['points'].append(value_dict)
        
        temp = str(point) +','+value_dict['Total'] +','+value_dict['HP'] +','+value_dict['Attack'] +','+value_dict['Defense']+','+value_dict['Sp_Attack'] +','+value_dict['Sp_Defence']+','+value_dict['Speed']+','+value_dict['Height (m)']+','+value_dict['Weight (kg)'] +','+ value_dict['Catch Rate']+'\n' 

        xnegative.write(temp)

    k = 'Point added to negative x axis'
    xnegative.close()
    #return k


@app.callback(
    
    Output('output2', 'children'),
    [Input('scatter-plot', 'clickData'),
    Input('xpbutton', 'n_clicks')])

#x-positive
def update_output(clickData,n_clicks):
    import csv
    count = 0
    x = open('x-positive.csv','a')
    x.close()
    if n_clicks == None and open('x-positive.csv'):
        os.remove('x-positive.csv')
    xnegative = open('x-positive.csv','a')
    if open('x-positive.csv'):
        countcsv = len(list(csv.reader(open('x-positive.csv'))))
    
    #print(clickData)
    #print(n_clicks)
    filtered_df = 're' 
    if n_clicks == None:
        count = 0
    else:
        count = int(n_clicks)
    if clickData != None and countcsv == count - 1:
        #Point Number gives us the row from the dataframe
        point = clickData['points'][0]['pointNumber']
        filtered_df = df_scaled.iloc[point]        
        data_point = dict()
        data_point['points'] = []
        value_dict = {}

        value_dict['Total'] = str(filtered_df.Total.item())

        value_dict['HP'] = str(filtered_df.HP.item())

        value_dict['Attack'] = str(filtered_df.Attack.item())

        value_dict['Defense'] = str(filtered_df.Defense.item())

        value_dict['Sp_Attack'] = str(filtered_df.Sp_Atk.item())

        value_dict['Sp_Defence'] = str(filtered_df.Sp_Def.item())

        value_dict['Speed'] = str(filtered_df.Speed.item())

        value_dict['Height (m)'] = str(filtered_df.Height_m.item())

        value_dict['Weight (kg)'] = str(filtered_df.Weight_kg.item())

        value_dict['Catch Rate'] = str(filtered_df.Catch_Rate.item())
        
        data_point['points'].append(value_dict)
        
        temp = str(point) + ',' +value_dict['Total'] +','+value_dict['HP'] +','+value_dict['Attack'] +','+value_dict['Defense']+','+value_dict['Sp_Attack'] +','+value_dict['Sp_Defence']+','+value_dict['Speed']+','+value_dict['Height (m)']+','+value_dict['Weight (kg)'] +','+ value_dict['Catch Rate']+'\n' 

        xnegative.write(temp)

    #k = 'Point added to positive x axis'
    xnegative.close()
    #return k



@app.callback(
    
    Output('output3', 'children'),
    [Input('scatter-plot', 'clickData'),
    Input('ynbutton', 'n_clicks')])

#y-negative
def update_output(clickData,n_clicks):
    import csv
    x = open('y-negative.csv','a')
    x.close()
    if n_clicks == None and open('y-negative.csv'):
        os.remove('y-negative.csv')
    xnegative = open('y-negative.csv','a')
    count = 0
    if open('y-negative.csv'):
        countcsv = len(list(csv.reader(open('y-negative.csv'))))
    
    #print(clickData)
    #print(n_clicks)
    filtered_df = 're' 
    if n_clicks == None:
        count = 0
    else:
        count = int(n_clicks)
    if clickData != None and countcsv == count - 1:
        #Point Number gives us the row from the dataframe
        point = clickData['points'][0]['pointNumber']
        filtered_df = df_scaled.iloc[point]

        data_point = dict()
        data_point['points'] = []
        value_dict = {}

        value_dict['Total'] = str(filtered_df.Total.item())

        value_dict['HP'] = str(filtered_df.HP.item())

        value_dict['Attack'] = str(filtered_df.Attack.item())

        value_dict['Defense'] = str(filtered_df.Defense.item())

        value_dict['Sp_Attack'] = str(filtered_df.Sp_Atk.item())

        value_dict['Sp_Defence'] = str(filtered_df.Sp_Def.item())

        value_dict['Speed'] = str(filtered_df.Speed.item())

        value_dict['Height (m)'] = str(filtered_df.Height_m.item())

        value_dict['Weight (kg)'] = str(filtered_df.Weight_kg.item())

        value_dict['Catch Rate'] = str(filtered_df.Catch_Rate.item())
        
        data_point['points'].append(value_dict)
        
        temp = str(point) + ','+value_dict['Total'] +','+value_dict['HP'] +','+value_dict['Attack'] +','+value_dict['Defense']+','+value_dict['Sp_Attack'] +','+value_dict['Sp_Defence']+','+value_dict['Speed']+','+value_dict['Height (m)']+','+value_dict['Weight (kg)'] +','+ value_dict['Catch Rate']+'\n' 

        xnegative.write(temp)

    k = 'Point added to negative y axis'
    xnegative.close()
    #return k



@app.callback(
    
    Output('output4', 'children'),
    [Input('scatter-plot', 'clickData'),
    Input('ypbutton', 'n_clicks')])

#y-positive
def update_output(clickData,n_clicks):
    import csv
    count = 0
    x = open('y-positive.csv','a')
    x.close()
    if n_clicks == None and open('y-positive.csv'):
        os.remove('y-positive.csv')
    xnegative = open('y-positive.csv','a')
    if open('y-positive.csv'):
        countcsv = len(list(csv.reader(open('y-positive.csv'))))
    
    #print(clickData)
    #print(n_clicks)
    filtered_df = 're' 
    if n_clicks == None:
        count = 0
    else:
        count = int(n_clicks)
    if clickData != None and countcsv == count - 1:
        #Point Number gives us the row from the dataframe
        point = clickData['points'][0]['pointNumber']
        filtered_df = df_scaled.iloc[point]

        data_point = dict()
        data_point['points'] = []
        value_dict = {}

        value_dict['Total'] = str(filtered_df.Total.item())

        value_dict['HP'] = str(filtered_df.HP.item())

        value_dict['Attack'] = str(filtered_df.Attack.item())

        value_dict['Defense'] = str(filtered_df.Defense.item())

        value_dict['Sp_Attack'] = str(filtered_df.Sp_Atk.item())

        value_dict['Sp_Defence'] = str(filtered_df.Sp_Def.item())

        value_dict['Speed'] = str(filtered_df.Speed.item())

        value_dict['Height (m)'] = str(filtered_df.Height_m.item())

        value_dict['Weight (kg)'] = str(filtered_df.Weight_kg.item())

        value_dict['Catch Rate'] = str(filtered_df.Catch_Rate.item())
        
        data_point['points'].append(value_dict)
        
        temp = str(point) +','+value_dict['Total'] +','+value_dict['HP'] +','+value_dict['Attack'] +','+value_dict['Defense']+','+value_dict['Sp_Attack'] +','+value_dict['Sp_Defence']+','+value_dict['Speed']+','+value_dict['Height (m)']+','+value_dict['Weight (kg)'] +','+ value_dict['Catch Rate']+'\n' 

        xnegative.write(temp)

    k = 'Point added to positive y axis'
    xnegative.close()
    #return k



if __name__ == '__main__':
    app.run_server(debug=True)
