# WellnessTrack - Application d'Analyse de Données de Santé

Application Streamlit pour la collecte et l'analyse descriptive des habitudes de vie et données de santé.

## Fonctionnalités

- 📝 Collecte de données santé (sommeil, activité physique, stress, alimentation, humeur)
- 📊 Statistiques descriptives complètes
- 📉 Visualisations interactives (histogrammes, boxplots)
- 🔍 Matrice de corrélation entre variables
- 💾 Export des données au format CSV

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation et exécution

### 1. Cloner le dépôt

```bash(Terminal):
git clone https://github.com/Dimi-programmeur/WellnessTrack_Application.git
cd votre-depot

# CREER UN ENVIRONNEMENT VIRTUEL:

Sur Windows:

python -m venv venv
venv\Scripts\activate

Sur Linux:

python3 -m venv venv
source venv/bin/activate

# INSTALLER LES DEPENDANCES:

pip install streamlit pandas plotly    ou   pip install -r requirements.txt

## LANCER L'APPLICATION:

streamlit run app.py

