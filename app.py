import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv('Rentas.csv', sep=';')

# Diccionario de columnas disponibles
columnas_lineas = {
    'Total': ('RentaAnualNetaMedia', 'yellowgreen', 3),
    '65 o más': ('RentaAnualNetaMedia65', 'magenta', 3),
    '45-64': ('RentaAnualNetaMedia45_64', 'red', 3),
    '30-44': ('RentaAnualNetaMedia30_44', 'blue', 3),
    '16-29': ('RentaAnualNetaMedia16_29', 'grey', 3)
}

# Sidebar con multiselección
seleccion = st.multiselect(
    "Selecciona los grupos de edad a mostrar:",
    options=list(columnas_lineas.keys()),
    default=list(columnas_lineas.keys())
)

# Crear gráfico
fig, ax = plt.subplots(figsize=(15, 10), facecolor='white')
ax.set_facecolor('#efe9e6')
ax.grid(alpha=1, linewidth=0.5, color='lightgrey', ls='--', zorder=0)

# Ejes
ax.set_ylim(8000, 18000)
ax.set_xlim(left=2010)
ax.set_xlim(right=2024)
ax.set_xlabel("Periodo")
ax.set_ylabel("Renta Anual Neta Media (€)")
ax.set_title("Evolución de la renta anual neta media por grupo de edad")

# Dibujar líneas seleccionadas
x = df['Periodo']
for grupo in seleccion:
    col, color, grosor = columnas_lineas[grupo]
    ax.plot(x, df[col], label=grupo, color=color, linewidth=grosor, zorder=5)

# Leyenda
if seleccion:
    ax.legend()
else:
    ax.text(0.5, 0.5, "Selecciona al menos una línea para mostrar", 
            horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

# Mostrar en Streamlit
st.pyplot(fig)
