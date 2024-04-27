import data_handler as dh
import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.model_selection import cross_val_score

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

def hyper_tune(data):
    results = {}
    for i,param in dt_params:
        model = train_dt_model(data,param)
        score = cross_val_score(model,data[:,0:-1],data[:,-1:],cv=10)
        results[f"dt_{i}"]=score.mean()

    model = train_lr_model(data)
    score = cross_val_score(model,data[:,0:-1],data[:,-1:],cv=10)
    results["linear_regression"] = score.mean()

    for i,param in svd_params:
        model = train_svd_model(data,param)
        score = cross_val_score(model,data[:,0:-1],data[:,-1:],cv=10)
        results[f"svd_{i}"]=score.mean()

    results = pd.Series(results)
    
    with open("text_scripts/hyper_tuning.md","w") as f:
        results.to_markdown(f)


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

# linear regression model
X = test[:, :-1]
y = test[:, -1]

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)

mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

# evaluating linear regression model
print("Coefficients:", model.coef_)
print("\nIntercept:", model.intercept_)
print("\nMean Squared Error:", mse)
print("R-squared:", r2)

if __name__=="__main__":
    train,test = get_data()
    # print(train)
