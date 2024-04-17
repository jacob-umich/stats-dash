import pandas as pd
import sqlite3

def get_main():
    data = pd.read_csv("data/Chronic_Disease_Indicators.csv")
    return data



def analyze_data():
    data = get_main()
    
    print(data[data["Response"].notna()][["Question","Response"]])

    print(data[data["Question"]=="Food insecure in the past 12 months among households"][["YearStart","YearEnd","LocationAbbr","DataValueUnit","DataValueType","DataValue"]].sort_values("LocationAbbr").to_markdown())

    print(data[data["Question"]=="Food insecure in the past 12 months among households"][["LowConfidenceLimit","Stratification1","StratificationCategory1","Geolocation","LocationID","DataValue"]].to_markdown())

    with open("ques.md","wt") as f:
        data.groupby("Question").size().sort_values(ascending=False).reset_index().to_markdown(buf=f)


def get_columns():
    data = pd.read_csv("data/Chronic_Disease_Indicators.csv")
    urbanization_distr= pd.read_csv(r"data\district-urbanization-index-2022\district-urbanization-index-2022\urbanization-index-2022.csv")
    food_prices= pd.read_csv(
        r"data\P_Data_Extract_From_Food_Prices_for_Nutrition\da10887b-3e2b-49e8-809f-8db742ca986c_Series - Metadata.csv",
        nrows=35,
        encoding='latin-1'
    )
    nutrition= pd.read_csv(
        r"data\P_Data_Extract_From_Health_Nutrition_and_Population_Statistics\802df0ff-19ca-4cc4-a0b8-0ab1cac2e7ba_Series - Metadata.csv",
        nrows=471
    )
    human_capital= pd.read_csv(
        r"data\P_Data_Extract_From_Human_Capital_Index\c1812adb-bffe-4deb-b43c-93b7a0927372_Series - Metadata.csv",
        nrows=28,
        encoding='latin-1'
    )
    metro_grade= pd.read_csv(r"data\redlining\metro-grades.csv")
    sots_index= pd.read_csv(r"data\state-of-the-state\state-of-the-state\index.csv")
    sots_words= pd.read_csv(r"data\state-of-the-state\state-of-the-state\words.csv")
    urbanization_state= pd.read_csv(r"C:\Users\Jacob\classes\stats_dash\data\urbanization-index\urbanization-index\urbanization-state.csv")
    column_data = pd.DataFrame.from_dict(
        {
            "main":data.columns,
            "urbanization_dist":urbanization_distr.columns,
            "food_prices":food_prices.columns,
            "nutrition":nutrition.columns,
            "human_capital":human_capital.columns,
            "metro_grade":metro_grade.columns,
            "sots_index":sots_index.columns,
            "sots_words":sots_words.columns,
            "urbanization_state":urbanization_state.columns
        },
        orient="index"
    )

    with open("features.md","wt") as f:
        column_data.transpose().to_markdown(buf=f)

def clean_main():
    data = get_main()
    # remove id columns
    # remove response column because its empty
    out = data["Response"].isna().all()
    # remove data source because its irrelevant

    # remove alt data value because only 5 records have it filled
    out = data[ data["DataValue"].fillna(0)!=data["DataValueAlt"].fillna(0)][["Question","DataValue","DataValueAlt"]]

    
    # remove datafootnotesymbol because its one-to-one with footnote
    out = data[["DataValueFootnoteSymbol","DataValueFootnote"]].dropna()
    out = out.groupby(["DataValueFootnote","DataValueFootnoteSymbol"]).size()

    # Geolocation is the same for every state
    out = data["Geolocation"].unique()

    # out = data[(data["DataValue"].isna()) & (data["LocationAbbr"]=="VI") & (data["Question"]=="Binge drinking prevalence among high school students")]

    # if data value footnote is not present then datavalue is a number
    out =  data[(data["DataValueFootnote"].isna())]["DataValue"].isna().any()

    # some data value footnote are present when data value is present. these notes are mainly to advise caution or because no cases were reported
    out =  data[~(data["DataValueFootnote"].isna())&~(data["DataValue"].isna())]["DataValueFootnote"].unique()

    # vaping data says no data available even though it is. fixing this
    out =  data[~(data["DataValueFootnote"].isna())&~(data["DataValue"].isna())&(data["DataValueFootnote"]=="No data available")]

    data = data[~(data["DataValueFootnote"].isna())&~(data["DataValue"].isna())&(data["DataValueFootnote"]=="No data available")]
    with open("temp.md","wt") as f:
        out.to_markdown(buf=f)
    # print(out)

    data = data[[
        "YearStart",
        "YearEnd",
        "LocationAbbr",
        "LocationDesc",
        "Topic",
        "Question",
        "DataValueUnit",
        "DataValueType",
        "DataValue",
        "DataValueFootnote",
        "LowConfidenceLimit",
        "StratificationCategory1",
        "Stratification1",
        "StratificationCategory2",
        "Stratification2",
        "StratificationCategory3",
        "Stratification3",
    ]]


clean_main()