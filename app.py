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

# --------- MAPA COROPLÉTICO CON GEOJSON CORREGIDO ---------
import plotly.express as px
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

# Diccionario de columnas con nombres normalizados para el GeoJSON
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
    "C. Valenciana": "RentaAnualNetaMediaComunidadvalenciana",
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

# GEOJSON CORREGIDO CON FORMATO ADECUADO
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        # Geometrías simplificadas pero con formato correcto
        {"type": "Feature", "properties": {"name": "Andalucía"}, "geometry": {"type": "Polygon", "coordinates": [[[-4.5,36.2],[-4.5,38.8],[-7.1,38.8],[-7.1,36.2],[-4.5,36.2]]]}},
        {"type": "Feature", "properties": {"name": "Aragón"}, "geometry": {"type": "Polygon", "coordinates": [[[-1.0,40.2],[-1.0,42.8],[0.5,42.8],[0.5,40.2],[-1.0,40.2]]]}},
        {"type": "Feature", "properties": {"name": "Asturias"}, "geometry": {"type": "Polygon", "coordinates": [[[-6.0,43.0],[-6.0,43.8],[-5.0,43.8],[-5.0,43.0],[-6.0,43.0]]]}},
        {"type": "Feature", "properties": {"name": "Baleares"}, "geometry": {"type": "Polygon", "coordinates": [[[1.5,38.5],[4.5,38.5],[4.5,40.0],[1.5,40.0],[1.5,38.5]]]}},
        {"type": "Feature", "properties": {"name": "Canarias"}, "geometry": {"type": "MultiPolygon", "coordinates": [
            [[[-15.6,28.1],[-15.6,28.8],[-16.3,28.8],[-16.3,28.1],[-15.6,28.1]]],  # Tenerife
            [[[-13.5,29.0],[-13.5,29.4],[-13.9,29.4],[-13.9,29.0],[-13.5,29.0]]]   # Gran Canaria
        ]}},
        {"type": "Feature", "properties": {"name": "Cantabria"}, "geometry": {"type": "Polygon", "coordinates": [[[-4.5,42.8],[-3.5,42.8],[-3.5,43.5],[-4.5,43.5],[-4.5,42.8]]]}},
        {"type": "Feature", "properties": {"name": "Castilla y León"}, "geometry": {"type": "Polygon", "coordinates": [[[-6.5,40.5],[-6.5,43.0],[-1.0,43.0],[-1.0,40.5],[-6.5,40.5]]]}},
        {"type": "Feature", "properties": {"name": "Castilla-La Mancha"}, "geometry": {"type": "Polygon", "coordinates": [[[-4.0,38.5],[-1.0,38.5],[-1.0,40.5],[-4.0,40.5],[-4.0,38.5]]]}},
        {"type": "Feature", "properties": {"name": "Cataluña"}, "geometry": {"type": "Polygon", "coordinates": [[[0.0,40.5],[3.5,40.5],[3.5,42.5],[0.0,42.5],[0.0,40.5]]]}},
        {"type": "Feature", "properties": {"name": "C. Valenciana"}, "geometry": {"type": "Polygon", "coordinates": [[[-1.0,38.0],[0.5,38.0],[0.5,40.5],[-1.0,40.5],[-1.0,38.0]]]}},
        {"type": "Feature", "properties": {"name": "Extremadura"}, "geometry": {"type": "Polygon", "coordinates": [[[-7.5,38.0],[-7.5,40.5],[-4.0,40.5],[-4.0,38.0],[-7.5,38.0]]]}},
        {"type": "Feature", "properties": {"name": "Galicia"}, "geometry": {"type": "Polygon", "coordinates": [[[-9.0,41.5],[-6.5,41.5],[-6.5,44.0],[-9.0,44.0],[-9.0,41.5]]]}},
        {"type": "Feature", "properties": {"name": "Madrid"}, "geometry": {"type": "Polygon", "coordinates": [[[-4.2,39.9],[-3.2,39.9],[-3.2,40.8],[-4.2,40.8],[-4.2,39.9]]]}},
        {"type": "Feature", "properties": {"name": "Murcia"}, "geometry": {"type": "Polygon", "coordinates": [[[-2.0,37.5],[-0.5,37.5],[-0.5,38.5],[-2.0,38.5],[-2.0,37.5]]]}},
        {"type": "Feature", "properties": {"name": "Navarra"}, "geometry": {"type": "Polygon", "coordinates": [[[-2.0,42.0],[-1.0,42.0],[-1.0,43.0],[-2.0,43.0],[-2.0,42.0]]]}},
        {"type": "Feature", "properties": {"name": "País Vasco"}, "geometry": {"type": "Polygon", "coordinates": [[[-3.0,42.5],[-1.5,42.5],[-1.5,43.5],[-3.0,43.5],[-3.0,42.5]]]}},
        {"type": "Feature", "properties": {"name": "La Rioja"}, "geometry": {"type": "Polygon", "coordinates": [[[-2.8,42.0],[-1.8,42.0],[-1.8,42.5],[-2.8,42.5],[-2.8,42.0]]]}},
        {"type": "Feature", "properties": {"name": "Ceuta"}, "geometry": {"type": "Point", "coordinates": [-5.3, 35.9]}},
        {"type": "Feature", "properties": {"name": "Melilla"}, "geometry": {"type": "Point", "coordinates": [-2.9, 35.3]}}
    ]
}

# Crear el mapa coroplético
try:
    fig = px.choropleth(
        datos_mapa,
        geojson=geojson_data,
        locations='Comunidad Autónoma',
        featureidkey='properties.name',
        color='Valor',
        color_continuous_scale='YlGnBu',
        range_color=(datos_mapa['Valor'].min() * 0.95, datos_mapa['Valor'].max() * 1.05),
        labels={'Valor': titulo_color},
        title=f"Renta Anual Neta Media - {año_seleccionado}"
    )
    
    # Configuración avanzada del mapa
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        center={"lat": 40.0, "lon": -4.0},
        projection_scale=5.5,
        showcountries=True,
        countrycolor="white",
        showsubunits=True,
        subunitcolor="rgba(255,255,255,0.5)",
        bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_layout(
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color="white", family="Arial"),
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_colorbar=dict(
            title=titulo_color,
            tickfont=dict(color="white"),
            title_font=dict(color="white", size=14),
            len=0.75
        ),
        height=600
    )
    
    fig.update_traces(
        hovertemplate="<b>%{location}</b><br>Valor: %{z:" + formato_hover + "}<extra></extra>",
        marker_line_width=0.5,
        marker_line_color="white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error creando el mapa: {str(e)}")
    
    # Mostrar datos en tabla como alternativa
    st.subheader("Datos por Comunidad Autónoma")
    st.dataframe(
        datos_mapa.style.format({"Valor": "{:,.0f} €" if tipo_valor == "Valores absolutos (€)" else "{:,.1f} %"}),
        height=400
    )

# Botón de descarga
csv_map = datos_mapa.copy()
csv_map.insert(0, "Año", año_seleccionado)
st.download_button(
    label="⬇️ Descargar datos completos",
    data=csv_map.to_csv(index=False).encode("utf-8"),
    file_name="renta_comunidades.csv",
    mime="text/csv"
)

# Notas explicativas
st.markdown("""
**Notas:**
- El mapa muestra los valores de renta neta anual media
- Las zonas más claras indican valores más altos
- Ceuta y Melilla se muestran como puntos
""")
