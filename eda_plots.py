import plotly.express as px
import data_handler as dh
from SHOD_cleaning_data import us_states

def question_plot():
    cdi_questions = dh.get_cdi_field("question")
    cdi_questions=cdi_questions.groupby("question").size().to_frame("count").reset_index().sort_values("count",axis=0)
    fig = px.bar(cdi_questions, x="count",y="question", orientation="h")
    return fig

def location_plot():
    data = dh.get_cdi_field("locationdesc, locationabbr")
    data = data[data['locationdesc'].isin(us_states)]
    data = data.groupby("locationabbr").size().to_frame("count").reset_index()
    fig = px.choropleth(data,locationmode="USA-states",scope="usa",locations=data['locationabbr'],color=data['count'])
    return fig

if __name__=="__main__":
    location_plot()