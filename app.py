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

# --------- GRÁFICO POR COMUNIDADES ---------
import plotly.graph_objects as go
import pandas as pd

st.markdown("---")
st.subheader("🍭 Evolución de Renta desde 2010 por Comunidad Autónoma")

# --- Diccionario de columnas base (euros) ---
columnas = {
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

# --- Año base y selector de año destino ---
anio_base = 2010
anio_destino = st.selectbox(
    "Selecciona el año a comparar con 2010:",
    sorted(df["Periodo"].unique()),
    index=len(df["Periodo"].unique()) - 1,
    key="anio_lollipop"
)

# --- Construir DataFrame con valores ---
datos = []
for comunidad, col in columnas.items():
    if col in df.columns:
        fila_base = df.loc[df["Periodo"] == anio_base, col]
        fila_dest = df.loc[df["Periodo"] == anio_destino, col]
        if not fila_base.empty and not fila_dest.empty:
            valor_base = fila_base.values[0]
            valor_actual = fila_dest.values[0]
            variacion = ((valor_actual - valor_base) / valor_base) * 100
            datos.append({
                "CCAA": comunidad,
                "Base": valor_base,
                "Actual": valor_actual,
                "Variación (%)": variacion
            })

df_lollipop = pd.DataFrame(datos).sort_values("Actual", ascending=True)

# --- Crear figura ---
fig = go.Figure()

for _, row in df_lollipop.iterrows():
    color_linea = "#2ecc71" if row["Variación (%)"] >= 0 else "#e74c3c"  # Verde o rojo
    fig.add_trace(go.Scatter(
        x=[row["Base"], row["Actual"]],
        y=[row["CCAA"], row["CCAA"]],
        mode="lines+text",
        line=dict(color=color_linea, width=3),
        text=[None, f"{row['Variación (%)']:.1f} %"],
        textposition="top center",
        textfont=dict(color=color_linea),
        hoverinfo="skip",
        showlegend=False
    ))

# --- Añadir puntos de inicio y fin ---
fig.add_trace(go.Scatter(
    x=df_lollipop["Base"],
    y=df_lollipop["CCAA"],
    mode="markers",
    marker=dict(size=10, color="lightgray"),
    name=f"{anio_base}",
    hovertemplate=f"<b>%{{y}}</b><br>{anio_base}: %{{x:,.0f}} €<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=df_lollipop["Actual"],
    y=df_lollipop["CCAA"],
    mode="markers",
    marker=dict(size=12, color="#00b4d8"),
    name=f"{anio_destino}",
    hovertemplate=f"<b>%{{y}}</b><br>{anio_destino}: %{{x:,.0f}} €<extra></extra>"
))

# --- Ajustes visuales ---
fig.update_layout(
    title=f"📍 Renta por Comunidad Autónoma: Comparación {anio_base} vs {anio_destino}",
    xaxis_title="Renta (€)",
    yaxis_title="",
    yaxis=dict(categoryorder="array", categoryarray=df_lollipop["CCAA"].tolist()),
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(color="white"),
    margin=dict(l=80, r=30, t=60, b=30),
    height=700,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)
