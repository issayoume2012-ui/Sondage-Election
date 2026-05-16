import streamlit as st
import smtplib
from email.mime.text import MIMEText

# Seulement le destinataire visible
EMAIL_DESTINATAIRE = "issayoume2012@gmail.com"

st.title("🗳️ Sondage Présidentiel")
st.subheader("Tous les votes comptent")

nom = st.text_input("Prénom et Nom")
date_naissance = st.date_input("Date de naissance")

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

electeur = st.checkbox("Électeur Éligible")

candidat = st.selectbox(
    "Quel candidat voteras-tu ?",
    ["", "Moussa Diagne", "Samba Ba", "ALD"]
)

raison = st.text_area(
    "Pourquoi ce candidat ?"
)

if st.button("Envoyer"):

    if nom == "" or candidat == "":
        st.warning(
            "Veuillez remplir les champs."
        )

    elif not electeur:
        st.error(
            "Vous devez être électeur éligible."
        )

    else:
        try:
            # Email caché dans secrets
            email_expediteur = st.secrets["EMAIL"]
            mot_de_passe = st.secrets["PASSWORD"]

            message = f"""
Nouveau vote reçu

Nom : {nom}
Date de naissance : {date_naissance}
Travail : {travail}

Candidat : {candidat}

Pourquoi :
{raison}
"""

            msg = MIMEText(message)
            msg["Subject"] = "🗳️ Nouveau Vote"
            msg["From"] = email_expediteur
            msg["To"] = EMAIL_DESTINATAIRE

            serveur = smtplib.SMTP(
                "smtp.gmail.com",
                587
            )

            serveur.starttls()

            serveur.login(
                email_expediteur,
                mot_de_passe
            )

            serveur.send_message(msg)
            serveur.quit()

            st.success(
                "✅ Vote envoyé avec succès"
            )

        except Exception as e:
            st.error(f"Erreur : {e}")
