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
    '16-29': 'gray'
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

# --------- MAPA COROPLÉTICO FUNCIONAL ---------
import plotly.express as px
import plotly.io as pio
import json

st.markdown("---")
st.subheader("🗺️ Mapa Coroplético de la Renta por Comunidad Autónoma")

# Selección de visualización
tipo_valor = st.selectbox(
    "Tipo de dato:",
    options=["Valores absolutos (€)", "Variación respecto a 2010 (%)"],
    index=0,
    key="vista_mapa"
)

# Obtener lista de años disponibles
años_disponibles = sorted(df['Periodo'].unique())
año_seleccionado = st.selectbox(
    "Selecciona el año:",
    options=años_disponibles,
    index=años_disponibles.index(2024) if 2024 in años_disponibles else len(años_disponibles) - 1,
    key="año_mapa"
)

# Diccionario de columnas con nombres normalizados
columnas_euro = {
    "Andalucía": "RentaAnualNetaMediaAndalucia",
    "Aragón": "RentaAnualNetaMediaAragon",
    "Asturias": "RentaAnualNetaMediaAsturias",
    "Baleares": "RentaAnualNetaMediaBaleares",
    "Canarias": "RentaAnualNetaMediaCanarias",
    "Cantabria": "RentaAnualNetaMediaCantabria",
    "Castilla y León": "RentaAnualNetaMediaCastillayleon",
    "Castilla-La Mancha": "RentaAnualNetaMediaCastillalamancha",
    "Cataluña": "RentaAnualNetaMediaCataluna",
    "Comunidad Valenciana": "RentaAnualNetaMediaComunidadvalenciana",
    "Extremadura": "RentaAnualNetaMediaExtremadura",
    "Galicia": "RentaAnualNetaMediaGalicia",
    "Madrid": "RentaAnualNetaMediaMadrid",
    "Murcia": "RentaAnualNetaMediaMurcia",
    "Navarra": "RentaAnualNetaMediaNavarra",
    "País Vasco": "RentaAnualNetaMediaPaisVasco",
    "La Rioja": "RentaAnualNetaMediaRioja",
    "Ceuta": "RentaAnualNetaMediaCeuta",
    "Melilla": "RentaAnualNetaMediaMelilla"
}

columnas_pct = {k: v + "Base2010" for k, v in columnas_euro.items()}
columnas_usar = columnas_euro if tipo_valor == "Valores absolutos (€)" else columnas_pct
titulo_color = "Renta (€)" if tipo_valor == "Valores absolutos (€)" else "Índice (base 2010 = 100)"
formato_hover = ".0f" if tipo_valor == "Valores absolutos (€)" else ".1f"

# Filtrar datos por año seleccionado
df_año = df[df["Periodo"] == año_seleccionado].copy()

# Crear datos para el mapa
datos_mapa = pd.DataFrame({
    "Comunidad Autónoma": list(columnas_usar.keys()),
    "Valor": [df_año[col].values[0] if col in df_año.columns and not df_año[col].isnull().all() 
             else None for col in columnas_usar.values()]
}).dropna(subset=['Valor'])

# Verificar si hay datos
if datos_mapa.empty:
    st.warning("⚠️ No hay datos disponibles para el año seleccionado. Por favor, elija otro año.")
    st.stop()

