import streamlit as st
import pandas as pd
import os

# ==========================
# CONFIGURATION ADMIN
# ==========================
MOT_DE_PASSE_ADMIN = "monsecret123"  # change ce mot de passe

# ==========================
# TITRE
# ==========================
st.header("🗳️ Sondage pour les élections présidentielles")
st.subheader("Tous les votes comptent. Ta voix, ton vote.")

# ==========================
# FORMULAIRE DE VOTE
# ==========================
nom = st.text_input("Veuillez donner votre Prénom et Nom")

date_naissance = st.date_input(
    "Saisir ta date de naissance"
)

travail = st.selectbox(
    "Votre travail",
    [
        "",
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

st.info("Merci pour le vote")

# ==========================
# BOUTON ENVOYER
# ==========================
if st.button("Envoyer"):

    if nom == "" or candidat == "":
        st.warning(
            "Veuillez remplir le nom et choisir un candidat."
        )

    elif not electeur:
        st.error(
            "Vous devez être électeur éligible."
        )

    else:
        vote = {
            "Nom": nom,
            "Date de naissance": str(date_naissance),
            "Travail": travail,
            "Candidat": candidat,
            "Pourquoi": raison
        }

        df_vote = pd.DataFrame([vote])

        fichier = "votes.csv"

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

        st.success("✅ Vote envoyé avec succès !")

# ==========================
# ESPACE ADMIN (PRIVÉ)
# ==========================
st.divider()
st.subheader("🔒 Accès Administrateur")

mot_de_passe = st.text_input(
    "Entrer le mot de passe admin",
    type="password"
)

if mot_de_passe == MOT_DE_PASSE_ADMIN:

    st.success("Connexion administrateur réussie")

    if os.path.exists("votes.csv"):
        df = pd.read_csv("votes.csv")

        st.write("### 📋 Résultats des votes")
        st.dataframe(df)

        st.write("### 📊 Résultat du sondage")
        resultat = df["Candidat"].value_counts()
        st.bar_chart(resultat)

    else:
        st.info("Aucun vote enregistré.")

elif mot_de_passe != "":
    st.error("Mot de passe incorrect")
