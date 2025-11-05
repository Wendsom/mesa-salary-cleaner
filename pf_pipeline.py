# pf_pipeline.py
import streamlit as st
# C'est le devoir final à déployer sur Streamlit
@st.cache_data
def nettoyer(valeur):
    if isinstance(valeur, (int, float)):
        if valeur != valeur:  # NaN
            return 0.0
        return float(valeur)
    return 0.0

@st.cache_data
def supprimer_doublons(liste):
    return list(dict.fromkeys(liste))

@st.cache_data
def normaliser(liste):
    if not liste:
        return []
    mini, maxi = min(liste), max(liste)
    if maxi - mini == 0:
        return [0.0] * len(liste)
    return [(x - mini) / (maxi - mini) for x in liste]

@st.cache_data
def pipeline_complet(donnees):
    nettoyees = list(map(nettoyer, donnees))
    sans_doublons = supprimer_doublons(nettoyees)
    return normaliser(sans_doublons)