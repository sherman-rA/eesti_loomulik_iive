import streamlit as st
import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import json

from io import StringIO

STATISTIKAAMETI_API_URL = "https://andmed.stat.ee/api/v1/et/stat/RV032"

JSON_PAYLOAD_STR =""" {
  "query": [
    {
      "code": "Aasta",
      "selection": {
        "filter": "item",
        "values": [
          "2014",
          "2015",
          "2016",
          "2017",
          "2018",
          "2019",
          "2020",
          "2021",
          "2022",
          "2023"
        ]
      }
    },
    {
      "code": "Maakond",
      "selection": {
        "filter": "item",
        "values": [
          "39",
          "44",
          "49",
          "51",
          "57",
          "59",
          "65",
          "67",
          "70",
          "74",
          "78",
          "82",
          "84",
          "86",
          "37"
        ]
      }
    },
    {
      "code": "Sugu",
      "selection": {
        "filter": "item",
        "values": [
          "2",
          "3"
        ]
      }
    }
  ],
  "response": {
    "format": "csv"
  }
}
"""

@st.cache_data
def import_data():
    headers = {"Content-Type": "application/json"}

    parsed_payload = json.loads(JSON_PAYLOAD_STR)

    response = requests.post(STATISTIKAAMETI_API_URL, json=parsed_payload, headers=headers)

    text = response.content.decode("utf-8-sig")
    df = pd.read_csv(StringIO(text))

    return df

st.title("Eesti loomulik iive.")
st.write("Kaart näitab loomulikku iivet Eesti maakondades valitud aastal.")

df = import_data()
#st.write(df.head())


geojson = "maakonnad.geojson"
gdf = gpd.read_file(geojson)
#st.write(gdf.head())

merged_data = gdf.merge(df, left_on="MNIMI", right_on="Maakond")
merged_data["Loomulik iive"] = (merged_data["Mehed Loomulik iive"] + merged_data["Naised Loomulik iive"])
#st.write(merged_data.head())


selected_year = st.sidebar.selectbox("Vali aasta:", sorted(merged_data["Aasta"].unique()))
year_data = merged_data[merged_data["Aasta"] == selected_year]


fig, ax = plt.subplots(figsize=(10,6))
year_data.plot(column="Loomulik iive", ax = ax, legend=True, cmap="coolwarm")
plt.title(f"Eesti loomulik iive {selected_year}")
plt.axis("off")

st.pyplot(fig)
