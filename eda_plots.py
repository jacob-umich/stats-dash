import plotly.express as px
import dash
import data_handler as dh
from SHOD_cleaning_data import us_states
import pandas as pd
import sqlite3
import textwrap

@dash.callback(
    dash.Output(component_id="questions_plot",component_property="figure"),
    dash.Input(component_id='state_questions',component_property="value")
)
def question_plot(state=None):
    cdi_questions = dh.get_cdi_field("question,locationdesc,yearstart")
    if state:
        cdi_questions = cdi_questions[cdi_questions["locationdesc"]==state]
    cdi_questions=cdi_questions.groupby(["question","yearstart"],as_index=False).agg(
        count=pd.NamedAgg(column="question",aggfunc="count")).sort_values("count",axis=0)
    qs = [f"q{i}" for i in range(len(cdi_questions['question'].unique()))]
    fig = px.bar(cdi_questions, y="count",x="question",hover_name="question", orientation="v",color="yearstart",barmode="relative")
    fig.update_layout(
        title='<b>Number of data entries for each question</b>',
        xaxis_title="Question (hover for question)",
        yaxis_title="Number of entries in database"
    )
    fig.update_xaxes(showticklabels=False)
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
    fig.update_layout(
        title='<b>Number of data entries for each question per state</b>',
    )
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

    def customwrap(s,width=30):
        return "<br>".join(textwrap.wrap(s,width=width))

    data['ratio'] = (data['size']-data['count'])/data['size']
    data.drop(data.loc[data['count']==0].index,inplace=True)
    data["question"]=data["question"].map(customwrap)
    data["datavaluetype"]=data["datavaluetype"].map(customwrap)
    fig = px.sunburst(
        data, 
        path=["question","datavaluetype","stratification1"],
        values='count',
        color="ratio"
    )
    fig.update_layout(
        title='<b>Tree structure of chronic disease indicator dataset</b>',
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
        title='Top 5 and Bottom 5 States for Life Expectancy',
        color_discrete_map={'Lowest Life Expectancy': 'red', 'Highest Life Expectancy': 'green'}
    )
    fig.update_yaxes(categoryorder='total ascending')
    fig.update_traces(marker_line_width=1.5, marker_line_color='black')
    fig.update_xaxes(range=[70, 81], dtick=4)
    fig.update_layout(
        title='<b>Life Expectancy: Best and Worst States</b>')
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
        title='Life Expectancy by State'
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
        title='Precent of U.S. Adults with Any Disability'
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


def coorelation():
    data = dh.df
    sleep_data = data[
        (data["question"]=="Short sleep duration among adults") &
        (data["datavaluetype"]=="Crude Prevalence") &
        (data["stratification1"]=="Overall")
        ]
    sleep_data = sleep_data.rename({"datavalue":"sleep"},axis=1)
    smoke_data = data[
        (data["question"]=="Current cigarette smoking among adults") &
        (data["datavaluetype"]=="Crude Prevalence") &
        (data["stratification1"]=="Overall")
        ]
    smoke_data = smoke_data.rename({"datavalue":"smoke"},axis=1)
    obesity_data = data[
        (data["question"]=="Obesity among adults") &
        (data["datavaluetype"]=="Crude Prevalence") &
        (data["stratification1"]=="Overall")
        ]
    obesity_data = obesity_data.rename({"datavalue":"obese"},axis=1)
    life_data = dh.get_all_le()
    merged = pd.merge(life_data,smoke_data,left_on=["state","year"],right_on=["locationabbr","yearstart"])
    merged = pd.merge(merged,sleep_data,how="left",left_on=["state","year"],right_on=["locationabbr","yearstart"])
    merged = pd.merge(merged,obesity_data,how="left",left_on=["state","year"],right_on=["locationabbr","yearstart"])
    fig = px.scatter_matrix(
        merged, 
        dimensions=['obese','sleep','smoke','rate'],
        color="year",
        color_continuous_scale='Viridis',
        labels={
            "obese":"%  obese",
            "sleep":"%  sleep deprived",
            "smoke":"%  that smokes",
            "rate":"Life expectancy",
        }
    )
    fig.update_layout(
        title='<b>Correlation between CDI variables and life expectancy</b>'
    )
    return fig
