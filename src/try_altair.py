from os.path import join

import icu
import altair as alt
import pandas as pd


f = "data/raw/municipalities.csv"
df = pd.read_csv(f, sep=",", encoding="utf-8")

municipalities = list(df.columns)[1:]
collator = icu.Collator.createInstance(icu.Locale('hu_HU.UTF-8'))
sorted(municipalities, key=collator.getSortKey)
options = []

# generate time series vizs
for municipality in municipalities:
    t = f"<option value=\"{municipality}\">{municipality}</option>"
    options.append(t)
    fname = join("charts", municipality + ".html")
    data = df[["date", municipality]]
    nearest = alt.selection(
        type="single", nearest=True, on="mouseover", fields=[municipality], empty="none"
    )
    line = (
        alt.Chart(data)
        .mark_line(interpolate="basis")
        .encode(x="date:Q", y=f"{municipality}:Q")
    )
    selectors = (
        alt.Chart(data)
        .mark_point()
        .encode(x="date:Q", opacity=alt.value(0),)
        .add_selection(nearest)
    )

    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    text = line.mark_text(align="left", dx=5, dy=-5).encode(
        text=alt.condition(nearest, f"{municipality}:Q", alt.value(" "))
    )

    # Draw a rule at the location of the selection
    rules = (
        alt.Chart(data)
        .mark_rule(color="gray")
        .encode(x="date:Q",)
        .transform_filter(nearest)
    )

    # Put the five layers into a chart and bind the data
    chart = alt.layer(line, selectors, points, rules, text).properties(
        width=600, height=300
    )

    chart.save(fname)

options = "\n".join(options)
menu_template = """
<form action="/action_page.php" method="get">
  <input list="browsers" name="browser">
  <datalist id="browsers">
    %s
  </datalist>
  <input type="submit">
</form>""" % options

with open("viz/menu_template.html", "w") as f:
    f.write(menu_template)
