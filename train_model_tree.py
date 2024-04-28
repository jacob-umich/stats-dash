import data_handler as dh
import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.tree import DecisionTreeRegressor 

def get_data():
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

    merged.loc[merged["sleep"].isna(),"sleep"]=merged['sleep'].mean()
    merged.dropna(inplace=True)
    data = merged[["obese","smoke","sleep","rate"]].to_numpy()
    np.random.shuffle(data)
    n_data = data.shape[0]
    print(data)
    train = data[0:int(n_data*0.8),:]
    test = data[int(n_data*0.8):,:]
    return train,test

def train_dt(training, max_leaf_nodes=None, max_depth=None, min_samples_split=2, random_state=None):
    X_train = training[:, :-1]  # assuming the last column is the target
    y_train = training[:, -1]
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, max_depth=max_depth,
                                  min_samples_split=min_samples_split, random_state=random_state)

    model.fit(X_train, y_train)
    return model

train_data, test_data = get_data()
model = train_dt(train_data, max_leaf_nodes=10, max_depth=5, random_state=42)

if __name__=="__main__":
    train,test = get_data()
    # print(train)
