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
import plotly.graph_objects as go

st.markdown("---")
st.subheader("🗺️ Mapa Coroplético de la Renta por Comunidad Autónoma")

tipo_valor = st.selectbox(
    "Tipo de dato:",
    options=["Valores absolutos (€)", "Variación respecto a 2010 (%)"],
    index=0,
    key="vista_mapa"
)

años_disponibles = sorted(df['Periodo'].unique())
año_seleccionado = st.selectbox(
    "Selecciona el año:",
    options=años_disponibles,
    index=años_disponibles.index(2024) if 2024 in años_disponibles else len(años_disponibles) - 1,
    key="año_mapa"
)

columnas_euro = {
    "Andalucía": "RentaAnualNetaMediaAndalucia",
    "Aragón": "RentaAnualNetaMediaAragon",
    "Asturias": "RentaAnualNetaMediaAsturias",
    "Baleares": "RentaAnualNetaMediaBaleares",
    "Cantabria": "RentaAnualNetaMediaCantabria",
    "Castilla y León": "RentaAnualNetaMediaCastillayleon",
    "Castilla-La Mancha": "RentaAnualNetaMediaCastillalamancha",
    "Cataluña": "RentaAnualNetaMediaCataluna",
    "Comunidad Valenciana": "RentaAnualNetaMediaComunidadvalenciana",
    "Extremadura": "RentaAnualNetaMediaExtremadura",
    "Galicia": "RentaAnualNetaMediaGalicia",
    "País Vasco": "RentaAnualNetaMediaPaisVasco"
}
columnas_pct = {k: v + "Base2010" for k, v in columnas_euro.items()}
columnas_usar = columnas_euro if tipo_valor == "Valores absolutos (€)" else columnas_pct
titulo_color = "Renta (€)" if tipo_valor == "Valores absolutos (€)" else "Índice (base 2010 = 100)"
formato_hover = ".0f" if tipo_valor == "Valores absolutos (€)" else ".1f"

df_año = df[df["Periodo"] == año_seleccionado].copy()
datos_mapa = pd.DataFrame({
    "Comunidad Autónoma": list(columnas_usar.keys()),
    "Valor": [df_año[col].values[0] if col in df_año.columns and not df_año[col].isnull().all() else None for col in columnas_usar.values()]
}).dropna(subset=['Valor'])

# GEOJSON limpio (solo comunidades sin problemas)
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "properties": {"name": "Andalucía"}, "geometry": {"type": "Polygon", "coordinates": [[[-7.5, 36.0], [-1.5, 36.0], [-1.5, 38.5], [-7.5, 38.5], [-7.5, 36.0]]]}},
        {"type": "Feature", "properties": {"name": "Aragón"}, "geometry": {"type": "Polygon", "coordinates": [[[-1.5, 40.0], [0.5, 40.0], [0.5, 42.5], [-1.5, 42.5], [-1.5, 40.0]]]}},
        {"type": "Feature", "properties": {"name": "Asturias"}, "geometry": {"type": "Polygon", "coordinates": [[[-6.5, 43.0], [-4.5, 43.0], [-4.5, 43.8], [-6.5, 43.8], [-6.5, 43.0]]]}},
        {"type": "Feature", "properties": {"name": "Baleares"}, "geometry": {"type": "Polygon", "coordinates": [[[1.5, 38.5], [4.5, 38.5], [4.5, 40.0], [1.5, 40.0], [1.5, 38.5]]]}},
        {"type": "Feature", "properties": {"name": "Cantabria"}, "geometry": {"type": "Polygon", "coordinates": [[[-4.5, 42.5], [-3.5, 42.5], [-3.5, 43.5], [-4.5, 43.5], [-4.5, 42.5]]]}},
        {"type": "Feature", "properties": {"name": "Castilla y León"}, "geometry": {"type": "Polygon", "coordinates": [[[-7.0, 40.0], [-1.0, 40.0], [-1.0, 43.0], [-7.0, 43.0], [-7.0, 40.0]]]}},
        {"type": "Feature", "properties": {"name": "Castilla-La Mancha"}, "geometry": {"type": "Polygon", "coordinates": [[[-4.5, 38.0], [-1.0, 38.0], [-1.0, 40.5], [-4.5, 40.5], [-4.5, 38.0]]]}},
        {"type": "Feature", "properties": {"name": "Cataluña"}, "geometry": {"type": "Polygon", "coordinates": [[[0.0, 40.0], [3.5, 40.0], [3.5, 42.5], [0.0, 42.5], [0.0, 40.0]]]}},
        {"type": "Feature", "properties": {"name": "Comunidad Valenciana"}, "geometry": {"type": "Polygon", "coordinates": [[[-1.0, 37.5], [0.5, 37.5], [0.5, 40.5], [-1.0, 40.5], [-1.0, 37.5]]]}},
        {"type": "Feature", "properties": {"name": "Extremadura"}, "geometry": {"type": "Polygon", "coordinates": [[[-7.5, 38.0], [-4.0, 38.0], [-4.0, 40.5], [-7.5, 40.5], [-7.5, 38.0]]]}},
        {"type": "Feature", "properties": {"name": "Galicia"}, "geometry": {"type": "Polygon", "coordinates": [[[-9.0, 41.5], [-6.5, 41.5], [-6.5, 44.0], [-9.0, 44.0], [-9.0, 41.5]]]}},
        {"type": "Feature", "properties": {"name": "País Vasco"}, "geometry": {"type": "Polygon", "coordinates": [[[-3.0, 42.5], [-1.5, 42.5], [-1.5, 43.5], [-3.0, 43.5], [-3.0, 42.5]]]}}
    ]
}

# Crear figura
min_val = datos_mapa['Valor'].min()
max_val = datos_mapa['Valor'].max()
rango = [min_val - 0.05*(max_val - min_val), max_val + 0.05*(max_val - min_val)]

fig = go.Figure(go.Choropleth(
    geojson=geojson_data,
    locations=datos_mapa['Comunidad Autónoma'],
    z=datos_mapa['Valor'],
    featureidkey="properties.name",
    colorscale='Viridis',
    marker_line_width=0.5,
    marker_line_color='white',
    zmin=rango[0],
    zmax=rango[1],
    hovertemplate="<b>%{location}</b><br>Valor: %{z:" + formato_hover + "}<extra></extra>",
    colorbar=dict(
        title=dict(text=titulo_color, font=dict(color="white")),
        tickfont=dict(color="white")
    )
))

fig.update_geos(
    fitbounds="locations",
    visible=False,
    showcountries=False,
    showland=False,
    showocean=False,
    bgcolor='rgba(0,0,0,0)'
)

fig.update_layout(
    title=dict(text=f"Renta Anual Neta Media - {año_seleccionado}", font=dict(color="white", size=20)),
    plot_bgcolor='#0e1117',
    paper_bgcolor='#0e1117',
    font=dict(color="white", family="Arial"),
    margin=dict(l=0, r=0, t=60, b=0),
    height=650
)

st.plotly_chart(fig, use_container_width=True)

# Botón de descarga
csv_map = datos_mapa.copy()
csv_map.insert(0, "Año", año_seleccionado)
st.download_button(
    label="⬇️ Descargar datos completos",
    data=csv_map.to_csv(index=False).encode("utf-8"),
    file_name="renta_comunidades.csv",
    mime="text/csv"
)
