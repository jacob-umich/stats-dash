import data_handler as dh
import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
import pickle
from sklearn.svm import SVR

dt_params = [
    {
        "max_leaf_nodes":3,
        "max_depth":3,
        "min_samples_split":3
    },
    {
        "max_leaf_nodes":6,
        "max_depth":6,
        "min_samples_split":6
    },
    {
        "max_leaf_nodes":9,
        "max_depth":9,
        "min_samples_split":9
    },
]
svd_params = [
    {
        "max_leaf_nodes":3,
        "max_depth":3,
        "min_samples_split":3
    },
]




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

def train_regression(data):
    # linear regression model
    x = data[:, :-1]
    y = data[:, -1:]

    model = sk.linear_model.LinearRegression()
    model.fit(x, y)

    return model

def train_dt(training, max_leaf_nodes=None, max_depth=None, min_samples_split=2, random_state=None):
    X_train = training[:, :-1]  # assuming the last column is the target
    y_train = training[:, -1]

    model = DecisionTreeRegressor(
        max_leaf_nodes=max_leaf_nodes, 
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=random_state
    )

    model.fit(X_train, y_train)
    return model

def hyper_tune(data):
    results = {}
    for i,param in dt_params:
        model = train_dt(data,param)
        score = cross_val_score(model,data[:,0:-1],data[:,-1:],cv=10)
        results[f"dt_{i}"]=score.mean()

    model = get_linear(data)
    score = cross_val_score(model,data[:,0:-1],data[:,-1:],cv=10)
    results["linear_regression"] = score.mean()

    for i,param in svd_params:
        model = train_svd_model(data,param)
        score = cross_val_score(model,data[:,0:-1],data[:,-1:],cv=10)
        results[f"svd_{i}"]=score.mean()

    results = pd.Series(results)

    with open("text_scripts/hyper_tuning.md","w") as f:
        results.to_markdown(f)

def train_svm(training, kernel='rbf', C=1.0, epsilon=0.1):
    # Extract features and target variable from training data
    X_train = training[:, :-1]
    y_train = training[:, -1]
    
    # Initialize SVM model
    svm_model = SVR(kernel=kernel, C=C, epsilon=epsilon)
    
    # Train the SVM model
    svm_model.fit(X_train, y_train)
    
    return svm_model

if __name__=="__main__":
    train,test = get_data()
    model = train_dt(train)
    with open("model.pkl","wb") as f:
        pickle.dump(model,f)

if __name__=="__main__":
    train,test = get_data()
    model = train_svm(train)
    with open("model.pkl","wb") as f:
        pickle.dump(model,f)

if __name__ == "__main__":
    train, test = get_data()
    model = train_regression(train)
    results = model.predict(test[:, :-1])
    print(results)