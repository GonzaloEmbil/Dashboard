import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Cargar datos
df = pd.read_csv('Rentas.csv', sep=';')

# Diccionario de columnas disponibles
columnas_lineas = {
    'Total': ('RentaAnualNetaMedia', 'yellowgreen'),
    '65 o más': ('RentaAnualNetaMedia65', 'magenta'),
    '45-64': ('RentaAnualNetaMedia45_64', 'red'),
    '30-44': ('RentaAnualNetaMedia30_44', 'blue'),
    '16-29': ('RentaAnualNetaMedia16_29', 'grey')
}

# Sidebar con selección
seleccion = st.multiselect(
    "Selecciona los grupos de edad a mostrar:",
    options=list(columnas_lineas.keys()),
    default=list(columnas_lineas.keys())
)

# Filtrar columnas seleccionadas
columnas_csv = ['Periodo'] + [columnas_lineas[grupo][0] for grupo in seleccion]
df_filtrado = df[columnas_csv]

# Crear gráfico interactivo
fig = go.Figure()
for grupo in seleccion:
    col, color = columnas_lineas[grupo]
    fig.add_trace(go.Scatter(
        x=df['Periodo'],
        y=df[col],
        mode='lines+markers',
        name=grupo,
        line=dict(color=color)
    ))

# Layout personalizado
fig.update_layout(
    title="Evolución de la renta anual neta media por grupo de edad",
    xaxis_title="Periodo",
    yaxis_title="Renta Anual Neta Media (€)",
    plot_bgcolor='#efe9e6',
    paper_bgcolor='white',
    hovermode='x unified',
    height=600
)
fig.update_yaxes(range=[8000, 18000])

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

# Botón para descargar CSV
csv = df_filtrado.to_csv(index=False, sep=';').encode('utf-8-sig')
st.download_button(
    label="📄 Descargar datos como CSV",
    data=csv,
    file_name='datos_renta_media.csv',
    mime='text/csv'
)
