import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración inicial
st.set_page_config(layout="wide", page_title="Dashboard Renta Anual Neta Media")
st.markdown("""
    <h1 style='text-align: center; color: white;'>Dashboard Interactivo para la Renta Anual Neta Media en España</h1>
""", unsafe_allow_html=True)

# Cargar datos
df = pd.read_csv('Rentas.csv', sep=';')

# Diccionarios de columnas por grupo de edad
columnas_edad_valor = {
    'Total': 'RentaAnualNetaMedia',
    '65 o más': 'RentaAnualNetaMedia65',
    '45-64': 'RentaAnualNetaMedia45_64',
    '30-44': 'RentaAnualNetaMedia30_44',
    '16-29': 'RentaAnualNetaMedia16_29'
}

columnas_edad_pct = {
    'Total': 'RentaAnualNetaMediaBase2010',
    '65 o más': 'RentaAnualNetaMedia65Base2010',
    '45-64': 'RentaAnualNetaMedia45_64Base2010',
    '30-44': 'RentaAnualNetaMedia30_44Base2010',
    '16-29': 'RentaAnualNetaMedia16_29Base2010'
}

colores = {
    'Total': 'yellowgreen',
    '65 o más': 'magenta',
    '45-64': 'red',
    '30-44': 'blue',
    '16-29': 'grey',
    'Hombres': 'dodgerblue',
    'Mujeres': 'lightcoral'
}

# Selección tipo visualización (euros o %)
st.markdown("""
    <h3 style='color:white;'>Selecciona el tipo de visualización:</h3>
""", unsafe_allow_html=True)
tipo_visualizacion_edad = st.selectbox("", ["Euros", "%"], key="edad_tipo")

# Selección de grupos de edad
st.markdown("""
    <h3 style='color:white;'>Selecciona los grupos de edad:</h3>
""", unsafe_allow_html=True)
grupos_seleccionados = st.multiselect("", list(columnas_edad_valor.keys()), default=list(columnas_edad_valor.keys()), key="grupos_edad")

# Subtítulo del gráfico
st.markdown("""
    <h2 style='color:white;'>Evolución de la Renta Anual Neta Media por Grupo de Edad</h2>
""", unsafe_allow_html=True)

# Crear gráfico de líneas por grupo de edad
fig_edad = go.Figure()

for grupo in grupos_seleccionados:
    col = columnas_edad_valor[grupo] if tipo_visualizacion_edad == "Euros" else columnas_edad_pct[grupo]
    fig_edad.add_trace(go.Scatter(
        x=df['Periodo'],
        y=df[col],
        mode='lines+markers',
        name=grupo,
        line=dict(color=colores[grupo], width=3),
        marker=dict(size=6),
        hovertemplate=f"<b>{grupo}</b><br>Año: %{{x}}<br>Renta: %{{y:,.0f}} {'€' if tipo_visualizacion_edad == 'Euros' else '%'}<extra></extra>"
    ))

fig_edad.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    xaxis=dict(title='Año', color='white'),
    yaxis=dict(title='Renta Anual Neta Media', color='white'),
    showlegend=True,
    legend=dict(font=dict(color='white')),
    margin=dict(l=40, r=20, t=40, b=40),
    modebar_remove=['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
)

st.plotly_chart(fig_edad, use_container_width=True)

# Datos para descargar (Edad)
cols_descarga = ["Periodo"] + [columnas_edad_valor[g] if tipo_visualizacion_edad == "Euros" else columnas_edad_pct[g] for g in grupos_seleccionados]
df_descarga_edad = df[cols_descarga]
csv_edad = df_descarga_edad.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Descargar CSV con los datos seleccionados",
    data=csv_edad,
    file_name="renta_por_edad.csv",
    mime='text/csv'
)

# Subtítulo del gráfico de sexo
st.markdown("""
    <h2 style='color:white;'>Evolución de la Renta Anual Neta Media por Sexo</h2>
""", unsafe_allow_html=True)

# Selección tipo visualización para sexo
st.markdown("""
    <h3 style='color:white;'>Selecciona el tipo de visualización:</h3>
""", unsafe_allow_html=True)
tipo_visualizacion_sexo = st.selectbox("", ["Euros", "%"], key="sexo_tipo")

# Crear gráfico de sexo
col_hombres = "RentaHombres" if tipo_visualizacion_sexo == "Euros" else "RentaHombresBase2010"
col_mujeres = "RentaMujeres" if tipo_visualizacion_sexo == "Euros" else "RentaMujeresBase2010"

fig_sexo = go.Figure()
fig_sexo.add_trace(go.Scatter(
    x=df['Periodo'],
    y=df[col_hombres],
    mode='lines+markers',
    name='Hombres',
    line=dict(color=colores['Hombres'], width=3),
    hovertemplate="<b>Hombres</b><br>Año: %{x}<br>Renta: %{y:,.0f} {}<extra></extra>".format('€' if tipo_visualizacion_sexo == 'Euros' else '%')
))
fig_sexo.add_trace(go.Scatter(
    x=df['Periodo'],
    y=df[col_mujeres],
    mode='lines+markers',
    name='Mujeres',
    line=dict(color=colores['Mujeres'], width=3),
    hovertemplate="<b>Mujeres</b><br>Año: %{x}<br>Renta: %{y:,.0f} {}<extra></extra>".format('€' if tipo_visualizacion_sexo == 'Euros' else '%')
))

fig_sexo.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    xaxis=dict(title='Año', color='white'),
    yaxis=dict(title='Renta Anual Neta Media', color='white'),
    showlegend=True,
    legend=dict(font=dict(color='white')),
    margin=dict(l=40, r=20, t=40, b=40),
    modebar_remove=['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
)

st.plotly_chart(fig_sexo, use_container_width=True)

# Botón descarga sexo
df_descarga_sexo = df[["Periodo", col_hombres, col_mujeres]]
csv_sexo = df_descarga_sexo.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Descargar CSV con los datos seleccionados",
    data=csv_sexo,
    file_name="renta_por_sexo.csv",
    mime='text/csv'
)
