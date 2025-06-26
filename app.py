import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard de Renta", layout="wide")

# Estilos para texto negro global
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

# Diccionario de columnas y colores por grupo
columnas_lineas = {
    'Total': ('RentaAnualNetaMedia', 'green'),
    '65 o más': ('RentaAnualNetaMedia65', 'purple'),
    '45-64': ('RentaAnualNetaMedia45_64', 'red'),
    '30-44': ('RentaAnualNetaMedia30_44', 'blue'),
    '16-29': ('RentaAnualNetaMedia16_29', 'gray')
}

# Menú desplegable con selección múltiple
seleccion = st.multiselect(
    "Selecciona los grupos de edad:",
    options=list(columnas_lineas.keys()),
    default=list(columnas_lineas.keys()),
    help="Puedes buscar y seleccionar uno o más grupos"
)

# Filtrar columnas seleccionadas
columnas_csv = ['Periodo'] + [columnas_lineas[grupo][0] for grupo in seleccion]
df_filtrado = df[columnas_csv]

# Crear gráfico interactivo con Plotly
fig = go.Figure()

for grupo in seleccion:
    col, color = columnas_lineas[grupo]
    fig.add_trace(go.Scatter(
        x=df['Periodo'],
        y=df[col],
        mode='lines+markers',
        name=grupo,
        line=dict(color=color, width=2),
        hovertemplate=f"<b>{grupo}</b><br>Año: %{{x}}<br>Renta: %{{y:,.0f}} €<extra></extra>"
    ))

# Configurar estilo del gráfico
fig.update_layout(
    title=dict(text="📈 Renta Anual Neta Media por Grupo de Edad", font=dict(color="black")),
    xaxis=dict(
        title="Año",
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showgrid=True,
        gridcolor="lightgray"
    ),
    yaxis=dict(
        title="Renta (€)",
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showgrid=True,
        gridcolor="lightgray",
        range=[8000, 18000]
    ),
    template="simple_white",
    plot_bgcolor='#fafafa',
    paper_bgcolor='#ffffff',
    font=dict(family="Segoe UI", size=14, color="black"),
    legend=dict(
        orientation="h",
        y=-0.2,
        font=dict(color="black")  # Leyenda en negro
    ),
    hovermode='x unified',
    height=550
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

# Botones de descarga
col1, col2 = st.columns(2)
with col1:
    csv = df_filtrado.to_csv(index=False, sep=';').encode('utf-8-sig')
    st.download_button("📄 Descargar datos como CSV", csv, file_name="datos_renta_media.csv", mime="text/csv")
with col2:
    st.markdown("💡 Clic derecho en el gráfico → *Guardar imagen como...*")
