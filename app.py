import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import io

# Cargar datos
df = pd.read_csv('Rentas.csv', sep=';')

# Conversión del campo 'Periodo' a datetime si es necesario
if not pd.api.types.is_datetime64_any_dtype(df['Periodo']):
    df['Periodo'] = pd.to_datetime(df['Periodo'], errors='coerce')

# Limpiar NaT si hubo problemas con fechas
df = df.dropna(subset=['Periodo'])

# Diccionario de columnas disponibles
columnas_lineas = {
    'Total': ('RentaAnualNetaMedia', 'yellowgreen', 5),
    '65 o más': ('RentaAnualNetaMedia65', 'magenta', 5),
    '45-64': ('RentaAnualNetaMedia45_64', 'red', 2.5),
    '30-44': ('RentaAnualNetaMedia30_44', 'blue', 2.5),
    '16-29': ('RentaAnualNetaMedia16_29', 'grey', 2.5)
}

# Sidebar
st.sidebar.title("Opciones")

# Selección de líneas
seleccion = st.sidebar.multiselect(
    "Selecciona los grupos de edad a mostrar:",
    options=list(columnas_lineas.keys()),
    default=list(columnas_lineas.keys())
)

# Filtro por rango de fechas
min_fecha = df['Periodo'].min()
max_fecha = df['Periodo'].max()

rango = st.sidebar.slider(
    "Selecciona el rango de fechas:",
    min_value=min_fecha,
    max_value=max_fecha,
    value=(min_fecha, max_fecha),
    format="YYYY-MM"
)

# Filtrar el DataFrame por fecha
df_filtrado = df[(df['Periodo'] >= rango[0]) & (df['Periodo'] <= rango[1])]

st.title("Evolución de la Renta Anual Neta Media por Grupo de Edad")

# Gráfico matplotlib para descarga
fig, ax = plt.subplots(figsize=(15, 10), facecolor='white')
ax.set_facecolor('#efe9e6')
ax.grid(alpha=1, linewidth=0.5, color='lightgrey', ls='--', zorder=0)
ax.set_ylim(8000, 18000)
ax.set_xlabel("Periodo")
ax.set_ylabel("Renta Anual Neta Media (€)")
ax.set_title("Renta por grupo de edad")

# Plot con matplotlib
for grupo in seleccion:
    col, color, grosor = columnas_lineas[grupo]
    ax.plot(df_filtrado['Periodo'], df_filtrado[col], label=grupo, color=color, linewidth=grosor, zorder=5)

if seleccion:
    ax.legend()
else:
    ax.text(0.5, 0.5, "Selecciona al menos una línea", horizontalalignment='center',
            verticalalignment='center', transform=ax.transAxes)

# Mostrar el gráfico en Streamlit
st.subheader("Gráfico estático (Matplotlib)")
st.pyplot(fig)

# -------------------------
# DESCARGA DE LA IMAGEN
# -------------------------
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
st.download_button(
    label="📥 Descargar gráfico como PNG",
    data=buf.getvalue(),
    file_name="renta_grupos_edad.png",
    mime="image/png"
)

# -------------------------
# GRÁFICO INTERACTIVO
# -------------------------
st.subheader("Gráfico interactivo (Plotly)")

fig_interactivo = go.Figure()

for grupo in seleccion:
    col, color, _ = columnas_lineas[grupo]
    fig_interactivo.add_trace(
        go.Scatter(
            x=df_filtrado['Periodo'],
            y=df_filtrado[col],
            mode='lines+markers',
            name=grupo,
            line=dict(color=color)
        )
    )

fig_interactivo.update_layout(
    plot_bgcolor='#efe9e6',
    paper_bgcolor='white',
    xaxis_title='Periodo',
    yaxis_title='Renta Anual Neta Media (€)',
    hovermode='x unified',
    height=600
)

st.plotly_chart(fig_interactivo, use_container_width=True)
