import pandas as pd
import math

def f(row, forEast):
    if row['FirstIsEast'] == forEast:
        val = row['Team1']
    else:
        val = row['Team2']
   
    floatVal = float(val)
    if math.isnan(floatVal):
        return -1
    return floatVal


tables_NBA = pd.read_html("https://en.wikipedia.org/wiki/NBA_All-Star_Game", match="Year")

data_frame = tables_NBA[0]

df = data_frame.dropna(how="any")
df = df.drop(columns="Game MVP")
df = df.drop(columns="Host arena")
df["Year"]= df["Year"].str[0:4].astype(int)
df["Host city"] = df["Host city"].str.split(",").str[0]
df["FirstIsEast"] = (df["Result"].str.split(",").str[0].str.contains("East")) | (df["Year"].eq(2018))

df = df.set_index("Year")

df["Team1"]=df["Result"].str.split(",").str[0]
df["Team2"]=df["Result"].str.split(",").str[1]
df = df.drop(columns="Result")
df["Team1"]=df["Team1"].str.findall("\d+").str[0]
df["Team2"]=df["Team2"].str.findall("\d+").str[0]

df["East"] = df.apply(f,forEast=True, axis=1)
df["West"] = df.apply(f,forEast=False, axis=1)

df = df.drop(columns="Team1")
df = df.drop(columns="Team2")
df = df.drop(columns="FirstIsEast")

df = df.drop(1999)

df["East"] = df["East"].astype(int)
df["West"] = df["West"].astype(int)

df["Difference"] = df["East"].sub(df["West"], axis=0)

groupedDf = df.groupby(["Difference"]).count()
groupedDf = groupedDf.drop(columns="Host city")
groupedDf = groupedDf.drop(columns="East")
groupedDf = groupedDf.rename(columns={"West": "Count"})
groupedDf = groupedDf.sort_values(by=['Difference'])

print(df)
print(f"shape: {df.shape}")

print(groupedDf)


filterDf = df.groupby("Host city").agg(["mean", "count"])
countBiggerThan1 = filterDf["East" , "count"] > 1

filterDf = filterDf[countBiggerThan1]
filterDf = filterDf.rename(columns={('East', 'mean'): 'East'})
filterDf = filterDf.drop(columns = ('East', 'count'))
filterDf = filterDf.drop(columns = ('West', 'count'))
filterDf = filterDf.drop(columns = ('Difference', 'mean'))
filterDf = filterDf.sort_values(by=[('Difference', 'count')])

print(filterDf)