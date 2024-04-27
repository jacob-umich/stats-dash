import sqlite3 as db
import pandas as pd
from SHOD_cleaning_data import state_mapping,us_states
class DataCacher():
    def __init__(self):
        self.data_dict = {}

    def cache_data(self,name,kwargs,df):
        entry = {"kwargs":kwargs,"df":df}
        if self.data_dict.get("name"):
            self.data_dict["name"].append(entry)
        else:
            self.data_dict["name"]=[entry]

    def check_cache_data(self,name,kwargs):

        calls = self.data_dict.get("name",[])

        for call in calls:
            matching = True
            for k,v in call.get("kwargs").items():
                if v != kwargs[k]:
                    matching=False
                    break
            if matching:
                return call.get("df")
        return False
cache = DataCacher()

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
        value_list+=f"'{v}',"
    value_list = value_list[:-1]
    value_list+=")"

    # this takes a while to run
    cdi = cache.check_cache_data("get_cdi_cond",{"features":features,"field":field,"accepted_values":accepted_values})

    if cdi is None:
        return cdi
    else:
        with db.connect("health.db") as con:
            cdi = pd.read_sql_query(f"select {features} from cdi", con)
        cdi = cdi[cdi[field].isin(accepted_values)]
        cache.cache_data("get_cdi_cond",{"features":features,"field":field,"accepted_values":accepted_values},cdi)
        return cdi

# loading this df once since it takes a while
df = get_cdi_cond(
    "topic, yearstart, datavaluetype,stratificationcategory1,locationdesc,datavalue,question,locationabbr,stratification1",
    'locationdesc',
    us_states
    )
def get_rates(question, year,topic):

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
  conditions = (df['topic'] == simple) & \
              (df['yearstart'] == int(year)) & \
              (df['question'] == question) & \
              (df['datavaluetype'] == 'Crude Prevalence') & \
              (df['stratificationcategory1'] == 'Overall')
  diabetes_simple = df.loc[conditions, ['locationabbr','datavalue']]
  return diabetes_simple

def disability_rates(question,year):
  return get_rates(question,year,"Disability")

def disability_simple(question, year):
    return get_simple(question,year,"Disability")

def diabetes_rates(question,year):
  return get_rates(question,year,"Diabetes")

def diabetes_simple(question,year):
    return get_simple(question,year,"Diabetes")

def get_high_low_life_data(year):
    with db.connect("health.db") as con:
        life_data = pd.read_sql_query(f"select * from le",con)
    life_data = life_data[life_data['year'] == year]
    life_data_low = life_data.sort_values(by='rate').nsmallest(5, 'rate')
    life_data_high = life_data.sort_values(by='rate').nlargest(5, 'rate')
    return life_data_low, life_data_high

def simple_life(year):
    with db.connect("health.db") as con:
        life_data = pd.read_sql_query(f"select rate,state from le where year={year}",con)
        life_data['state'] = life_data['state'].map({v: k for k, v in state_mapping.items()})
    return life_data

def get_all_le():
    with db.connect("health.db") as con:
        life_data = pd.read_sql_query(f"select rate,state,year from le",con)
        life_data['state'] = life_data['state'].map({v: k for k, v in state_mapping.items()})
    return life_data

def obesity(question, location):
    conditions = (df['topic'] == 'Nutrition, Physical Activity, and Weight Status') & \
                (df['datavaluetype'] == 'Crude Prevalence') & \
                (df['stratificationcategory1'] == 'Overall') & \
                (df['question']==question)
    data = df.loc[conditions, ['yearstart', 'datavalue']]
    return data

def get_simple(question,year):
  conditions = (df['Topic'] == 'Diabetes') & \
              (df['YearStart'] == int(year)) & \
              (df['Question'] == question) & \
              (df['DataValueType'] == 'Crude Prevalence') & \
              (df['StratificationCategory1'] == 'Overall')
  diabetes_simple = df.loc[conditions, ['LocationAbbr','DataValue']]
  return diabetes_simple

def obesity_rates(question):
    return obesity(question, 'US')

