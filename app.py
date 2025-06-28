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
st.title("Dashboard Interactivo para la Renta Anual Neta Media en España entre los años 2010 y 2024")

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

# --------- GRÁFICO POR COMUNIDADES ---------
import pandas as pd
import plotly.graph_objects as go

st.markdown("---")
st.subheader("🍭 Renta anual neta media por Comunidad Autónoma")

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

anio_base = 2010
anio_destino = st.selectbox(
    "Selecciona el año a comparar con 2010:",
    sorted(df["Periodo"].unique()),
    index=len(df["Periodo"].unique()) - 1,
    key="anio_lollipop"
)

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
                "Valor 2010": valor_base,
                f"Valor {anio_destino}": valor_actual,
                "Variación (%)": variacion
            })

df_lollipop = pd.DataFrame(datos).sort_values(f"Valor {anio_destino}", ascending=True)

fig = go.Figure()

for _, row in df_lollipop.iterrows():
    base = row["Valor 2010"]
    actual = row[f"Valor {anio_destino}"]
    variacion = row["Variación (%)"]
    color = "#2ecc71" if variacion >= 0 else "#e74c3c"
    x_center = (base + actual) / 2
    variacion_texto = f"{'+' if variacion > 0 else '-'}{abs(variacion):.1f} %"

    fig.add_trace(go.Scatter(
        x=[base, actual],
        y=[row["CCAA"], row["CCAA"]],
        mode="lines",
        line=dict(color=color, width=3),
        hoverinfo="skip",
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[x_center],
        y=[row["CCAA"]],
        mode="text",
        text=[variacion_texto],
        textposition="top center",
        textfont=dict(color=color, size=12),
        hoverinfo="skip",
        showlegend=False
    ))

fig.add_trace(go.Scatter(
    x=df_lollipop["Valor 2010"],
    y=df_lollipop["CCAA"],
    mode="markers",
    marker=dict(size=10, color="lightgray"),
    name="2010",
    hovertemplate="<b>%{y}</b><br>2010: %{x:,.0f} €<extra></extra>"
))
fig.add_trace(go.Scatter(
    x=df_lollipop[f"Valor {anio_destino}"],
    y=df_lollipop["CCAA"],
    mode="markers",
    marker=dict(size=12, color="#00b4d8"),
    name=str(anio_destino),
    hovertemplate=f"<b>%{{y}}</b><br>{anio_destino}: %{{x:,.0f}} €<extra></extra>"
))

fig.update_layout(
    title=f"🍭 Comparación de Renta por Comunidad Autónoma: 2010 vs {anio_destino}",
    xaxis_title="Renta (€)",
    yaxis=dict(categoryorder="array", categoryarray=df_lollipop["CCAA"].tolist()),
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(color="white"),
    margin=dict(l=80, r=30, t=60, b=30),
    height=700,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# 👉 Botón de descarga CSV por comunidades
csv_comunidades = df_lollipop.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Descargar CSV de comparación por CCAA",
    data=csv_comunidades,
    file_name=f"comparacion_renta_CCAA_2010_vs_{anio_destino}.csv",
    mime='text/csv'
)

# --------- GRÁFICO POR SEXO ---------
st.markdown("---")
st.subheader("👥 Evolución de la Brecha Salarial entre Hombres y Mujeres")

# Selector de vista
vista_sexo = st.selectbox(
    "Selecciona el tipo de visualización:",
    options=[
        "Diferencia entre hombres y mujeres (€)",
        "Variación en la diferencia respecto a 2010 (%)"
    ],
    index=0,
    key="vista_sexo"
)

fig_sexo = go.Figure()

if vista_sexo == "Diferencia entre hombres y mujeres (€)":
    y_col = "DiferenciaHombresMujeres"
    yaxis_title = "Diferencia (Hombres - Mujeres) en €"
    fill_color = 'rgba(147, 112, 219, 0.3)'  # púrpura semitransparente

    fig_sexo.add_trace(go.Scatter(
        x=df['Periodo'],
        y=df[y_col],
        mode='lines',
        name="Brecha salarial (€)",
        line=dict(color='mediumpurple', width=2),
        fill='tozeroy',
        fillcolor=fill_color,
        hovertemplate="Año: %{x}<br>Diferencia: %{y:,.0f} €<extra></extra>"
    ))

elif vista_sexo == "Variación en la diferencia respecto a 2010 (%)":
    y_col = "DiferenciaHombresMujeresBase2010"
    yaxis_title = "Variación de la brecha respecto a 2010 (%)"

    x_vals = df["Periodo"]
    # ✅ Convertir porcentaje en texto a float
    y_vals = pd.to_numeric(df[y_col].str.replace('%', ''), errors='coerce')

    y_mayor = [y if y >= 100 else None for y in y_vals]
    y_menor = [y if y < 100 else None for y in y_vals]

    # Área para valores ≥ 100% (verde)
    fig_sexo.add_trace(go.Scatter(
        x=x_vals,
        y=y_mayor,
        mode='lines',
        name="Brecha ↑",
        line=dict(color='limegreen', width=2),
        fill='tozeroy',
        fillcolor='rgba(50, 205, 50, 0.3)',
        hovertemplate="Año: %{x}<br>Variación: %{y:.1f} %<extra></extra>"
    ))

    # Área para valores < 100% (rojo)
    fig_sexo.add_trace(go.Scatter(
        x=x_vals,
        y=y_menor,
        mode='lines',
        name="Brecha ↓",
        line=dict(color='crimson', width=2),
        fill='tozeroy',
        fillcolor='rgba(220, 20, 60, 0.3)',
        hovertemplate="Año: %{x}<br>Variación: %{y:.1f} %<extra></extra>"
    ))

    # Línea horizontal de referencia en 100%
    fig_sexo.add_trace(go.Scatter(
        x=x_vals,
        y=[100] * len(x_vals),
        mode="lines",
        name="Referencia 100%",
        line=dict(color="gray", width=1, dash="dash"),
        hoverinfo="skip",
        showlegend=True
    ))

    # Anotación fija en el margen
    fig_sexo.add_annotation(
        xref="paper", x=1.005,
        y=100,
        xanchor="left",
        text="↔ Brecha igual que en 2010",
        showarrow=False,
        font=dict(color="gray", size=11)
    )

# Layout del gráfico
fig_sexo.update_layout(
    xaxis=dict(title="Año", title_font=dict(color="white"), tickfont=dict(color="white"),
               showgrid=True, gridcolor="gray"),
    yaxis=dict(title=yaxis_title, title_font=dict(color="white"), tickfont=dict(color="white"),
               showgrid=True, gridcolor="gray"),
    template="none",
    plot_bgcolor='#0e1117',
    paper_bgcolor='#0e1117',
    font=dict(color="white"),
    legend=dict(orientation="h", y=-0.2, font=dict(color="white")),
    hovermode='x unified',
    height=500
)

# Mostrar gráfico
st.plotly_chart(fig_sexo, use_container_width=True, config={
    "displayModeBar": True,
    "modeBarButtonsToRemove": [
        "zoom", "pan", "select", "zoomIn", "zoomOut", "autoScale", "resetScale"
    ],
    "displaylogo": False
})

# Botón de descarga CSV
df_descarga_sexo = df[["Periodo", y_col]]
csv_sexo = df_descarga_sexo.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Descargar CSV con los datos seleccionados",
    data=csv_sexo,
    file_name="brecha_salarial.csv",
    mime='text/csv'
)
