# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Configuration de la page
st.set_page_config(
    page_title="WellnessTrack - Analyse Santé",
    page_icon="📊",
    layout="wide"
)

# Titre et description
st.title("📊 WellnessTrack - Collecte et Analyse des Données de Santé")
st.markdown("*Application de suivi des habitudes de vie et analyse descriptive Built by Dimitri*")

# Initialisation du fichier de données
DATA_FILE = "wellness_data.csv"

def init_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "Date", "Nom", "Age", "Sexe", "Heures_Sommeil", 
            "Minutes_Sport", "Niveau_Stress", "Repas_Par_Jour",
            "Eau_Litres", "Humeur"
        ])
        df.to_csv(DATA_FILE, index=False)

def save_data(entry):
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

init_data()

# === SECTION COLLECTE DES DONNÉES ===
st.header("📝 Collecte de données")

with st.form("collecte_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        nom = st.text_input("Nom complet")
        age = st.slider("Âge", 15, 100, 30)
        sexe = st.selectbox("Sexe", ["Homme", "Femme", "Autre"])
        heures_sommeil = st.slider("Heures de sommeil par nuit", 0.0, 12.0, 7.0, 0.5)
        minutes_sport = st.slider("Minutes d'activité physique par jour", 0, 180, 30)
    
    with col2:
        niveau_stress = st.select_slider(
            "Niveau de stress (1=Faible, 5=Élevé)",
            options=[1, 2, 3, 4, 5], value=3
        )
        repas = st.number_input("Nombre de repas par jour", 1, 6, 3)
        eau_litres = st.slider("Consommation d'eau (litres)", 0.0, 5.0, 2.0, 0.1)
        humeur = st.select_slider(
            "Humeur générale (1=Très mauvais, 5=Excellent)",
            options=[1, 2, 3, 4, 5], value=3
        )
    
    submitted = st.form_submit_button("✅ Enregistrer les données")
    
    if submitted and nom:
        entry = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nom": nom,
            "Age": age,
            "Sexe": sexe,
            "Heures_Sommeil": heures_sommeil,
            "Minutes_Sport": minutes_sport,
            "Niveau_Stress": niveau_stress,
            "Repas_Par_Jour": repas,
            "Eau_Litres": eau_litres,
            "Humeur": humeur
        }
        save_data(entry)
        st.success(f"✅ Données enregistrées pour {nom} !")
        st.balloons()

# === SECTION ANALYSE DESCRIPTIVE ===
st.header("📈 Analyse descriptive des données")

df = pd.read_csv(DATA_FILE)

if len(df) > 0:
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Nombre de participants", len(df))
    with col2:
        st.metric("Âge moyen", f"{df['Age'].mean():.1f} ans")
    with col3:
        st.metric("Sommeil moyen", f"{df['Heures_Sommeil'].mean():.1f} h")
    with col4:
        st.metric("Sport moyen", f"{df['Minutes_Sport'].mean():.0f} min")
    
    # Onglets pour différentes analyses
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistiques descriptives", "📉 Visualisations", "🔍 Corrélations", "📋 Données brutes"])
    
    with tab1:
        st.subheader("Statistiques descriptives complètes")
        st.dataframe(df.describe(), use_container_width=True)
        
        # Stats par sexe
        st.subheader("Analyse par sexe")
        st.dataframe(df.groupby("Sexe").agg({
            "Heures_Sommeil": "mean",
            "Minutes_Sport": "mean",
            "Niveau_Stress": "mean",
            "Humeur": "mean"
        }).round(2), use_container_width=True)
    
    with tab2:
        st.subheader("Distribution des variables")
        
        # Sélection du graphique
        var_choice = st.selectbox(
            "Choisissez une variable à visualiser",
            ["Heures_Sommeil", "Minutes_Sport", "Niveau_Stress", "Humeur", "Age"]
        )
        
        fig = px.histogram(df, x=var_choice, title=f"Distribution de {var_choice}",
                           color_discrete_sequence=["#2E86AB"])
        st.plotly_chart(fig, use_container_width=True)
        
        # Boxplot par sexe
        fig2 = px.box(df, x="Sexe", y="Heures_Sommeil", title="Sommeil par sexe",
                      color="Sexe")
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        st.subheader("Matrice de corrélation")
        
        # Calcul des corrélations
        corr_matrix = df[["Age", "Heures_Sommeil", "Minutes_Sport", 
                          "Niveau_Stress", "Repas_Par_Jour", "Eau_Litres", "Humeur"]].corr()
        
        fig3 = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                         title="Corrélations entre variables")
        st.plotly_chart(fig3, use_container_width=True)
        
        st.info("💡 Interprétation : Plus la valeur est proche de 1 ou -1, plus la corrélation est forte.")
    
    with tab4:
        st.subheader("Données collectées")
        st.dataframe(df, use_container_width=True)
        
        # Export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger les données (CSV)", csv, "wellness_data.csv", "text/csv")
else:
    st.info("ℹ️ Aucune donnée collectée pour le moment. Utilisez le formulaire ci-dessus.")

# Pied de page
st.markdown("---")
st.markdown("*Application développée pour le TP INF232 EC2 - Collecte et analyse de données*")