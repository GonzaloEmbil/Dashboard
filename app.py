import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard de Renta", layout="wide")

# Estilo global para texto negro
st.markdown("""
    <style>
    body, label, .css-1aumxhk, .stText, .stSelectbox, .stMultiSelect, .stMarkdown {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.title("📈 Renta Anual Neta Media")

# Cargar datos
df = pd.read_csv('Rentas.csv', sep=';')

# --- Selector para gráfico de grupos de edad ---
vista_edad = st.selectbox(
    "Selecciona el tipo de visualización para grupos de edad:",
    options=["Valores absolutos (€)", "Variación respecto a 2010 (%)"],
    index=0,
    key="vista_edad"
)

# Diccionarios columnas según vista
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

# Selección de grupos de edad
seleccion = st.multiselect(
    "Selecciona los grupos de edad:",
    options=list(columnas_valores.keys()),
    default=list(columnas_valores.keys())
)

# Asignar columnas según selección de vista
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

# Crear figura grupos de edad
fig_edad = go.Figure()

for grupo in seleccion:
    col = columnas[grupo]
    color = colores[grupo]
    fig_edad.add_trace(go.Scatter(
        x=df['Periodo'],
        y=df[col],
        mode='lines+markers',
        name=grupo,
        line=dict(color=color, width=2),
        hovertemplate=f"<b>{grupo}</b><br>Año: %{{x}}<br>Valor: {hover_fmt_edad}<extra></extra>"
    ))

fig_edad.update_layout(
    title="Renta anual neta media por grupos de edad",
    xaxis=dict(
        title="Año",
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showgrid=True,
        gridcolor="lightgray"
    ),
    yaxis=dict(
        title=yaxis_title_edad,
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showgrid=True,
        gridcolor="lightgray",
        range=y_range_edad if vista_edad != "Valores absolutos (€)" else None
    ),
    template="none",
    plot_bgcolor='#fafafa',
    paper_bgcolor='#ffffff',
    font=dict(family="Segoe UI", size=14, color="black"),
    legend=dict(
        orientation="h",
        y=-0.2,
        font=dict(color="black")
    ),
    hovermode='x unified',
    height=550
)

st.plotly_chart(fig_edad, use_container_width=True)

# --- Separador ---
st.markdown("---")
st.subheader("Renta anual neta media por sexo")

# Selector para gráfico por sexo
vista_sexo = st.selectbox(
    "Selecciona el tipo de visualización para sexo:",
    options=["Valores absolutos (€)", "Variación respecto a 2010 (%)"],
    index=0,
    key="vista_sexo"
)

# Columnas según vista para sexo
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

# Crear figura sexo
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
    title="Evolución de la renta por sexo",
    xaxis=dict(
        title="Año",
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showgrid=True,
        gridcolor="lightgray"
    ),
    yaxis=dict(
        title=yaxis_title_sexo,
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showgrid=True,
        gridcolor="lightgray",
        range=y_range_sexo if vista_sexo != "Valores absolutos (€)" else None
    ),
    template="none",
    plot_bgcolor='#fafafa',
    paper_bgcolor='#ffffff',
    font=dict(family="Segoe UI", size=14, color="black"),
    legend=dict(
        orientation="h",
        y=-0.2,
        font=dict(color="black")
    ),
    hovermode='x unified',
    height=500
)

st.plotly_chart(fig_sexo, use_container_width=True)
