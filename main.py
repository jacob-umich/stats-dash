

import dash
from dash import dcc
from dash import html
import custom_dash_component as cdc
import eda_plots
import pandas as pd
import data_handler as dh
import predict_engine

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

alc_year = df[df["topic"]=="Alcohol"]["yearstart"].unique()
alc_ques = df[df["topic"]=="Alcohol"]["question"].unique()
alc_metric = df[df["topic"]=="Alcohol"]["datavaluetype"].unique()

smoke_year = df[df["topic"]=="Tobacco"]["yearstart"].unique()
smoke_ques = df[df["topic"]=="Tobacco"]["question"].unique()
smoke_metric = df[df["topic"]=="Tobacco"]["datavaluetype"].unique()

stress_year = df[df["topic"]=="Mental Health"]["yearstart"].unique()
stress_ques = df[df["topic"]=="Mental Health"]["question"].unique()
stress_metric = df[df["topic"]=="Mental Health"]["datavaluetype"].unique()

obes_quest = df[df["topic"]=="Nutrition, Physical Activity, and Weight Status"]["question"].unique()
topics = df["topic"].unique()
states_df = dh.get_cdi_cond(
        "topic, yearstart, datavaluetype,stratificationcategory1,locationdesc,datavalue,question,locationabbr",
        'locationdesc',
        dh.us_states
        )

app.layout = html.Div([
    cdc.explanation_component("introduction.md",header = "Chronic Disease Indicators"),
    cdc.explanation_component("eda_1.md",header = "Question Distribution"),
    
    dcc.Dropdown(sorted(questions),style={"width":"150px"},id='state_questions'),
    html.Div([
        dcc.Graph(
            id='questions_plot',
            style={
                "width":"100%",
                "height":"100%",
            }
        ),
    ],style={
        "overflowX":"scroll",
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
    cdc.explanation_component("eda_4.md",header="Presence and Types of Data"),
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
    cdc.explanation_component("disability.md",header = "Comparison of Disability Prevalence"),
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
    cdc.explanation_component("diabetes.md",header = "Comparison of Diabetes Prevalence"),
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
    dcc.RadioItems(diab_year,style={"width":"150px"},id='diabetes_hist_year',value=2019),
    dcc.Graph(
        id='diabetes_hist',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    cdc.explanation_component("obesity.md",header = "Obesity"),
    dcc.Dropdown(questions,style={"width":"1000px"},id='obesity_line_state_drop',value="Alabama"),
    dcc.Graph(
        id='obesity_line',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    cdc.explanation_component("sdoh_conclusion.md",header = "Social Determinant Trends Hold True"),

    cdc.explanation_component("alcohol.md",header = "Alcohol Consumption"),
    dcc.Dropdown(alc_ques,style={"width":"1000px"},id='alc_scat_qeust',value="Binge drinking intensity among adults who binge drink"),
    dcc.Dropdown(alc_year,style={"width":"1000px"},id='alc_scat_year',value=2019),
    dcc.Dropdown(alc_metric,style={"width":"1000px"},id='alc_scat_metric',value="Crude Median"),
    dcc.Graph(
        id='alc_scat',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    cdc.explanation_component("smoke.md",header = "Smoking"),
    dcc.Dropdown(smoke_ques,style={"width":"1000px"},id='smoke_scat_qeust',value="Quit attempts in the past year among adult current smokers"),
    dcc.Dropdown(smoke_year,style={"width":"1000px"},id='smoke_scat_year',value=2019),
    dcc.Dropdown(smoke_metric,style={"width":"1000px"},id='smoke_scat_metric',value="Crude Prevalence"),
    dcc.Graph(
        id='smoke_scat',
        style={
            "width":"100%",
            "height":"70vh",
        }
    ),
    cdc.explanation_component("depression.md",header = "Mental Health"),
    dcc.Dropdown(stress_ques,style={"width":"1000px"},id='stress_scat_qeust',value="Depression among adults"),
    dcc.Dropdown(stress_year,style={"width":"1000px"},id='stress_scat_year',value=2019),
    dcc.Dropdown(stress_metric,style={"width":"1000px"},id='stress_scat_metric',value="Crude Prevalence"),
    dcc.Graph(
        id='stress_scat',
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
    cdc.explanation_component("ml.md",header = "Machine Learning Prediction"),
    html.Label('percentage of population that is obese',style={"color":"#DBF7EC"}),
    dcc.Input(value=50, type='number',id="ml_ob"),
    html.Label('percentage of population that smokes',style={"color":"#DBF7EC"}),
    dcc.Input(value=50, type='number',id="ml_smoke"),
    html.Label('percentage of population that doesn\'t get enough sleep',style={"color":"#DBF7EC"}),
    dcc.Input(value=50, type='number',id="ml_sleep"),
    html.P("The life expectancy for your population is:",style={"color":"#DBF7EC"}),
    html.Div(id="ml_predict",style={"color":"#DBF7EC"})
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
