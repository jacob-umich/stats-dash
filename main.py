

import dash
from dash import dcc
from dash import html
import eda_plots
import pandas as pd


app = dash.Dash(__name__)
server = app.server




# see https://plotly.com/python/px-arguments/ for more options




app.layout = html.Div([
    html.H1("Question distribution"),
    html.Div([
        dcc.Graph(
            id='question',
            figure=eda_plots.question_plot(),
            style={
                "wdith":"40vh",
                "height":"3000px",
            }
        ),
    ],style={
        "overflowY":"scroll",
        "height":"500px",

    }
    ),
    html.H1("Location distribution"),
    dcc.Graph(
        id='locale',
        figure=eda_plots.location_plot(),
        style={
            "wdith":"40vh",
            "height":"70vh",
        }
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