# GEOJSON CORREGIDO Y VERIFICADO
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "properties": {"name": "Andalucía"}, "geometry": {"type": "Polygon", "coordinates": [[[-7.5, 36.0], [-1.5, 36.0], [-1.5, 38.5], [-7.5, 38.5], [-7.5, 36.0]]]}},
        {"type": "Feature", "properties": {"name": "Aragón"}, "geometry": {"type": "Polygon", "coordinates": [[[-1.5, 40.0], [0.5, 40.0], [0.5, 42.5], [-1.5, 42.5], [-1.5, 40.0]]]}},
        {"type": "Feature", "properties": {"name": "Asturias"}, "geometry": {"type": "Polygon", "coordinates": [[[-6.5, 43.0], [-4.5, 43.0], [-4.5, 43.8], [-6.5, 43.8], [-6.5, 43.0]]]}},
        {"type": "Feature", "properties": {"name": "Baleares"}, "geometry": {"type": "Polygon", "coordinates": [[[1.5, 38.5], [4.5, 38.5], [4.5, 40.0], [1.5, 40.0], [1.5, 38.5]]]}},
        {"type": "Feature", "properties": {"name": "Canarias"}, "geometry": {"type": "Point", "coordinates": [-15.5, 28.0]}},
        {"type": "Feature", "properties": {"name": "Cantabria"}, "geometry": {"type": "Polygon", "coordinates": [[[-4.5, 42.5], [-3.5, 42.5], [-3.5, 43.5], [-4.5, 43.5], [-4.5, 42.5]]]}},
        {"type": "Feature", "properties": {"name": "Castilla y León"}, "geometry": {"type": "Polygon", "coordinates": [[[-7.0, 40.0], [-1.0, 40.0], [-1.0, 43.0], [-7.0, 43.0], [-7.0, 40.0]]]}},
        {"type": "Feature", "properties": {"name": "Castilla-La Mancha"}, "geometry": {"type": "Polygon", "coordinates": [[[-4.5, 38.0], [-1.0, 38.0], [-1.0, 40.5], [-4.5, 40.5], [-4.5, 38.0]]]}},
        {"type": "Feature", "properties": {"name": "Cataluña"}, "geometry": {"type": "Polygon", "coordinates": [[[0.0, 40.0], [3.5, 40.0], [3.5, 42.5], [0.0, 42.5], [0.0, 40.0]]]}},
        {"type": "Feature", "properties": {"name": "Comunidad Valenciana"}, "geometry": {"type": "Polygon", "coordinates": [[[-1.0, 37.5], [0.5, 37.5], [0.5, 40.5], [-1.0, 40.5], [-1.0, 37.5]]]}},
        {"type": "Feature", "properties": {"name": "Extremadura"}, "geometry": {"type": "Polygon", "coordinates": [[[-7.5, 38.0], [-4.0, 38.0], [-4.0, 40.5], [-7.5, 40.5], [-7.5, 38.0]]]}},
        {"type": "Feature", "properties": {"name": "Galicia"}, "geometry": {"type": "Polygon", "coordinates": [[[-9.0, 41.5], [-6.5, 41.5], [-6.5, 44.0], [-9.0, 44.0], [-9.0, 41.5]]]}},
        {"type": "Feature", "properties": {"name": "Madrid"}, "geometry": {"type": "Point", "coordinates": [-3.7, 40.4]}},
        {"type": "Feature", "properties": {"name": "Murcia"}, "geometry": {"type": "Point", "coordinates": [-1.1, 37.9]}},
        {"type": "Feature", "properties": {"name": "Navarra"}, "geometry": {"type": "Point", "coordinates": [-1.6, 42.8]}},
        {"type": "Feature", "properties": {"name": "País Vasco"}, "geometry": {"type": "Polygon", "coordinates": [[[-3.0, 42.5], [-1.5, 42.5], [-1.5, 43.5], [-3.0, 43.5], [-3.0, 42.5]]]}},
        {"type": "Feature", "properties": {"name": "La Rioja"}, "geometry": {"type": "Point", "coordinates": [-2.4, 42.4]}},
        {"type": "Feature", "properties": {"name": "Ceuta"}, "geometry": {"type": "Point", "coordinates": [-5.3, 35.9]}},
        {"type": "Feature", "properties": {"name": "Melilla"}, "geometry": {"type": "Point", "coordinates": [-2.9, 35.3]}}
    ]
}

# SOLUCIÓN DEFINITIVA CON PLOTLY EXPRESS
try:
    # Crear el mapa con plotly express
    fig = px.choropleth(
        datos_mapa,
        geojson=geojson_data,
        locations='Comunidad Autónoma',
        color='Valor',
        featureidkey='properties.name',
        color_continuous_scale='Viridis',
        range_color=(datos_mapa['Valor'].min(), datos_mapa['Valor'].max()),
        labels={'Valor': titulo_color},
        title=f"Renta Anual Neta Media - {año_seleccionado}"
    )
    
    # Configuración crítica del mapa
    fig.update_geos(
        visible=False,
        center=dict(lon=-4, lat=40),
        projection_type='mercator',
        projection_scale=5.5,
        lonaxis_range=[-10, 4.5],
        lataxis_range=[35, 44],
        fitbounds="locations"
    )
    
    # Configuración del layout
    fig.update_layout(
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color="white"),
        margin=dict(l=0, r=0, t=50, b=0),
        height=650,
        coloraxis_colorbar=dict(
            title=titulo_color,
            tickfont=dict(color="white"),
            title_font=dict(color="white")
        )
    )
    
    # Configurar hovertemplate
    fig.update_traces(
        hovertemplate="<b>%{location}</b><br>Valor: %{z:" + formato_hover + "}<extra></extra>"
    )
    
    # Forzar la vista inicial de España
    fig.update_geos(
        lataxis_range=[36, 44],  # Ajuste fino de latitud
        lonaxis_range=[-10, 5]    # Ajuste fino de longitud
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

except Exception as e:
    st.error(f"Error creando el mapa: {str(e)}")
    st.error("Por favor verifique los nombres de las comunidades en los datos y en el GeoJSON")
    
    # Mostrar datos para diagnóstico
    st.write("Datos del mapa:", datos_mapa)
    st.write("Nombres en GeoJSON:", [feature['properties']['name'] for feature in geojson_data['features']])
