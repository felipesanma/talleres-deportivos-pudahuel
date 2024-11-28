import streamlit as st
import pandas as pd


file_path = 'PUDAHUEL_TALLERES_DEPORTIVOS_PRIMAVERA_VERANO_2024.xlsx'
data = pd.read_excel(file_path)


data.columns = ['Taller', 'Dias', 'Horario', 'Ubicacion', 'Monitor']
data = data.drop_duplicates().apply(lambda x: x.str.strip() if x.dtype == "object" else x)


st.title("Talleres Deportivos Pudahuel - Primavera/Verano 2024")
st.sidebar.header("Filtros de búsqueda")


selected_dias = st.sidebar.multiselect("Selecciona días", options=data['Dias'].unique(), default=None)
selected_taller = st.sidebar.text_input("Taller (ejemplo: 'Futbol')", value="", max_chars=50)

filtered_data = data.copy()

if selected_dias:
    filtered_data = filtered_data[filtered_data['Dias'].isin(selected_dias)]

if selected_taller:
    filtered_data = filtered_data[filtered_data['Taller'].str.contains(selected_taller, case=False, na=False)]


# Mostrar los resultados
st.write(f"### Resultados: {len(filtered_data)} talleres encontrados")
st.dataframe(filtered_data)

# Opción para descargar los resultados
csv = filtered_data.to_csv(index=False)
st.sidebar.markdown("### Descargar resultados")
st.sidebar.download_button(
    label="Descargar en CSV",
    data=csv,
    file_name="talleres_filtrados.csv",
    mime="text/csv",
)