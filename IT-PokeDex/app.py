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

from dash.exceptions import PreventUpdate

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

    # The memory store reverts to the default on every page refresh


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
                    dcc.Graph(
                        id='scatter-plot',
                    ),
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
            html.Button('X -ve', id='xnbutton'),
            html.Button('X +ve', id='xpbutton'),
            html.Button('Y -ve', id='ynbutton'),
            html.Button('Y +ve', id='ypbutton'),
            html.Button('Transform', id='transform'),

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
                "height": 100,
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

@app.callback(
    Output(component_id='scatter-plot', component_property='figure'),
    [Input(component_id='xaxis-dropdown', component_property='value'),
    Input(component_id='yaxis-dropdown', component_property='value'),
    Input('transform', 'n_clicks')]
)

def updateScatterPlot(xAxis, yAxis,n_clicks):
    print(n_clicks)
    #Get DF
    #print(xAxis)
    x_list = df[xAxis].values.tolist()
    y_list = df[yAxis].values.tolist()


    #print(df.head())

    #print(len(x_list),len(y_list))
    #Get Max and Min values for axes and normalize the points
    denum = math.sqrt(sum((i**2) for i in x_list))
    for index in range(len(x_list)):
        x_list[index] = x_list[index]/denum

    #print(x_list)

    denum = math.sqrt(sum((i ** 2) for i in y_list))
    for index in range(len(y_list)):
        y_list[index] = y_list[index]/denum

    figure = {
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
    print(clickData)
    print(type(clickData))
    data_point = dict()
    if clickData != None:
        #Point Number gives us the row from the dataframe
        point = clickData['points'][0]['pointNumber']
        filtered_df = df[(df.Number == point)]
        print(filtered_df.head())

        #
        data_point = dict()
        data_point['points'] = []
        value_dict = {}
        value_dict['Name'] = str(filtered_df.Name.item())
        value_dict['Type_1'] = str(filtered_df.Type_1.item())
        value_dict['Type_2'] = str(filtered_df.Type_2.item())

        value_dict['Total'] = str(filtered_df.Total.item())

        value_dict['HP'] = str(filtered_df.HP.item())

        value_dict['Attack'] = str(filtered_df.Attack.item())

        value_dict['Defense'] = str(filtered_df.Defense.item())

        value_dict['Sp_Attack'] = str(filtered_df.Sp_Atk.item())

        value_dict['Sp_Defence'] = str(filtered_df.Sp_Def.item())

        value_dict['Color'] = str(filtered_df.Color.item())

        value_dict['Has Mega Evolution'] = str(filtered_df.hasMegaEvolution.item())

        value_dict['Height (m)'] = str(filtered_df.Height_m.item())

        value_dict['Weight (kg)'] = str(filtered_df.Weight_kg.item())

        value_dict['Catch Rate'] = str(filtered_df.Catch_Rate.item())

        data_point['points'].append(value_dict)

    #print(clickData['points'])
    #print(clickData['points'][0][0]['pointNumber'])

    return json.dumps(data_point, indent=2)


@app.callback(
    
    Output('output1', 'children'),
    [Input('scatter-plot', 'clickData'),
    Input('xnbutton', 'n_clicks')])

#negativex
def update_output(clickData,n_clicks,):
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
        filtered_df = df[(df.Number == point)]
        #print(filtered_df.head())

        #
        data_point = dict()
        data_point['points'] = []
        value_dict = {}
        value_dict['Name'] = str(filtered_df.Name.item())
        value_dict['Type_1'] = str(filtered_df.Type_1.item())
        value_dict['Type_2'] = str(filtered_df.Type_2.item())

        value_dict['Total'] = str(filtered_df.Total.item())

        value_dict['HP'] = str(filtered_df.HP.item())

        value_dict['Attack'] = str(filtered_df.Attack.item())

        value_dict['Defense'] = str(filtered_df.Defense.item())

        value_dict['Sp_Attack'] = str(filtered_df.Sp_Atk.item())

        value_dict['Sp_Defence'] = str(filtered_df.Sp_Def.item())

        value_dict['Color'] = str(filtered_df.Color.item())

        value_dict['Has Mega Evolution'] = str(filtered_df.hasMegaEvolution.item())

        value_dict['Height (m)'] = str(filtered_df.Height_m.item())

        value_dict['Weight (kg)'] = str(filtered_df.Weight_kg.item())
        
        value_dict['Catch Rate'] = str(filtered_df.Catch_Rate.item())

        data_point['points'].append(value_dict)
        
        temp = str(point) + ',' +value_dict['Name'] +','+ value_dict['Type_1'] +','+ value_dict['Type_2'] +','+value_dict['Total'] +','+value_dict['HP'] +','+value_dict['Attack'] +','+value_dict['Defense']+','+value_dict['Sp_Attack'] +','+value_dict['Sp_Defence']+','+ value_dict['Color'] + ','+value_dict['Has Mega Evolution']+','+value_dict['Height (m)']+','+value_dict['Weight (kg)'] +','+ value_dict['Catch Rate']+'\n' 

        xnegative.write(temp)

    k = 'Point added to negative x axis'
    xnegative.close()
    #return k

    




@app.callback(
    
    Output('output2', 'children'),
    [Input('scatter-plot', 'clickData'),
    Input('xpbutton', 'n_clicks')])

#negativex
def update_output(clickData,n_clicks,):
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
        filtered_df = df[(df.Number == point)]
        #print(filtered_df.head())

        #
        data_point = dict()
        data_point['points'] = []
        value_dict = {}
        value_dict['Name'] = str(filtered_df.Name.item())
        value_dict['Type_1'] = str(filtered_df.Type_1.item())
        value_dict['Type_2'] = str(filtered_df.Type_2.item())

        value_dict['Total'] = str(filtered_df.Total.item())

        value_dict['HP'] = str(filtered_df.HP.item())

        value_dict['Attack'] = str(filtered_df.Attack.item())

        value_dict['Defense'] = str(filtered_df.Defense.item())

        value_dict['Sp_Attack'] = str(filtered_df.Sp_Atk.item())

        value_dict['Sp_Defence'] = str(filtered_df.Sp_Def.item())

        value_dict['Color'] = str(filtered_df.Color.item())

        value_dict['Has Mega Evolution'] = str(filtered_df.hasMegaEvolution.item())

        value_dict['Height (m)'] = str(filtered_df.Height_m.item())

        value_dict['Weight (kg)'] = str(filtered_df.Weight_kg.item())
        
        value_dict['Catch Rate'] = str(filtered_df.Catch_Rate.item())

        data_point['points'].append(value_dict)
        
        temp = str(point) + ',' +value_dict['Name'] +','+ value_dict['Type_1'] +','+ value_dict['Type_2'] +','+value_dict['Total'] +','+value_dict['HP'] +','+value_dict['Attack'] +','+value_dict['Defense']+','+value_dict['Sp_Attack'] +','+value_dict['Sp_Defence']+','+ value_dict['Color'] + ','+value_dict['Has Mega Evolution']+','+value_dict['Height (m)']+','+value_dict['Weight (kg)'] +','+ value_dict['Catch Rate']+'\n' 

        xnegative.write(temp)

    #k = 'Point added to positive x axis'
    xnegative.close()
    #return k



@app.callback(
    
    Output('output3', 'children'),
    [Input('scatter-plot', 'clickData'),
    Input('ynbutton', 'n_clicks')])

#negativex
def update_output(clickData,n_clicks,):
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
        filtered_df = df[(df.Number == point)]
        #print(filtered_df.head())

        #
        data_point = dict()
        data_point['points'] = []
        value_dict = {}
        value_dict['Name'] = str(filtered_df.Name.item())
        value_dict['Type_1'] = str(filtered_df.Type_1.item())
        value_dict['Type_2'] = str(filtered_df.Type_2.item())

        value_dict['Total'] = str(filtered_df.Total.item())

        value_dict['HP'] = str(filtered_df.HP.item())

        value_dict['Attack'] = str(filtered_df.Attack.item())

        value_dict['Defense'] = str(filtered_df.Defense.item())

        value_dict['Sp_Attack'] = str(filtered_df.Sp_Atk.item())

        value_dict['Sp_Defence'] = str(filtered_df.Sp_Def.item())

        value_dict['Color'] = str(filtered_df.Color.item())

        value_dict['Has Mega Evolution'] = str(filtered_df.hasMegaEvolution.item())

        value_dict['Height (m)'] = str(filtered_df.Height_m.item())

        value_dict['Weight (kg)'] = str(filtered_df.Weight_kg.item())
        
        value_dict['Catch Rate'] = str(filtered_df.Catch_Rate.item())

        data_point['points'].append(value_dict)
        
        temp = str(point) + ',' +value_dict['Name'] +','+ value_dict['Type_1'] +','+ value_dict['Type_2'] +','+value_dict['Total'] +','+value_dict['HP'] +','+value_dict['Attack'] +','+value_dict['Defense']+','+value_dict['Sp_Attack'] +','+value_dict['Sp_Defence']+','+ value_dict['Color'] + ','+value_dict['Has Mega Evolution']+','+value_dict['Height (m)']+','+value_dict['Weight (kg)'] +','+ value_dict['Catch Rate']+'\n' 

        xnegative.write(temp)

    k = 'Point added to negative y axis'
    xnegative.close()
    #return k



@app.callback(
    
    Output('output4', 'children'),
    [Input('scatter-plot', 'clickData'),
    Input('ypbutton', 'n_clicks')])

#negativex
def update_output(clickData,n_clicks,):
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
        filtered_df = df[(df.Number == point)]
        #print(filtered_df.head())

        #
        data_point = dict()
        data_point['points'] = []
        value_dict = {}
        value_dict['Name'] = str(filtered_df.Name.item())
        value_dict['Type_1'] = str(filtered_df.Type_1.item())
        value_dict['Type_2'] = str(filtered_df.Type_2.item())

        value_dict['Total'] = str(filtered_df.Total.item())

        value_dict['HP'] = str(filtered_df.HP.item())

        value_dict['Attack'] = str(filtered_df.Attack.item())

        value_dict['Defense'] = str(filtered_df.Defense.item())

        value_dict['Sp_Attack'] = str(filtered_df.Sp_Atk.item())

        value_dict['Sp_Defence'] = str(filtered_df.Sp_Def.item())

        value_dict['Color'] = str(filtered_df.Color.item())

        value_dict['Has Mega Evolution'] = str(filtered_df.hasMegaEvolution.item())

        value_dict['Height (m)'] = str(filtered_df.Height_m.item())

        value_dict['Weight (kg)'] = str(filtered_df.Weight_kg.item())
        
        value_dict['Catch Rate'] = str(filtered_df.Catch_Rate.item())

        data_point['points'].append(value_dict)
        
        temp = str(point) + ',' +value_dict['Name'] +','+ value_dict['Type_1'] +','+ value_dict['Type_2'] +','+value_dict['Total'] +','+value_dict['HP'] +','+value_dict['Attack'] +','+value_dict['Defense']+','+value_dict['Sp_Attack'] +','+value_dict['Sp_Defence']+','+ value_dict['Color'] + ','+value_dict['Has Mega Evolution']+','+value_dict['Height (m)']+','+value_dict['Weight (kg)'] +','+ value_dict['Catch Rate']+'\n' 

        xnegative.write(temp)

    k = 'Point added to positive y axis'
    xnegative.close()
    #return k



if __name__ == '__main__':
    app.run_server(debug=True)
