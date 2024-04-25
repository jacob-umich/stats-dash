import plotly.express as px
import dash
import data_handler as dh
from SHOD_cleaning_data import us_states

@dash.callback(
    dash.Output(component_id="questions_plot",component_property="figure"),
    dash.Input(component_id='state_questions',component_property="value")
)
def question_plot(state=None):
    cdi_questions = dh.get_cdi_field("question,locationdesc")
    if state:
        cdi_questions = cdi_questions[cdi_questions["locationdesc"]==state]
    cdi_questions=cdi_questions.groupby("question").size().to_frame("count").reset_index().sort_values("count",axis=0)
    fig = px.bar(cdi_questions, x="count",y="question", orientation="h")
    return fig

@dash.callback(
    dash.Output(component_id="locale",component_property="figure"),
    dash.Input(component_id='question_drop',component_property="value")
)
def location_plot(question=None):
    data = dh.get_cdi_field("locationdesc, locationabbr,question")
    if question!=None and  question!="all":
        data = data[data['question']==question]
    data = data[data['locationdesc'].isin(us_states)]
    data = data.groupby("locationabbr").size().to_frame("count").reset_index()
    fig = px.choropleth(data,locationmode="USA-states",scope="usa",locations=data['locationabbr'],color=data['count'])
    return fig

if __name__=="__main__":
    location_plot()