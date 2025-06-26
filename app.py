import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración general del dashboard
st.set_page_config(page_title="Dashboard de Renta", layout="wide")

# Título principal
st.title("📊 Evolución de la Renta Anual Neta Media")
st.markdown("Selecciona los grupos de edad y exporta los datos si lo deseas.")

# Cargar datos
df = pd.read_csv('Rentas.csv', sep=';')

# Diccionario de columnas disponibles
columnas_lineas = {
    'Total': ('RentaAnualNetaMedia', 'green'),
    '65 o más': ('RentaAnualNetaMedia65', 'purple'),
    '45-64': ('RentaAnualNetaMedia45_64', 'red'),
    '30-44': ('RentaAnualNetaMedia30_44', 'blue'),
    '16-29': ('RentaAnualNetaMedia16_29', 'gray')
}

# Filtros en sidebar
with st.sidebar:
    st.header("⚙️ Filtros")
    seleccion = st.multiselect(
        "Grupos de edad:",
        options=list(columnas_lineas.keys()),
        default=list(columnas_lineas.keys())
    )
    
    st.markdown("---")
    st.write("Puedes descargar los datos o el gráfico al final.")

# Filtrar columnas para CSV
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
        line=dict(color=color, width=2)
    ))

# Personalización del gráfico
fig.update_layout(
    title="📈 Renta Anual Neta Media por Grupo de Edad",
    xaxis_title="Año",
    yaxis_title="Renta (€)",
    template="simple_white",
    plot_bgcolor='#fafafa',
    paper_bgcolor='#ffffff',
    font=dict(family="Segoe UI", size=14),
    legend=dict(orientation="h", y=-0.2),
    hovermode='x unified',
    height=550
)
fig.update_yaxes(range=[8000, 18000])

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)

# Botones de descarga organizados en columnas
col1, col2 = st.columns(2)

with col1:
    csv = df_filtrado.to_csv(index=False, sep=';').encode('utf-8-sig')
    st.download_button(
        label="📄 Descargar datos como CSV",
        data=csv,
        file_name='datos_renta_media.csv',
        mime='text/csv'
    )

with col2:
    st.markdown("💡 Puedes hacer clic derecho en el gráfico → *Guardar imagen como...* para exportarlo en PNG.")
