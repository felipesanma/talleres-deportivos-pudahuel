import streamlit as st
from PIL import Image
from process_data import get_data

favicon = Image.open("favicon.ico")
st.set_page_config(
    page_title="Talleres Deportivos Pudahuel 2024",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="auto",
)

# Cargar los datos
data = get_data()

st.title("Talleres Deportivos Pudahuel - Primavera/Verano 2024")
st.sidebar.header("Filtros de búsqueda")

# Filtros en la barra lateral
selected_dias = st.sidebar.multiselect("Selecciona días", options=data['Dias'].unique(), default=None)
selected_taller = st.sidebar.text_input("Taller (ejemplo: 'Futbol')", value="", max_chars=50)

# Filtrar datos basados en filtros de taller y días
filtered_data = data.copy()
if selected_dias:
    filtered_data = filtered_data[filtered_data['Dias'].isin(selected_dias)]

if selected_taller:
    filtered_data = filtered_data[filtered_data['Taller'].str.contains(selected_taller, case=False, na=False)]


columns_to_display = ['Taller', 'Dias', 'Horario', 'Ubicacion', 'Monitor']

st.dataframe(filtered_data[columns_to_display])

# Opción para descargar los resultados
csv = filtered_data.to_csv(index=False)
st.sidebar.markdown("### Descargar resultados")
st.sidebar.download_button(
    label="Descargar en CSV",
    data=csv,
    file_name="talleres_filtrados.csv",
    mime="text/csv",
)
