

import dash
from dash import dcc
from dash import html
import custom_dash_component as cdc
import eda_plots
import pandas as pd
import data_handler as dh
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server




# see https://plotly.com/python/px-arguments/ for more options

questions = dh.get_cdi_field('locationdesc')["locationdesc"].unique()
states = dh.get_cdi_field("question")["question"].unique()

app.layout = html.Div([
    cdc.explanation_component("introduction.md",header = "Introduction"),
    cdc.explanation_component("eda_1.md",header = "Question Distribution"),
    dcc.Dropdown(sorted(questions),style={"width":"150px"},id='state_questions'),
    html.Div([
        dcc.Graph(
            id='questions_plot',
            style={
                "wdith":"40vh",
                "height":"3000px",
            }
        ),
    ],style={
        "overflowY":"scroll",
        "height":"500px",

    }),
    cdc.explanation_component("eda_2.md",header = "Location Distribution"),
    dcc.Dropdown(sorted(states),style={"width":"1000px"},id='question_drop',value="all"),
    dcc.Graph(
        id='locale',
        style={
            "wdith":"40vh",
            "height":"70vh",
        }
    ),
    cdc.explanation_component("eda_3.md",header="Life Expectancy Analysis")
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
