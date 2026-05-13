import streamlit as st
import imaplib
import email
from email.header import decode_header
from google import genai
import urllib.parse
import streamlit.components.v1 as components

# --- 1. CONFIGURATION VISUELLE & BRANDING ---
st.set_page_config(page_title="MailIA Pro", page_icon="⚡", layout="wide")

# CSS personnalisé pour les badges
st.markdown(
    """
<style>
.badge-urgent { background-color: #ff4b4b; color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.9em;}
.badge-devis { background-color: #00cc96; color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.9em;}
.badge-info { background-color: #1f77b4; color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.9em;}
.badge-default { background-color: #808495; color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.9em;}
</style>
""",
    unsafe_allow_html=True,
)

st.title("Boîte de réception intelligente ⚡")
st.caption("Propulsé par l'Intelligence Artificielle")

# --- 2. INITIALISATION DE LA MÉMOIRE ---
if "liste_mails" not in st.session_state:
    st.session_state.liste_mails = []

# --- 3. MENU LATÉRAL (Espace Client) ---
st.sidebar.markdown("## 🏢 Mon Agence IA")
st.sidebar.info("Espace sécurisé Client")

st.sidebar.header("⚙️ Connexion")
email_user = st.sidebar.text_input("Adresse Gmail", value="ton.adresse@gmail.com")
email_pass = st.sidebar.text_input("Mot de passe d'App", type="password")
api_key = st.sidebar.text_input("Clé API Gemini", type="password")

st.sidebar.markdown("---")
st.sidebar.header("🎭 Personnalité de l'IA")
personnalite_client = st.sidebar.text_area(
    "Instructions personnalisées :",
    value="Je m'appelle Gabriel Vernat, je suis expert web. Je vouvoie les clients avec un ton formel et premium.",
    help="Décrivez simplement qui vous êtes et comment vous parlez.",
)
st.sidebar.markdown("---")


