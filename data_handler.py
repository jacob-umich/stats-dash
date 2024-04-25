import sqlite3 as db
import pandas as pd



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