import pandas as pd

f = "data/raw/2018-1986.csv"
df = pd.read_csv(f, sep=",", encoding="utf-8")
municipalities = list(df["Település"])
years = []
for i in range(1986, 2019):
    years.append(str(i))


js = {}
for year in years:
    t = dict(zip(municipalities, [0]*len(municipalities)))
    js[year] = t

for idx, row in df.iterrows():
    municipality = row["Település"]
    for year in years:
        population_year = row[year]
        js[year][municipality] = population_year

with open("data/raw/municipalities.csv", "w") as f:
    h = ",".join(municipalities)
    h = "date," + h + "\n"
    f.write(h)
    for year in years:
        o = year
        for municipality in municipalities:
            population = str(js[year][municipality])
            o += "," + population
        o += "\n"
        f.write(o)
