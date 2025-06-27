import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard de Renta", layout="wide")

# Estilo global en modo oscuro
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    label, .stText, .stSelectbox, .stMultiSelect, .stMarkdown, .stDownloadButton, .stButton {
        color: white !important;
    }
    .css-1p05t8e, .css-10trblm {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.title("Dashboard Interactivo para la Renta Anual Neta Media en España")

# Cargar datos
df = pd.read_csv('Rentas.csv', sep=';')

# --------- GRÁFICO POR EDAD ---------
st.subheader("📈 Renta Anual Neta Media por Grupo de Edad")

vista_edad = st.selectbox(
    "Selecciona el tipo de visualización:",
    options=["Valores absolutos (€)", "Variación respecto a 2010 (%)"],
    index=0,
    key="vista_edad"
)

columnas_valores = {
    'Total': 'RentaAnualNetaMedia',
    '65 o más': 'RentaAnualNetaMedia65',
    '45-64': 'RentaAnualNetaMedia45_64',
    '30-44': 'RentaAnualNetaMedia30_44',
    '16-29': 'RentaAnualNetaMedia16_29'
}
columnas_porcentaje = {
    'Total': 'RentaAnualNetaMediaBase2010',
    '65 o más': 'RentaAnualNetaMedia65Base2010',
    '45-64': 'RentaAnualNetaMedia45_64Base2010',
    '30-44': 'RentaAnualNetaMedia30_44Base2010',
    '16-29': 'RentaAnualNetaMedia16_29Base2010'
}
colores = {
    'Total': 'green',
    '65 o más': 'purple',
    '45-64': 'red',
    '30-44': 'blue',
    '16-29': 'orange'
}

seleccion = st.multiselect(
    "Selecciona los grupos de edad:",
    options=list(columnas_valores.keys()),
    default=list(columnas_valores.keys())
)

if vista_edad == "Valores absolutos (€)":
    columnas = columnas_valores
    yaxis_title_edad = "Renta (€)"
    y_range_edad = [8000, 18000]
    hover_fmt_edad = "%{y:,.0f} €"
else:
    columnas = columnas_porcentaje
    yaxis_title_edad = "Variación desde 2010 (%)"
    y_range_edad = [80, 120]
    hover_fmt_edad = "%{y:.1f} %"

fig_edad = go.Figure()

for grupo in seleccion:
    col = columnas[grupo]
    fig_edad.add_trace(go.Scatter(
        x=df['Periodo'],
        y=df[col],
        mode='lines+markers',
        name=grupo,
        line=dict(color=colores[grupo], width=2),
        hovertemplate=f"<b>{grupo}</b><br>Año: %{{x}}<br>Valor: {hover_fmt_edad}<extra></extra>"
    ))

fig_edad.update_layout(
    xaxis=dict(title="Año", title_font=dict(color="white"), tickfont=dict(color="white"),
               showgrid=True, gridcolor="gray"),
    yaxis=dict(title=yaxis_title_edad, title_font=dict(color="white"), tickfont=dict(color="white"),
               showgrid=True, gridcolor="gray", range=y_range_edad if vista_edad != "Valores absolutos (€)" else None),
    template="none",
    plot_bgcolor='#0e1117',
    paper_bgcolor='#0e1117',
    font=dict(color="white"),
    legend=dict(orientation="h", y=-0.2, font=dict(color="white")),
    hovermode='x unified',
    height=550
)

st.plotly_chart(fig_edad, use_container_width=True, config={
    "displayModeBar": True,
    "modeBarButtonsToRemove": [
        "zoom", "pan", "select", "zoomIn", "zoomOut", "autoScale", "resetScale"
    ],
    "displaylogo": False
})

df_descarga_edad = df[['Periodo'] + [columnas[grupo] for grupo in seleccion]]
csv_edad = df_descarga_edad.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Descargar CSV con los datos seleccionados",
    data=csv_edad,
    file_name="renta_por_edad.csv",
    mime='text/csv'
)

# --------- GRÁFICO POR SEXO ---------
st.markdown("---")
st.subheader("👥 Renta Anual Neta Media por Sexo")

vista_sexo = st.selectbox(
    "Selecciona el tipo de visualización:",
    options=["Valores absolutos (€)", "Variación respecto a 2010 (%)"],
    index=0,
    key="vista_sexo"
)

if vista_sexo == "Valores absolutos (€)":
    hombres_col = 'RentaAnualNetaMediaHombres'
    mujeres_col = 'RentaAnualNetaMediaMujeres'
    yaxis_title_sexo = "Renta (€)"
    y_range_sexo = [8000, 18000]
    hover_h = "Hombres: %{y:,.0f} €"
    hover_m = "Mujeres: %{y:,.0f} €"
else:
    hombres_col = 'RentaAnualNetaMediaHombresBase2010'
    mujeres_col = 'RentaAnualNetaMediaMujeresBase2010'
    yaxis_title_sexo = "Variación desde 2010 (%)"
    y_range_sexo = [80, 120]
    hover_h = "Hombres: %{y:.1f} %"
    hover_m = "Mujeres: %{y:.1f} %"

