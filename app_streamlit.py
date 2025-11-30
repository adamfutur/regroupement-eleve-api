import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Groupement d'Élèves", page_icon="🎓", layout="centered")

st.title("🎓 Microservice de Groupement d'Élèves")
st.markdown("---")

# --- Section Configuration
st.subheader("⚙️ Configuration du groupement")
size = st.number_input("Taille du groupe (X)", min_value=1, value=5, step=1)

if st.button("Mettre à jour la taille X"):
    r = requests.put(f"{API_URL}/config", params={"size": size})
    if r.status_code == 200:
        st.success(f"Taille des groupes mise à jour à {size}")
    else:
        st.error("Erreur lors de la mise à jour.")

# --- Section Élèves
st.markdown("---")
st.subheader("👩‍🎓 Ajouter un élève")

with st.form("add_student"):
    name = st.text_input("Nom de l'élève")
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")
    submit = st.form_submit_button("Ajouter")

    if submit:
        r = requests.post(f"{API_URL}/students", json={"nom": name, "latitude": lat, "longitude": lon})
        if r.status_code == 200:
            st.success(f"Élève '{name}' ajouté !")
        else:
            st.error("Erreur lors de l'ajout de l'élève.")

# --- Section Groupement
st.markdown("---")
st.subheader("📦 Génération automatique des groupes")

if st.button("Générer les groupes automatiquement"):
    r = requests.post(f"{API_URL}/groups/generate")
    if r.status_code == 200:
        st.success("Groupes générés avec succès 🎉")
    else:
        st.error("Erreur lors de la génération.")

# --- Section Affichage
st.markdown("---")
st.subheader("📋 Liste des groupes")

r = requests.get(f"{API_URL}/groups")
if r.status_code == 200:
    groupes = r.json()
    for g in groupes:
        st.markdown(f"### 🧩 {g['nom']} (taille: {g['taille']})")
        if g["eleves"]:
            df = pd.DataFrame(g["eleves"])
            st.table(df[["nom", "latitude", "longitude"]])
        else:
            st.info("Aucun élève assigné à ce groupe.")
else:
    st.error("Impossible de récupérer les groupes.")
