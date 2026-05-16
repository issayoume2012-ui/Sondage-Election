import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==================================================
# CONFIGURATION EMAIL (CACHÉE)
# ==================================================
EMAIL_EXPEDITEUR = st.secrets["EMAIL_EXPEDITEUR"]
MOT_DE_PASSE_APP = st.secrets["MOT_DE_PASSE_APP"]
EMAIL_DESTINATAIRE = st.secrets["EMAIL_DESTINATAIRE"]

# ==================================================
# CONFIGURATION PAGE
# ==================================================
st.set_page_config(
    page_title="Sondage Présidentiel",
    page_icon="🗳️",
    layout="centered"
)

# ==================================================
# TITRE
# ==================================================
st.header("🗳️ Sondage pour les élections présidentielles")
st.subheader("Tous les votes comptent. Ta voix, ton vote.")

# ==================================================
# FORMULAIRE
# ==================================================
nom = st.text_input(
    "Veuillez donner votre Prénom et Nom"
)

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

electeur = st.checkbox(
    "Électeur Éligible"
)

candidat = st.selectbox(
    "Quel candidat voteras-tu ?",
    [
        "",
        "Moussa Diagne",
        "Samba Ba",
        "ALD"
    ]
)

raison = st.text_area(
    "Pourquoi ce candidat ?"
)

st.info("Merci pour votre vote")

# ==================================================
# FONCTION EMAIL
# ==================================================
def envoyer_email():

    sujet = "🗳️ Nouveau Vote Présidentiel"

    contenu = f"""
NOUVEAU VOTE REÇU

Nom : {nom}

Date de naissance : {date_naissance}

Travail : {travail}

Électeur éligible : {"Oui" if electeur else "Non"}

Candidat choisi : {candidat}

Pourquoi ce candidat :
{raison}
"""

    message = MIMEMultipart()
    message["From"] = EMAIL_EXPEDITEUR
    message["To"] = EMAIL_DESTINATAIRE
    message["Subject"] = sujet

    message.attach(
        MIMEText(contenu, "plain")
    )

    serveur = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    serveur.starttls()

    serveur.login(
        EMAIL_EXPEDITEUR,
        MOT_DE_PASSE_APP
    )

    serveur.send_message(message)

    serveur.quit()

# ==================================================
# ENVOYER
# ==================================================
if st.button("📨 Envoyer"):

    if nom.strip() == "":
        st.warning(
            "Veuillez entrer votre nom."
        )

    elif candidat == "":
        st.warning(
            "Veuillez choisir un candidat."
        )

    elif not electeur:
        st.error(
            "Vous devez être électeur éligible."
        )

    else:
        try:
            envoyer_email()

            st.success(
                "✅ Vote envoyé avec succès !"
            )

            st.balloons()

        except Exception as e:
            st.error(
                f"Erreur : {e}"
            )
