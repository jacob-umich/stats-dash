import sqlite3 as db
import pandas as pd
from SHOD_cleaning_data import state_mapping,us_states


def get_all_cdi():
    with db.connect("health.db") as con:
        cdi = pd.read_sql_query("select * from cdi", con)
    return cdi


def get_cdi_question(question):
    with db.connect("health.db") as con:
        cdi = pd.read_sql_query(f"select * from cdi where question = '{question}'", con)
    return cdi

def get_cdi_field(field):
    with db.connect("health.db") as con:
        cdi = pd.read_sql_query(f"select {field} from cdi", con)
    return cdi

def get_cdi_cond(features,field,accepted_values):
    value_list = "("
    for v in accepted_values:
        value_list+=f"{v},"
    value_list = value_list[:,-1]
    value_list+=")"
    with db.connect("health.db") as con:
        cdi = pd.read_sql_query(f"select {features} from cdi where {field} in {value_list}", con)
    return cdi


def get_rates(question, year,topic):
  df = get_cdi_cond(
      "topic, yearstart, datavaluetype,stratificationcategory1,locationdesc,datavalue,question",
      'locationdesc',
      us_states
    )
  
  conditions = (df['topic'] == topic) & \
              (df['yearstart'] == year) & \
              (df['datavaluetype'] == 'Crude Prevalence') & \
              (df['stratificationcategory1'] == 'Overall') & \
              (df['question']==question)
  data = df.loc[conditions, ['locationdesc','datavalue']]
  data_bad = data.sort_values(by='datavalue').nlargest(5, 'datavalue')
  data_good = data.sort_values(by='datavalue').nsmallest(5, 'datavalue')
  return data_bad, data_good

def get_simple(question,year,simple):
  df = get_cdi_cond('locationdesc',us_states)
  conditions = (df['topic'] == simple) & \
              (df['yearstart'] == year) & \
              (df['question'] == question) & \
              (df['datavaluetype'] == 'Crude Prevalence') & \
              (df['stratificationcategory1'] == 'Overall')
  diabetes_simple = df.loc[conditions, ['locationdesc','datavalue']]
  return diabetes_simple

def disability_rates(question,year):
  return get_rates(question,year,"Disability")

def disability_simple(year):
    return get_simple("*",year,"Disability")

def diabetes_rates(question,year):
  return get_rates(question,year,"Diabetes")

def diabetes_simple(year):
    return get_simple('Diabetes among adults',year,"Diabetes")

def get_high_low_life_data(year):
    with db.connect("health.db") as con:
        life_data = pd.read_sql_query(f"select * from le",con)
    life_data = life_data[life_data['year'] == year]
    life_data_low = life_data.sort_values(by='rate').nsmallest(5, 'rate')
    life_data_high = life_data.sort_values(by='rate').nlargest(5, 'rate')
    return life_data_low, life_data_high

def simple_life(year):
    with db.connect("health.db") as con:
        life_data = pd.read_sql_query(f"select rate from le where year={year}")
    return life_data