# --- 4. FONCTION DE RÉCUPÉRATION DES MAILS ---
def recuperer_mails(limite=10):
    mails_trouves = []
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_pass)
        mail.select("inbox")
        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()

        if mail_ids:
            derniers_ids = mail_ids[-limite:][::-1]
            for i in derniers_ids:
                res, msg_data = mail.fetch(i, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        sujet, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(sujet, bytes):
                            sujet = sujet.decode(encoding if encoding else "utf-8")
                        mails_trouves.append(
                            {"id": i, "expediteur": msg.get("From"), "sujet": sujet}
                        )
        mail.logout()
        return mails_trouves
    except Exception as e:
        st.error(f"❌ Erreur de connexion : {e}")
        return []


# --- 5. L'INTERFACE PRINCIPALE ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📬 Boîte de réception")
    if st.button("🔄 Synchroniser les mails", use_container_width=True):
        if not email_pass:
            st.warning("⚠️ Remplissez vos identifiants à gauche.")
        else:
            with st.spinner("Récupération en cours..."):
                st.session_state.liste_mails = recuperer_mails(limite=10)
                st.success(f"{len(st.session_state.liste_mails)} mail(s) trouvé(s) !")

    st.markdown("---")
    mail_selectionne = None
    if st.session_state.liste_mails:
        options = [
            f"{m['expediteur']} - {m['sujet'][:30]}..."
            for m in st.session_state.liste_mails
        ]
        choix = st.radio("Sélectionnez un mail :", options)
        mail_selectionne = st.session_state.liste_mails[options.index(choix)]

with col2:
    if mail_selectionne:
        st.subheader("✉️ Détail du message")
        st.markdown(f"**De :** `{mail_selectionne['expediteur']}`")
        st.markdown(f"**Sujet :** {mail_selectionne['sujet']}")
        st.divider()

        st.markdown("### 🤖 Analyse & Action IA")

        cle_categorie = f"categorie_{mail_selectionne['id']}"
        cle_resume = f"resume_{mail_selectionne['id']}"
        cle_brouillon = f"brouillon_{mail_selectionne['id']}"

        if st.button("Générer l'analyse et la réponse", type="primary"):
            if not api_key:
                st.error("⚠️ Entrez votre clé API Gemini à gauche.")
            else:
                with st.spinner("L'IA analyse les intentions du client..."):
                    try:
                        client = genai.Client(api_key=api_key)

                        # --- INJECTION DES RÈGLES SECRÈTES ---
                        regles_de_formatage_cachees = """
                        RÈGLES ABSOLUES POUR LA GÉNÉRATION (FORMATAGE) :
                        1. Pour la Partie 1 (Résumé) : NE ME DIS PAS BONJOUR. Rédige uniquement le résumé brut et neutre du mail.
                        2. Pour la Partie 2 (Brouillon) : Interdiction absolue de faire une phrase d'introduction (ne dis jamais "Voici le brouillon :" ou "Voici une proposition :"). Commence DIRECTEMENT par la salutation.
                        3. Pour la Salutation : Analyse le champ 'Expéditeur'. Ne mets JAMAIS de crochets [ ]. Commence toujours directement par "Bonjour Monsieur [Vrai nom]" ou "Bonjour Madame [Vrai nom]".
                        """
                        custom_instructions = (
                            personnalite_client + "\n\n" + regles_de_formatage_cachees
                        )

                        # --- LE PROMPT STRICT INTOUCHABLE ---
                        prompt = f"""
                        Tu es un assistant de direction virtuel de très haut niveau, expert en relation client et vente de services B2B.

                        CONTEXTE DE L'UTILISATEUR (À RESPECTER ABSOLUMENT) :
                        {custom_instructions if custom_instructions else "Adopte un ton extrêmement formel, poli et expert. Vouvoie le client."}

                        Expéditeur : {mail_selectionne['expediteur']}
                        Sujet : {mail_selectionne['sujet']}

                        MISSION : 
                        Sépare OBLIGATOIREMENT ta réponse en deux parties avec la balise exacte : |||
                        Partie 1 (Avant la balise) : Un résumé très court (1 ou 2 phrases) du besoin.
                        Partie 2 (Après la balise) : Rédige le brouillon de la réponse.

                        CONSIGNES STRICTES POUR LE BROUILLON :
                        - Structure : Fais une réponse longue et détaillée (au moins 3 ou 4 paragraphes).
                        - Empathie & Rassurance : Remercie le client pour sa demande et montre que tu as parfaitement compris l'enjeu.
                        - Précision : Réponds point par point aux questions posées dans le mail (utilise des puces ou tirets si besoin).
                        - Expertise : Si le client parle technique (API, e-commerce, budget), montre ton professionnalisme en demandant des précisions stratégiques (ex: technologies visées, volume de trafic, etc.).
                        - Conclusion : Termine toujours par un "Appel à l'action" clair (ex: proposer 2 créneaux horaires pour un appel, ou demander un cahier des charges).
                        """

                        reponse_ia = client.models.generate_content(
                            model="gemini-2.5-flash", contents=prompt
                        )

                        # --- DÉCOUPAGE ADAPTÉ AUX 2 PARTIES ---
                        texte_complet = reponse_ia.text.split("|||")

                        if len(texte_complet) >= 2:
                            st.session_state[cle_resume] = texte_complet[0].strip()
                            st.session_state[cle_brouillon] = texte_complet[1].strip()

                            # Logique automatique pour les badges de couleur
                            sujet_mail = mail_selectionne["sujet"].lower()
                            if "urgent" in sujet_mail:
                                st.session_state[cle_categorie] = "URGENT"
                            elif any(
                                mot in sujet_mail
                                for mot in ["devis", "prix", "budget", "tarif"]
                            ):
                                st.session_state[cle_categorie] = "DEVIS"
                            else:
                                st.session_state[cle_categorie] = "INFO"
                        else:
                            st.session_state[cle_categorie] = "INFO"
                            st.session_state[cle_resume] = "Résumé indisponible."
                            st.session_state[cle_brouillon] = reponse_ia.text

                    except Exception as e:
                        st.error(f"❌ Erreur IA : {e}")

                        # --- L'AFFICHAGE PREMIUM ---
        if cle_brouillon in st.session_state:

            # Choix de la couleur du badge
            cat = st.session_state[cle_categorie]
            css_class = "badge-default"
            if "URGENT" in cat:
                css_class = "badge-urgent"
            elif "DEVIS" in cat:
                css_class = "badge-devis"
            elif "INFO" in cat:
                css_class = "badge-info"

            # Affichage Badge + Résumé
            st.markdown(
                f"**Tag IA :** <span class='{css_class}'>🏷️ {cat}</span>",
                unsafe_allow_html=True,
            )
            st.markdown("#### 📌 Résumé express :")
            st.info(st.session_state[cle_resume])

            # --- LE FORMULAIRE PRO (Résout les problèmes de synchronisation) ---
            with st.form(key=f"form_{mail_selectionne['id']}"):
                # Zone de texte modifiable
                brouillon_final = st.text_area(
                    "✍️ Brouillon proposé (modifiable) :",
                    value=st.session_state[cle_brouillon],
                    height=350,
                )

                # Le bouton qui force la sauvegarde de tes modifications
                sauvegarde = st.form_submit_button("💾 Valider mes modifications")
                if sauvegarde:
                    # Si tu cliques, on met à jour la mémoire de l'application
                    st.session_state[cle_brouillon] = brouillon_final
                    st.success("✅ Texte mis à jour avec succès !")

            # --- LE BOUTON D'ENVOI SÉCURISÉ ---
            # Le lien lit maintenant directement la mémoire (qui est toujours à jour)
            sujet_encode = urllib.parse.quote(f"Re: {mail_selectionne['sujet']}")
            corps_encode = urllib.parse.quote(st.session_state[cle_brouillon])
            lien_mailto = f"mailto:{mail_selectionne['expediteur']}?subject={sujet_encode}&body={corps_encode}"

            st.markdown("---")
            # Le vrai composant lien, 100% autorisé par les navigateurs
            st.link_button("🚀 Ouvrir ma boîte mail", url=lien_mailto, type="primary")
