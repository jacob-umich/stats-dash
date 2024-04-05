import pandas as pd

data = pd.read_csv("Chronic_Disease_Indicators.csv")

print(len(data.columns))

# print(data[data["Response"].notna()][["Question","Response"]])
with open("ques.md","wt") as f:
    data.groupby("Question").size().sort_values(ascending=False).reset_index().to_markdown(buf=f)


# print(data[data["Question"]=="Food insecure in the past 12 months among households"][["YearStart","YearEnd","LocationAbbr","DataValueUnit","DataValueType","DataValue"]].sort_values("LocationAbbr").to_markdown())

# print(data[data["Question"]=="Food insecure in the past 12 months among households"][["LowConfidenceLimit","Stratification1","StratificationCategory1","Geolocation","LocationID","DataValue"]].to_markdown())
