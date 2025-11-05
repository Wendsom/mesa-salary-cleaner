# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pf_pipeline import pipeline_complet

st.title("MESA Salary Cleaner Pro")

tab1, tab2 = st.tabs(["Saisie manuelle", "Upload un fichier CSV ou un fichier XLSX"])

# --- TAB 1 : Saisie manuelle ---
with tab1:
    salaires_input = st.text_input(
        "Salaires (virgules)",
        value="2500, 2800, None, 'erreur', 2500"
    )
    # Cliquer sur le bouton : cas de la saisie manuelle

    if st.button("Lancer (manuel)"):
      
        # --- Nettoyage de la saisie ---
        cleaned_input = salaires_input.replace(" ", "")  # Supprime espaces
        
        # Liste convertie en une liste de chaine de caractères
        
        raw_list = cleaned_input.split(',')
        
        # --- Conversion sécurisée ---
        
        salaires = []
        for x in raw_list:
            if x == '' or x == 'None' or x == "'erreur'":
                salaires.append(None)
                continue
            try:
                salaires.append(float(x))
            except ValueError:
                salaires.append(None)  # Erreur → None

        # → pipeline_complet → affichage séparé + graphique
        # --- Affichage brut ---
        st.subheader("Données brutes (saisie)")
        st.write(salaires)

        # --- Pipeline PF ---
        with st.spinner("Nettoyage PF en cours..."):
            resultats = pipeline_complet(salaires)

        df = pd.DataFrame({
            "Brut": salaires,
        })

        df_result = pd.DataFrame({
            "Normalisé": resultats
        })

        # --- Résultats ---
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Avant / Après")
            st.dataframe(df)
            st.dataframe(df_result)

        with col2:
            st.subheader("Distribution")
            # Création de figure
            fig = px.histogram(df_result, x="Normalisé", title="Après normalisation")
            fig.update_traces(marker_line_width = 2,#épaisseur de la bordure en pixel
            marker_line_color = "black", marker_color="#63FA95")
            fig.update_xaxes(title_font_color = "red", title_font_size =20, tickfont_color = "yellow", tickfont_size = 15)
            fig.update_yaxes(title = "Effectifs",title_font_color = "blue", title_font_size = 20, tickfont_color= "green", tickfont_size = 15)
            # Le conteneur c'est la deuxième colonne
            st.plotly_chart(fig, use_container_width=True)

        st.success("Pipeline PF terminé ! Données prêtes pour l’analyse")

# --- TAB 2 : Upload CSV ---
with tab2:
    uploaded = st.file_uploader("CSV ou XLSX avec colonne 'salaire'", type=["csv","xlsx"])
    # Si variable uploaded n'est pas vide ie si elle contient le fichier uploaded
    if uploaded:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
            # Si le nom "salaire" correspond à celui de df
            if "salaire" in df.columns:
                # Alors convertire ce dataframe en liste en utilisant tolist()
                salaires = df["salaire"].tolist()
                resultats = pipeline_complet(salaires)
                # → affichage + graphique
                df_result = pd.DataFrame({"Normalisé": resultats})

                col1,col2 = st.columns(2)
                with col1 :
                    st.subheader("Avant et Après nettoyage")
                    st.dataframe(df)
                    st.dataframe(df_result)
                with col2 :
                    st.subheader("Distribution du salaire")
                    fig = px.histogram(df_result, x = "Normalisé", title = "Distribution après normalisation")
                    fig.update_traces(marker_line_width = 2,#épaisseur de la bordure en pixel
                    marker_line_color = "black", marker_color="#63FA95")
                    fig.update_xaxes(title_font_color = "red", title_font_size =20, tickfont_color = "yellow", tickfont_size = 15)
                    fig.update_yaxes(title = "Effectifs",title_font_color = "blue", title_font_size = 20, tickfont_color= "green", tickfont_size = 15)
                    # Le conteneur c'est la deuxième colonne
                    st.plotly_chart(fig, use_container_width=True)
                    st.success("Pipeline PF terminé ! Données prêtes pour l’analyse")
            else:
                st.error("Colonne 'salaire' manquante")
                st.info("Renommer la colonne en 'salaire'")
        elif uploaded.name.endswith(".xlsx") :
            df = pd.read_excel(uploaded)
# Si le nom "salaire" correspond à celui de df
            if "salaire" in df.columns:
                # Alors convertire ce dataframe en liste en utilisant tolist()
                salaires = df["salaire"].tolist()
                resultats = pipeline_complet(salaires)
                # → affichage + graphique
                df_result = pd.DataFrame({"Normalisé": resultats})

                col1,col2 = st.columns(2)
                with col1 :
                    st.subheader("Avant et Après nettoyage")
                    st.dataframe(df)
                    st.dataframe(df_result)
                with col2 :
                    st.subheader("Distribution du salaire")
                    fig = px.histogram(df_result, x = "Normalisé", title = "Distribution après normalisation")
                    fig.update_traces(marker_line_width = 2,#épaisseur de la bordure en pixel
                    marker_line_color = "black", marker_color="#63FA95")
                    fig.update_xaxes(title_font_color = "red", title_font_size =20, tickfont_color = "yellow", tickfont_size = 15)
                    fig.update_yaxes(title = "Effectifs",title_font_color = "blue", title_font_size = 20, tickfont_color= "green", tickfont_size = 15)
                    # Le conteneur c'est la deuxième colonne
                    st.plotly_chart(fig, use_container_width=True)
                    st.success("Pipeline PF terminé ! Données prêtes pour l’analyse")
            else:
                st.error("Colonne 'salaire' manquante")
                st.info("Renommer la colonne en 'salaire'")
        else :
            st.error("Fichier non pris en charge")
            st.info("Veuillez charger soit un fichier CSV ou XLSX avec colonne 'salaire'")