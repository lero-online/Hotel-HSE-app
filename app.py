import streamlit as st
import json
import os

# --------------------------
# Funktion zum Laden der JSON-Library
# --------------------------
@st.cache_data
def load_hse_library(file_path):
    """Lädt die HSE-Library aus der JSON-Datei."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# --------------------------
# App-Titel
# --------------------------
st.set_page_config(page_title="Hotel HSE App", layout="wide")
st.title("🏨 Hotel HSE Test-App")
st.write("Diese App zeigt Tätigkeiten und Gefährdungen für Hotels und Gaststätten.")

# --------------------------
# Bibliothek laden
# --------------------------
library_path = os.path.join("data", "hotel_hse_library.json")
hse_library = load_hse_library(library_path)
all_bereiche = list(hse_library["HotelGaststaetten_HSE_CompleteLibrary"].keys())

# --------------------------
# Bereich auswählen
# --------------------------
bereich = st.selectbox("Bereich auswählen", all_bereiche)
taetigkeiten = hse_library["HotelGaststaetten_HSE_CompleteLibrary"][bereich]

# --------------------------
# Suche nach Tätigkeit
# --------------------------
search_term = st.text_input("Suche nach Tätigkeit (optional)").lower()
filtered_taetigkeiten = [
    t for t in taetigkeiten if search_term in t["Tätigkeit"].lower()
] if search_term else taetigkeiten

taetigkeit_name = st.selectbox(
    "Tätigkeit auswählen",
    [t["Tätigkeit"] for t in filtered_taetigkeiten]
)

# --------------------------
# Gefährdungen filtern
# --------------------------
gefaehrdung_typen = ["Alle", "Physisch", "Chemisch", "Biologisch", "Psychisch", "Elektrisch"]
filter_typ = st.selectbox("Gefährdungstyp filtern", gefaehrdung_typen)

# --------------------------
# Gefährdungen anzeigen
# --------------------------
st.subheader("Gefährdungen:")

for t in filtered_taetigkeiten:
    if t["Tätigkeit"] == taetigkeit_name:
        gef_list = t["Gefährdungen"]
        if filter_typ != "Alle":
            gef_list = [g for g in gef_list if g["Typ"] == filter_typ]
        if gef_list:
            for g in gef_list:
                st.write(f"- {g['Gefährdung']} ({g['Typ']})")
        else:
            st.write("Keine Gefährdungen für diesen Typ gefunden.")

