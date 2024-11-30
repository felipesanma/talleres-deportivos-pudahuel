import streamlit as st
import pandas as pd
from PIL import Image
from geopy.distance import geodesic
from process_data import get_data
import folium
from streamlit_folium import st_folium
from folium import plugins

favicon = Image.open("favicon.ico")
st.set_page_config(
    page_title="Talleres Deportivos Pudahuel 2024",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="auto",
)


data = get_data()

st.title("Talleres Deportivos Pudahuel - Primavera/Verano 2024")
st.sidebar.header("Filtros de búsqueda")


st.sidebar.header("Busca talleres cercanos a ti")
st.sidebar.write("Selecciona tu ubicación directamente en el mapa.")


map_center = [-33.4561, -70.6486]
m = folium.Map(location=map_center, zoom_start=12)
marker_cluster = plugins.MarkerCluster().add_to(m)


for _, row in data.iterrows():
    if pd.notna(row['Coordenadas']):
        folium.Marker(
            location=row['Coordenadas'],
            popup=f"Taller: {row['Taller']}<br>Ubicación: {row['Ubicacion']}",
        ).add_to(marker_cluster)


map_data = st_folium(m, width=700, height=500)
user_coords = None

if map_data and map_data.get("last_clicked"):
    user_coords = (
        map_data["last_clicked"]["lat"],
        map_data["last_clicked"]["lng"],
    )
    st.sidebar.write(f"Ubicación seleccionada: {user_coords}")


selected_dias = st.sidebar.multiselect("Selecciona días", options=data['Dias'].unique(), default=None)
selected_taller = st.sidebar.text_input("Taller (ejemplo: 'Futbol')", value="", max_chars=50)


filtered_data = data.copy()
if selected_dias:
    filtered_data = filtered_data[filtered_data['Dias'].isin(selected_dias)]

if selected_taller:
    filtered_data = filtered_data[filtered_data['Taller'].str.contains(selected_taller, case=False, na=False)]


if user_coords:
    def calculate_distance(coords):
        if pd.notna(coords):
            return geodesic(user_coords, coords).kilometers
        return None

    filtered_data['Distancia (km)'] = filtered_data['Coordenadas'].apply(calculate_distance)
    filtered_data = filtered_data.sort_values('Distancia (km)').dropna(subset=['Distancia (km)'])

    m = folium.Map(location=user_coords, zoom_start=12)
    folium.Marker(
        location=user_coords, 
        icon=folium.Icon(color="red"), 
        popup="Tu ubicación seleccionada"
    ).add_to(m)

    marker_cluster = plugins.MarkerCluster().add_to(m)
    for _, row in filtered_data.iterrows():
        folium.Marker(
            location=row['Coordenadas'],
            popup=f"Taller: {row['Taller']}<br>Ubicación: {row['Ubicacion']}<br>Distancia: {row['Distancia (km)']:.2f} km",
        ).add_to(marker_cluster)


st.write(f"### Resultados: {len(filtered_data)} talleres encontrados")
st_folium(m, width=700, height=500)


st.dataframe(filtered_data[['Taller', 'Dias', 'Horario', 'Ubicacion', 'Monitor', 'Distancia (km)']])


csv = filtered_data.to_csv(index=False)
st.sidebar.markdown("### Descargar resultados")
st.sidebar.download_button(
    label="Descargar en CSV",
    data=csv,
    file_name="talleres_filtrados.csv",
    mime="text/csv",
)
