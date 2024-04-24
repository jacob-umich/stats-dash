import sqlite3 as db
import pandas as pd

con = db.connect("health.db")


def get_all_cdi():
    cdi = pd.read_sql_query("select * from cdi", con)
    return cdi


def get_cdi_question(question):
    cdi = pd.read_sql_query(f"select * from cdi where question = '{question}'", con)
    return cdi
def get_cdi_field(field):
    cdi = pd.read_sql_query(f"select {field} from cdi", con)
    return cdi