#chris plots (5 scatter plots):

@dash.callback(
    dash.Output(component_id="obesity_line",component_property="figure"),
    dash.Input(component_id='obesity_line_state_drop',component_property="value")
)
def obesity_line(location):
    print(location)
    obesity_rates = dh.obesity(location)
    fig = px.line(
        obesity_rates, 
        x='yearstart', 
        y='datavalue', 
        title=f'Obesity Rates Among Adults in {location}',
        # markers=True, 
        line_shape='linear'
    )
    fig.update_traces(mode='markers+lines')
    fig.update_layout(title_x=0.5)
    fig.update_xaxes(type='category', title='Year')
    fig.update_yaxes(title='Percent of Obese Adults')
    return fig
    
@dash.callback(
    dash.Output(component_id="diabetes_hist",component_property="figure"),
    dash.Input(component_id='diabetes_hist_year',component_property="value")
)
def diabetes_hist(year):
    filter_df = dh.diabetes_simple('Diabetes among adults',year)
    fig = px.histogram(
    filter_df,
    x = 'datavalue', 
    nbins = 5,
    title = 'Distribution of Adults with Diabetes',
    )
    fig.update_layout(title_x=0.5)
    fig.update_layout(coloraxis_colorbar_title_text='Distribution of Adults with Diabetes')
    fig.update_layout(xaxis_title='% of Adults', yaxis_title='Count')
    return fig

#le vs. binge drink freq.
@dash.callback(
    dash.Output(component_id="alc_scat",component_property="figure"),
    dash.Input(component_id='alc_scat_qeust',component_property="value"),
    dash.Input(component_id='alc_scat_year',component_property="value"),
    dash.Input(component_id='alc_scat_metric',component_property="value")
)
def plot_life_expectancy_alcohol_binge_freqq(question,year,metric):
    merged_data = dh.alcohol(question, year,metric)
        
        # Create scatter plot
    fig = px.scatter(merged_data, x='datavalue', y='rate', color='locationdesc',
                        labels={'datavalue': metric, 'rate': 'Average Life Expectancy'},
                        title=f'Life Expectancy vs {metric} of {question} (Year {year})')
    return fig
    

@dash.callback(
    dash.Output(component_id="smoke_scat",component_property="figure"),
    dash.Input(component_id='smoke_scat_qeust',component_property="value"),
    dash.Input(component_id='smoke_scat_year',component_property="value"),
    dash.Input(component_id='smoke_scat_metric',component_property="value")
)
def smoking_scat(question,year,metric):
    merged_data = dh.smoking(question, year,metric)
        
        # Create scatter plot
    fig = px.scatter(merged_data, x='datavalue', y='rate', color='locationdesc',
                        labels={'datavalue': metric, 'rate': 'Average Life Expectancy'},
                        title=f'Life Expectancy vs {metric} of {question} (Year {year})')
    return fig
    

@dash.callback(
    dash.Output(component_id="stress_scat",component_property="figure"),
    dash.Input(component_id='stress_scat_qeust',component_property="value"),
    dash.Input(component_id='stress_scat_year',component_property="value"),
    dash.Input(component_id='stress_scat_metric',component_property="value")
)
def stress_scat(question,year,metric):
    merged_data = dh.stress(question, year,metric)
        
        # Create scatter plot
    fig = px.scatter(merged_data, x='datavalue', y='rate', color='locationdesc',
                        labels={'datavalue': metric, 'rate': 'Average Life Expectancy'},
                        title=f'Life Expectancy vs {metric} of {question} (Year {year})')
    return fig
    
if __name__=="__main__":
    location_plot()
