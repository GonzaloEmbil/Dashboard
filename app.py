import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard de Renta", layout="wide")

# Estilo global en negro
st.markdown("""
    <style>
    body, label, .css-1aumxhk, .stText, .stSelectbox, .stMultiSelect, .stMarkdown {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.title("📈 Renta Anual Neta Media por Grupo de Edad")

# Cargar datos
df = pd.read_csv('Rentas.csv', sep=';')

# Selector tipo de visualización
vista = st.selectbox(
    "Selecciona el tipo de visualización:",
    options=["Valores absolutos (€)", "Variación respecto a 2010 (%)"],
    index=0
)

# Columnas por grupo
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

# Dropdown para seleccionar grupos
seleccion = st.multiselect(
    "Selecciona los grupos de edad:",
    options=list(columnas_valores.keys()),
    default=list(columnas_valores.keys())
)

# Crear gráfico principal
fig = go.Figure()

# Configurar vista
if vista == "Valores absolutos (€)":
    columnas = columnas_valores
    yaxis_title = "Renta (€)"
    y_range = [8000, 18000]
    hover_format = "%{y:,.0f} €"
else:
    columnas = columnas_porcentaje
    yaxis_title = "Variación desde 2010 (%)"
    y_range = [80, 120]
    hover_format = "%{y:.1f} %"

# Añadir líneas al gráfico
for grupo in seleccion:
    col = columnas[grupo]
    color = colores[grupo]
    fig.add_trace(go.Scatter(
        x=df['Periodo'],
        y=df[col],
        mode='lines+markers',
        name=grupo,
        line=dict(color=color, width=2),
        hovertemplate=f"<b>{grupo}</b><br>Año: %{{x}}<br>Valor: {hover_format}<extra></extra>"
    ))

# Estilo del gráfico
fig.update_layout(
    title="📈 Renta Anual Neta Media por Grupo de Edad",
    xaxis=dict(title="Año", title_font=dict(color="black"), tickfont=dict(color="black"), showgrid=True, gridcolor="lightgray"),
    yaxis=dict(title=yaxis_title, title_font=dict(color="black"), tickfont=dict(color="black"), showgrid=True, gridcolor="lightgray", range=y_range),
    template="none",
    plot_bgcolor='#fafafa',
    paper_bgcolor='#ffffff',
    font=dict(family="Segoe UI", size=14, color="black"),
    legend=dict(orientation="h", y=-0.2, font=dict(color="black")),
    hovermode='x unified',
    height=550
)

# Mostrar gráfico principal
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# NUEVO GRÁFICO POR SEXO 👇
# ---------------------------

st.markdown("---")
st.subheader("👥 Renta Anual Neta Media por Sexo")

fig_sexo = go.Figure()

# Añadir barras para Hombres y Mujeres
fig_sexo.add_trace(go.Bar(
    x=df['Periodo'],
    y=df['RentaAnualNetaMediaHombres'],
    name="Hombres",
    marker_color='royalblue',
    hovertemplate="Año: %{x}<br>Hombres: %{y:,.0f} €<extra></extra>"
))

fig_sexo.add_trace(go.Bar(
    x=df['Periodo'],
    y=df['RentaAnualNetaMediaMujeres'],
    name="Mujeres",
    marker_color='tomato',
    hovertemplate="Año: %{x}<br>Mujeres: %{y:,.0f} €<extra></extra>"
))

# Estilo gráfico de barras
fig_sexo.update_layout(
    barmode='group',
    xaxis=dict(title="Año", title_font=dict(color="black"), tickfont=dict(color="black"), showgrid=True, gridcolor="lightgray"),
    yaxis=dict(title="Renta (€)", title_font=dict(color="black"), tickfont=dict(color="black"), showgrid=True, gridcolor="lightgray"),
    template="none",
    plot_bgcolor='#fafafa',
    paper_bgcolor='#ffffff',
    font=dict(family="Segoe UI", size=14, color="black"),
    legend=dict(orientation="h", y=-0.2, font=dict(color="black")),
    height=500
)

# Mostrar gráfico de sexo
st.plotly_chart(fig_sexo, use_container_width=True)
