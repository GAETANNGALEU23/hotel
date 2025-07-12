import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuration de la page
st.set_page_config(page_title="HOTEL LA SANTE", page_icon="🏨", layout="wide")

# Style CSS pour le fond bleu clair et autres éléments
st.markdown(
    """
    <style>
    .stApp {
        background-color: #e6f0ff;
    }
    .title {
        color: #003366;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        padding: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 80%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fonction pour initialiser ou charger le fichier Excel
def init_data():
    if not os.path.exists("reservations.xlsx"):
        df = pd.DataFrame(columns=[
            "Nom", "Prenom", "Telephone", "Ville", "Profession", 
            "CNI", "Prix_Chambre", "Nb_Jours", "Date_Arrivee", 
            "Montant_Total", "Date_Reservation"
        ])
        df.to_excel("RESERVATIONS.xlsx", index=False)
    else:
        df = pd.read_excel("RESERVATIONS.xlsx")
    return df

# Fonction pour sauvegarder les données
def save_data(df):
    df.to_excel("RESERVATIONS.xlsx", index=False)

# Fonction pour ajouter une réservation
def add_reservation(data):
    df = init_data()
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)

# Sidebar avec logo et fonctions supplémentaires
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>HOTEL LA SANTE</h1>", unsafe_allow_html=True)
    
    # Logo (remplacez par votre propre image)
    st.image("https://www.facebook.com/photo/?fbid=671851741719088&set=pb.100066828047627.-2207520000", caption="Logo Hotel", use_column_width=True)
    
    st.markdown("---")
    st.markdown("### Fonctions supplémentaires")
    
    # Afficher le nombre total de réservations
    if st.button("Voir statistiques"):
        df = init_data()
        total_reservations = len(df)
        total_revenus = df["Montant_Total"].sum() if "Montant_Total" in df.columns else 0
        st.info(f"Réservations totales: {total_reservations}")
        st.info(f"Revenus totaux: {total_revenus} FCFA")
    
    # Afficher les dernières réservations
    if st.button("Dernières réservations"):
        df = init_data()
        if not df.empty:
            st.dataframe(df.tail(5))
        else:
            st.warning("Aucune réservation enregistrée")

# Contenu principal de l'application
#st.markdown("<h1 class='title'>HOTEL LA SANTE</h1>", unsafe_allow_html=True)
#st.markdown("---")
st.markdown(
    """
    <div style="
        border: 2px solid #0099ff;
        background-color: #eaf6ff;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        ">
      <h1 style="margin: 0; color: #024a86;">HOTEL LA SANTE</h1>
      <hr style="border:1px solid #0099ff; width: 80%; margin-top: 10px;">
    </div>
    """,
    unsafe_allow_html=True
)



# Formulaire de réservation
with st.form("reservation_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        nom = st.text_input("Nom*", max_chars=50)
        prenom = st.text_input("Prénom*", max_chars=50)
        telephone = st.text_input("Téléphone*", max_chars=15)
        ville = st.text_input("Ville de résidence", max_chars=50)
    
    with col2:
        profession = st.text_input("Profession", max_chars=50)
        cni = st.text_input("Numéro CNI*", max_chars=20)
        prix_chambre = st.selectbox("Prix de chambre (FCFA)*", [7000, 8000, 10000,12000])
        nb_jours = st.slider("Nombre de jours*", 1, 365, 1)
    
    date_arrivee = st.date_input("Date d'arrivée*", min_value=datetime.today())
    
    # Calcul du montant total
    montant_total = prix_chambre * nb_jours
    
    st.markdown(f"**Montant total à payer: {montant_total} FCFA**")
    st.markdown("*Champs obligatoires*")
    
    submitted = st.form_submit_button("Enregistrer")
    cancelled = st.form_submit_button("Annuler")

# Traitement des actions du formulaire
if submitted:
    if not nom or not prenom or not telephone or not cni:
        st.error("Veuillez remplir tous les champs obligatoires (*)")
    else:
        reservation_data = {
            "Nom": nom,
            "Prenom": prenom,
            "Telephone": telephone,
            "Ville": ville,
            "Profession": profession,
            "CNI": cni,
            "Prix_Chambre": prix_chambre,
            "Nb_Jours": nb_jours,
            "Date_Arrivee": date_arrivee.strftime("%Y-%m-%d"),
            "Montant_Total": montant_total,
            "Date_Reservation": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        add_reservation(reservation_data)
        st.success("Réservation enregistrée avec succès!")
        st.balloons()

if cancelled:
    st.experimental_rerun()
