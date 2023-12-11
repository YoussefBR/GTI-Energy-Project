import plotly.express as px
import pandas as pd

df = pd.read_csv("plumes_2017-01-01_2018-01-01.csv")

fig = px.scatter_geo(df,lat='plume_latitude',lon='plume_longitude', hover_name="plume_id")
fig.update_layout(title = 'World map', title_x=0.5)
fig.show()