fig_sexo = go.Figure()

fig_sexo.add_trace(go.Scatter(
    x=df['Periodo'],
    y=df[hombres_col],
    mode='lines+markers',
    name="Hombres",
    line=dict(color='royalblue', width=2),
    hovertemplate=f"Año: %{{x}}<br>{hover_h}<extra></extra>"
))
fig_sexo.add_trace(go.Scatter(
    x=df['Periodo'],
    y=df[mujeres_col],
    mode='lines+markers',
    name="Mujeres",
    line=dict(color='tomato', width=2),
    hovertemplate=f"Año: %{{x}}<br>{hover_m}<extra></extra>"
))

fig_sexo.update_layout(
    xaxis=dict(title="Año", title_font=dict(color="white"), tickfont=dict(color="white"),
               showgrid=True, gridcolor="gray"),
    yaxis=dict(title=yaxis_title_sexo, title_font=dict(color="white"), tickfont=dict(color="white"),
               showgrid=True, gridcolor="gray", range=y_range_sexo if vista_sexo != "Valores absolutos (€)" else None),
    template="none",
    plot_bgcolor='#0e1117',
    paper_bgcolor='#0e1117',
    font=dict(color="white"),
    legend=dict(orientation="h", y=-0.2, font=dict(color="white")),
    hovermode='x unified',
    height=500
)

st.plotly_chart(fig_sexo, use_container_width=True, config={
    "displayModeBar": True,
    "modeBarButtonsToRemove": [
        "zoom", "pan", "select", "zoomIn", "zoomOut", "autoScale", "resetScale"
    ],
    "displaylogo": False
})

df_descarga_sexo = df[['Periodo', hombres_col, mujeres_col]]
csv_sexo = df_descarga_sexo.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Descargar CSV con los datos seleccionados",
    data=csv_sexo,
    file_name="renta_por_sexo.csv",
    mime='text/csv'
)

# --------- MAPA COROPLÉTICO FUNCIONAL (sin Ceuta, Melilla, Canarias, Madrid, La Rioja, Navarra, Murcia) ---------
import json
import plotly.express as px

st.markdown("---")
st.subheader("🗺️ Mapa Interactivo de Renta por Comunidad Autónoma")

# --- Cargar GeoJSON con los límites de las CCAA ---
with open("ccaa_es.geojson", encoding="utf-8") as f:
    geojson = json.load(f)

# --- Diccionario para mapear columnas a nombres de CCAA ---
columnas_ccaa = {
    "Andalucía": "RentaAnualNetaMediaAndalucia",
    "Aragón": "RentaAnualNetaMediaAragon",
    "Principado de Asturias": "RentaAnualNetaMediaAsturias",
    "Illes Balears": "RentaAnualNetaMediaBaleares",
    "Cantabria": "RentaAnualNetaMediaCantabria",
    "Castilla y León": "RentaAnualNetaMediaCastillayleon",
    "Castilla-La Mancha": "RentaAnualNetaMediaCastillalamancha",
    "Cataluña": "RentaAnualNetaMediaCataluna",
    "Comunitat Valenciana": "RentaAnualNetaMediaComunidadvalenciana",
    "Extremadura": "RentaAnualNetaMediaExtremadura",
    "Galicia": "RentaAnualNetaMediaGalicia",
    "País Vasco": "RentaAnualNetaMediaPaisVasco",
    "Comunidad de Madrid": "RentaAnualNetaMediaMadrid",
    "Región de Murcia": "RentaAnualNetaMediaMurcia",
    "Comunidad Foral de Navarra": "RentaAnualNetaMediaNavarra",
    "La Rioja": "RentaAnualNetaMediaRioja",
    "Canarias": "RentaAnualNetaMediaCanarias"
}

# --- Selector de año ---
anio_mapa = st.selectbox(
    "Selecciona el año a visualizar en el mapa:",
    options=sorted(df['Periodo'].unique()),
    index=len(df['Periodo'].unique()) - 1,
    key="anio_mapa"
)

# --- Crear DataFrame para el mapa ---
df_mapa = pd.DataFrame({
    "CCAA": list(columnas_ccaa.keys()),
    "Renta": [df.loc[df['Periodo'] == anio_mapa, col].values[0] for col in columnas_ccaa.values()]
})

# --- Crear el mapa con Plotly Express ---
fig_mapa = px.choropleth(
    df_mapa,
    geojson=geojson,
    locations="CCAA",
    featureidkey="properties.name",
    color="Renta",
    color_continuous_scale="Viridis",
    labels={"Renta": "Renta (€)"},
    title=f"Renta Anual Neta Media por CCAA ({anio_mapa})"
)

# --- Personalización visual ---
fig_mapa.update_geos(fitbounds="locations", visible=False)
fig_mapa.update_layout(
    margin={"r":0, "t":50, "l":0, "b":0},
    paper_bgcolor='#0e1117',
    plot_bgcolor='#0e1117',
    font=dict(color="white")
)

st.plotly_chart(fig_mapa, use_container_width=True)
