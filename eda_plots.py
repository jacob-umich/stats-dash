import plotly.express as px
import dash
import data_handler as dh
from SHOD_cleaning_data import us_states
import pandas as pd

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

@dash.callback(
    dash.Output(component_id="strat",component_property="figure"),
    dash.Input(component_id='topic_drop',component_property="value")
)
def tree_strat(topic):
    data = dh.get_cdi_field("topic, question,datavaluetype,stratification1,datavalue")
    data = data[data["topic"]==topic]

    data = data.groupby(["question","datavaluetype","stratification1"],as_index=False).agg(
        count=pd.NamedAgg(column="datavalue",aggfunc="count"),
        size=pd.NamedAgg(column="datavalue",aggfunc="size")
    )
    data['ratio'] = (data['size']-data['count'])/data['size']

    fig = px.sunburst(
        data, 
        path=["question","datavaluetype","stratification1"],
        values='count',
        color="ratio"
    )
    return fig



@dash.callback(
    dash.Output(component_id="le_bar",component_property="figure"),
    dash.Input(component_id='le_bar_year',component_property="value")
)
def life_expectancy_plot(year):
    life_data_low, life_data_high = dh.get_high_low_life_data(year)

    life_data_low['Group'] = 'Lowest Life Expectancy'
    life_data_high['Group'] = 'Highest Life Expectancy'
    combined_data = pd.concat([life_data_low, life_data_high])

    fig = px.bar(
        combined_data, y='state', x='rate', color='Group', barmode='group',
        labels={'state': 'State', 'rate': 'Life Expectancy'},
        title='Top 5 and Bottom 5 States for Life Expectancy in 2019',
        color_discrete_map={'Lowest Life Expectancy': 'red', 'Highest Life Expectancy': 'green'}
    )
    fig.update_yaxes(categoryorder='total ascending')
    fig.update_traces(marker_line_width=1.5, marker_line_color='black')
    fig.update_xaxes(range=[70, 81], dtick=4)
    fig.update_layout(
        title='<b>2019 Life Expectancy: Best and Worst States</b>')
    fig.update_layout(title_x=0.5, title_font=dict(size=20, family='Arial', color='black'))
    fig.update_layout(
        legend=dict(
            x=0.78,
            y=0.02,
            bgcolor='rgba(255, 255, 255, 0.5)'
        )
    )
    return fig


@dash.callback(
    dash.Output(component_id="le_map",component_property="figure"),
    dash.Input(component_id='le_map_year',component_property="value")
)
def life_expectancy_map(year):
    # add a slider for the year
    simple_life_data = dh.simple_life(year)
    fig = px.choropleth(
        simple_life_data,
        locations='state',
        locationmode='USA-states',
        color='rate',
        scope='usa',
        color_continuous_scale='Viridis',
        title='2019 Life Expectancy by State'
    )

    fig.update_layout(title_x=0.5)
    fig.update_layout(coloraxis_colorbar_title_text='Average Lifespan')
    return fig

@dash.callback(
    dash.Output(component_id="dis_bar",component_property="figure"),
    [dash.Input(component_id='dis_bar_ques_drop',component_property="value"),
    dash.Input(component_id='dis_bar_year',component_property="value")]
)
def dis_bar(question,year):
    disability_bad, disability_good = dh.disability_rates(question,year)
    disability_bad['Group'] = 'Highest Percentage of Disabled Adults'
    disability_good['Group'] = 'Lowest Percentage of Disabled Adults'
    combined_data = pd.concat([disability_bad, disability_good])
    fig = px.bar(
        combined_data, y='locationdesc', x='datavalue', color='Group', barmode='group',
        labels={'locationdesc': 'state', 'datavalue': '% of Disabled Adults'},
        color_discrete_map={'Lowest Percentage of Disabled Adults': 'green', 'Highest Percentage of Disabled Adults': 'red'})
    fig.update_yaxes(categoryorder='total ascending')
    fig.update_traces(marker_line_width=1.5, marker_line_color='black')
    fig.update_xaxes(range=[18, 43], dtick=4)
    fig.update_layout(
        title='<b>% of Adults with Disability: Best and Worst States</b>')
    fig.update_layout(title_x=0.5, title_font=dict(size=20, family='Arial', color='black'))
    fig.update_layout(
        legend=dict(
            x=0.68,
            y=0.02,
            bgcolor='rgba(255, 255, 255, 0.5)'
        )
    )

    return fig


@dash.callback(
    dash.Output(component_id="dis_map",component_property="figure"),
    dash.Input(component_id='dis_map_ques_drop',component_property="value"),
    dash.Input(component_id='dis_map_year',component_property="value")
)
def dis_map(question,year):

    disability_code = dh.disability_simple(question,year)

    fig = px.choropleth(
        disability_code,
        locations='locationabbr',
        locationmode='USA-states',
        color='datavalue',
        scope='usa',
        color_continuous_scale='Inferno',
        title='2019 Precent of U.S. Adults with Any Disability'
    )

    fig.update_layout(title_x=0.5)
    fig.update_layout(coloraxis_colorbar_title_text='% of Disabled Adults')

    return fig



@dash.callback(
    dash.Output(component_id="diab_bar",component_property="figure"),
    dash.Input(component_id='diab_bar_ques_drop',component_property="value"),
    dash.Input(component_id='diab_bar_year',component_property="value")
)
def diab_bar(question, year):
    diabetes_bad, diabetes_good = dh.diabetes_rates(question,year)
    diabetes_bad['Group'] = 'Highest Percentage of Adults with Diabetes'
    diabetes_good['Group'] = 'Lowest Percentage of Adults with Diabetes'
    combined_data = pd.concat([diabetes_bad, diabetes_good])
    fig = px.bar(
        combined_data, y='locationdesc', x='datavalue', color='Group', barmode='group',
        labels={'LocationDesc': 'State', 'DataValue': '% of Disabled Adults'},
        color_discrete_map={'Lowest Percentage of Adults with Diabetes': 'green', 'Highest Percentage of Adults with Diabetes': 'red'})
    fig.update_yaxes(categoryorder='total ascending')
    fig.update_traces(marker_line_width=1.5, marker_line_color='black')
    fig.update_xaxes(range=[6, 16], dtick=4)
    fig.update_layout(
        title='<b>% of Adults with Diabetes: Best and Worst States</b>')
    fig.update_layout(title_x=0.5, title_font=dict(size=20, family='Arial', color='black'))
    fig.update_layout(
        legend=dict(
            x=0.68,
            y=0.02,
            bgcolor='rgba(255, 255, 255, 0.5)'
        )
    )
    return fig


@dash.callback(
    dash.Output(component_id="diab_map",component_property="figure"),
    dash.Input(component_id='diab_map_ques_drop',component_property="value"),
    dash.Input(component_id='diab_map_year',component_property="value")
)
def diab_map(question,year):

    diabetes_simple = dh.diabetes_simple(question,year)

    fig = px.choropleth(
        diabetes_simple,
        locations='locationabbr',
        locationmode='USA-states',
        color='datavalue',
        scope='usa',
        color_continuous_scale='Plasma',
        title='Percentage of Adults with Diabetes in 2019'
    )

    fig.update_layout(title_x=0.5)
    fig.update_layout(coloraxis_colorbar_title_text='% of Adults with Diabetes')

    return fig

if __name__=="__main__":
    location_plot()