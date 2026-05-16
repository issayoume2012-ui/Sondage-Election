import streamlit as st
import pandas as pd
import os

# Titre
st.header("🗳️ Sondage pour les élections présidentielles")
st.subheader("Tous les votes comptent. Ta voix, ton vote.")

# Formulaire
nom = st.text_input("Veuillez donner votre Prénom et Nom")

date_naissance = st.date_input(
    "Saisir ta date de naissance"
)

travail = st.selectbox(
    "Votre travail",
    [
        " ",
        "Fonctionnaire",
        "Étudiant",
        "Sans-emploi",
        "Ouvrier",
        "Retraité",
        "Autre"
    ]
)

st.info("Cochez si vous êtes électeur éligible")
electeur = st.checkbox("Électeur Éligible")

candidat = st.selectbox(
    "Quel candidat voteras-tu ?",
    [
        "",
        "Moussa Diagne",
        "Samba Ba",
        "ALD"
    ]
)

raison = st.text_area("Pourquoi ce candidat ?")

# Message info
st.info("Merci pour le vote")

# Bouton envoyer
if st.button("Envoyer"):

    # Vérification
    if nom == "" or candidat == "":
        st.warning(
            "Veuillez remplir le nom et choisir un candidat."
        )

    elif not electeur:
        st.error(
            "Vous devez être électeur éligible pour voter."
        )

    else:
        # Création des données
        vote = {
            "Nom": nom,
            "Date de naissance": str(date_naissance),
            "Travail": travail,
            "Électeur éligible": "Oui",
            "Candidat": candidat,
            "Pourquoi ce candidat": raison
        }

        df_vote = pd.DataFrame([vote])

        fichier = "votes.csv"

        # Sauvegarder dans CSV
        if os.path.exists(fichier):
            ancien_df = pd.read_csv(fichier)
            nouveau_df = pd.concat(
                [ancien_df, df_vote],
                ignore_index=True
            )
            nouveau_df.to_csv(
                fichier,
                index=False
            )
        else:
            df_vote.to_csv(
                fichier,
                index=False
            )

        # Confirmation
        st.success("✅ Vote envoyé avec succès !")

        # Résumé
        st.write("### Résumé du vote")
        st.write("**Nom :**", nom)
        st.write("**Date de naissance :**", date_naissance)
        st.write("**Travail :**", travail)
        st.write("**Candidat choisi :**", candidat)
        st.write("**Pourquoi :**", raison)

# Afficher les votes enregistrés
if os.path.exists("votes.csv"):
    st.write("### 📋 Votes enregistrés")
    df = pd.read_csv("votes.csv")
    st.dataframe(df)
