import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import streamlit as st

data= pd.read_csv("municipio.csv")
gdf= gpd.read_parquet("Municipio.parquet")

st.title("Municipios")

munis = data ['entidad'].unique().tolist()
mun=st.selectbox ("seleccione un municipio:",munis)
filtro = data[data['entidad'] == mun]


#st.dataframe(filtro)
gen=( filtro.groupby ('clas_gen')['total_recaudo'].sum())

total_gen = gen.sum()
gen = (gen/ total_gen).round(2)

det= (filtro.groupby ('clasificacion_ofpuj') ['total_recaudo'].sum())
total_det = det.sum()
det= (det/ total_det).round(3)


color_palette = ["#e67e9c", "#8e44ad", "#c05b81", "#a267b2", "#d988b4", "#7b2447"]
# Pie chart
fig1 = px.pie(
    names=gen.index,
    values=gen.values,
    title="Distribución general",
    color_discrete_sequence=color_palette,
    width=800,   # ancho
    height=600   # alto
)
st.plotly_chart(fig1, use_container_width=True)  # ocupa todo el ancho del contenedor

# Treemap
fin = (filtro.groupby(['clas_gen', 'clasificacion_ofpuj'])['total_recaudo'].sum().reset_index())

fig = px.treemap(
    fin,
    path=[px.Constant("Total"), 'clas_gen', 'clasificacion_ofpuj'],
    values='total_recaudo',
    color_discrete_sequence=color_palette,
    width=1000,  # más ancho
    height=700   # más alto
)
st.plotly_chart(fig, use_container_width=True)
# mapa filtrado
filtro2 = gdf[gdf['entidad'] == mun][["codigo_alt","geometry"]]

fig, ax = plt.subplots(1, 1, figsize=(6, 6), facecolor="none")

# dibujar el polígono
filtro2.plot(ax=ax, color='#FFB6C1', edgecolor="black")

# quitar fondo y ejes
ax.set_axis_off()
ax.set_facecolor("none")   # fondo de los ejes transparente
fig.patch.set_alpha(0)     # fondo de la figura transparente

st.pyplot(fig)