

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
df = dh.get_all_cdi()
dis_ques = df[df["topic"]=="Disability"]["question"].unique()
dis_year = df[df["topic"]=="Disability"]["yearstart"].unique()
diab_ques = df[df["topic"]=="Diabetes"]["question"].unique()
diab_year = df[df["topic"]=="Diabetes"]["yearstart"].unique()
obes_quest = df[df["topic"]=="Nutrition, Physical Activity, and Weight Status"]["question"].unique()
topics = df["topic"].unique()
states_df = dh.get_cdi_cond(
        "topic, yearstart, datavaluetype,stratificationcategory1,locationdesc,datavalue,question,locationabbr",
        'locationdesc',
        dh.us_states
        )

app.layout = html.Div([
    cdc.explanation_component("introduction.md",header = "Introduction"),
    cdc.explanation_component("eda_1.md",header = "Question Distribution"),
    
    dcc.Dropdown(sorted(questions),style={"width":"150px"},id='state_questions'),
    html.Div([
        dcc.Graph(
            id='questions_plot',
            style={
                "width":"100%",
                "height":"3000px",
            }
        ),
    ],style={
        "overflowY":"scroll",
        "height":"500px",
        "width":"100%"

    }),
    cdc.explanation_component("eda_2.md",header = "Location Distribution"),
    dcc.Dropdown(sorted(states),style={"width":"1000px"},id='question_drop',value="all"),
    dcc.Graph(
        id='locale',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    dcc.Dropdown(sorted(topics),style={"width":"1000px"},id='topic_drop',value="Diabetes"),
    dcc.Graph(
        id='strat',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    cdc.explanation_component("eda_3.md",header="Life Expectancy Analysis"),
    dcc.RadioItems([2018,2019,2020],style={"width":"150px"},id='le_bar_year',value=2019),
    dcc.Graph(
        id='le_bar',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    dcc.RadioItems([2018,2019,2020],style={"width":"150px"},id='le_map_year',value=2019),
    dcc.Graph(
        id='le_map',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    cdc.explanation_component("sdoh_intro.md",header = "Trends Seen in Social Determinants of Health"),
    dcc.RadioItems(dis_year,style={"width":"150px"},id='dis_bar_year',value=2019),
    dcc.Dropdown(dis_ques,style={"width":"1000px"},id='dis_bar_ques_drop',value="Adults with any disability"),
    dcc.Graph(
        id='dis_bar',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    dcc.RadioItems(dis_year,style={"width":"150px"},id='dis_map_year',value=2019),
    dcc.Dropdown(dis_ques,style={"width":"1000px"},id='dis_map_ques_drop',value="Adults with any disability"),
    dcc.Graph(
        id='dis_map',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    dcc.RadioItems(diab_year,style={"width":"150px"},id='diab_bar_year',value=2019),
    dcc.Dropdown(diab_ques,style={"width":"1000px"},id='diab_bar_ques_drop',value="Diabetes among adults"),
    dcc.Graph(
        id='diab_bar',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    dcc.RadioItems(diab_year,style={"width":"150px"},id='diab_map_year',value=2019),
    dcc.Dropdown(diab_ques,style={"width":"1000px"},id='diab_map_ques_drop',value="Diabetes among adults"),
    dcc.Graph(
        id='diab_map',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    dcc.Dropdown(questions,style={"width":"1000px"},id='obesity_line_state_drop',value="Alabama"),
    cdc.explanation_component("sdoh_conclusion.md",header = "Social Determinant Trends Hold True"),
    dcc.Graph(
        id='obesity_line',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    cdc.explanation_component("eda_n.md",header = "Life Expectancy Predictors"),
    dcc.Graph(
        id='life_sleep',
        figure = eda_plots.coorelation(),
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
],
style={
    "width":"100vw",
    "display":"flex",
    "align-items":"center",
    "flex-direction":"column",
    "padding":"0 6em",
    "box-sizing":'border-box',
    "background-color":"#1C506C"
})

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
