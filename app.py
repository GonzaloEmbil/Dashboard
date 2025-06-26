import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configurar la página
st.set_page_config(page_title="Dashboard de Renta", layout="wide")

# Título principal
st.title("📊 Evolución de la Renta Anual Neta Media")
st.markdown("Selecciona los grupos de edad que deseas visualizar y descarga los datos si lo necesitas.")

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

# Sidebar con filtros
with st.sidebar:
    st.header("⚙️ Filtros")
    seleccion = st.multiselect(
        "Grupos de edad:",
        options=list(columnas_lineas.keys()),
        default=list(columnas_lineas.keys())
    )
    st.markdown("---")
    st.write("Puedes descargar los datos en CSV al final.")

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
        line=dict(color=color, width=2),
        hovertemplate=
            f"<b>{grupo}</b><br>" +
            "Año: %{x}<br>" +
            "Renta: %{y:,.0f} €<extra></extra>"
    ))

# Configurar diseño del gráfico
fig.update_layout(
    title="📈 Renta Anual Neta Media por Grupo de Edad",
    xaxis_title="Año",
    yaxis_title="Renta (€)",
    template="simple_white",
    plot_bgcolor='#fafafa',
    paper_bgcolor='black',
    font=dict(family="Segoe UI", size=14, color="black"),
    legend=dict(orientation="h", y=-0.2),
    hovermode='x unified',
    height=550
)

# Ejes en color negro y con grilla clara
fig.update_xaxes(color="black", showgrid=True, gridcolor="lightgray")
fig.update_yaxes(color="black", showgrid=True, gridcolor="lightgray", range=[8000, 18000])

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)

# Botones de descarga
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
    st.markdown("💡 Puedes hacer clic derecho sobre el gráfico y elegir *'Guardar imagen como...'* para exportarlo como PNG.")
