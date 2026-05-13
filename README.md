# ⚡ MailIA Pro - Boîte de réception intelligente

**MailIA Pro** est un dashboard email intelligent propulsé par l'Intelligence Artificielle (Google Gemini 2.5 Flash). Conçu pour les professionnels, les freelances et les agences, cet outil permet de trier, résumer et rédiger automatiquement des brouillons de réponses aux emails entrants directement depuis une interface web fluide.

Développé par **Gabriel Vernat**.

---

## 🚀 Fonctionnalités Principales

- **Synchronisation IMAP :** Récupération sécurisée des derniers emails de votre boîte Gmail.
- **Catégorisation Automatique :** Attribution de badges intelligents (URGENT, DEVIS, INFO) selon le contenu du mail.
- **Résumé Express IA :** Synthèse en une phrase de la demande du client pour un gain de temps immédiat.
- **Génération de Brouillons :** Rédaction de réponses structurées, professionnelles et adaptées au contexte.
- **Personnalité Sur-Mesure :** L'IA s'adapte à votre ton (formel, tutoiement, expert, etc.) via des instructions personnalisables.
- **Envoi Sécurisé :** Modification du brouillon en direct et ouverture native de votre client mail via un lien `mailto` sécurisé.

---

## 📂 Structure du Projet

````text
📁 mon-projet/
├── 📁 code/                 # Dossier principal contenant la logique de l'application
│   └── app.py               # Le script principal Streamlit (Interface et Backend)
├── 📁 env/                  # Environnement virtuel Python (à ne pas push sur GitHub)
├── .gitignore               # Fichier ignorant l'environnement et les clés privées
└── README.md                # Documentation du projet (ce fichier)

# Se placer dans le dossier du projet
cd code/

# Créer un environnement virtuel
python -m venv env

# Activer l'environnement virtuel
# Sur Windows :
.\env\Scripts\activate
# Sur Mac/Linux :
source env/bin/activate

# Installer les dépendances nécessaires
pip install streamlit google-genai

# Lancement de l'application
streamlit run app.py


# ⚡ MailIA Pro - Boîte de réception intelligente

**MailIA Pro** est un dashboard email intelligent propulsé par l'Intelligence Artificielle (Google Gemini 2.5 Flash). Conçu pour les professionnels, les freelances et les agences, cet outil permet de trier, résumer et rédiger automatiquement des brouillons de réponses aux emails entrants directement depuis une interface web fluide.

Développé par **Gabriel Vernat**.

---

## 🚀 Fonctionnalités Principales

*   **Synchronisation IMAP :** Récupération sécurisée des derniers emails de votre boîte Gmail.
*   **Catégorisation Automatique :** Attribution de badges intelligents (URGENT, DEVIS, INFO) selon le contenu du mail.
*   **Résumé Express IA :** Synthèse en une phrase de la demande du client pour un gain de temps immédiat.
*   **Génération de Brouillons :** Rédaction de réponses structurées, professionnelles et adaptées au contexte.
*   **Personnalité Sur-Mesure :** L'IA s'adapte à votre ton (formel, tutoiement, expert, etc.) via des instructions personnalisables.
*   **Envoi Sécurisé :** Modification du brouillon en direct et ouverture native de votre client mail via un lien `mailto` sécurisé.

---

## 📂 Structure du Projet

```text
📁 mon-projet/
├── 📁 code/                 # Dossier principal contenant la logique de l'application
│   └── app.py               # Le script principal Streamlit (Interface et Backend)
├── 📁 env/                  # Environnement virtuel Python (à ne pas push sur GitHub)
├── .gitignore               # Fichier ignorant l'environnement et les clés privées
└── README.md                # Documentation du projet (ce fichier)
````

---

## 🛠️ Installation et Configuration

### Prérequis

- Python 3.9 ou supérieur installé sur votre machine.
- Un compte Google (pour générer une clé API Gemini).
- Un compte Gmail avec la validation en deux étapes activée (pour le mot de passe d'application).

### 1. Cloner et préparer l'environnement

Ouvrez votre terminal et exécutez les commandes suivantes :

```bash
# Se placer dans le dossier du projet
cd code/

# Créer un environnement virtuel
python -m venv env

# Activer l'environnement virtuel (Sur Windows)
.\env\Scripts\activate

# Installer les dépendances nécessaires
pip install streamlit google-genai
```

---

## 📖 Guide d'Utilisation Détaillé (Étape par Étape)

Pour utiliser MailIA Pro, vous devez configurer vos accès sécurisés. Voici la marche à suivre complète :

### Étape 1 : Obtenir un Mot de passe d'Application Gmail

1. Allez sur votre compte Google (myaccount.google.com).
2. Allez dans l'onglet **Sécurité**.
3. Assurez-vous que la **Validation en deux étapes** est activée.
4. Cherchez **Mots de passe des applications** dans la barre de recherche des paramètres.
5. Créez une nouvelle application (nommez-la "MailIA" par exemple) et cliquez sur "Générer".
6. **Copiez le mot de passe à 16 lettres** qui s'affiche (sans les espaces). C'est ce mot de passe que vous utiliserez dans l'application.

### Étape 2 : Obtenir une Clé API Google Gemini

1. Rendez-vous sur Google AI Studio (aistudio.google.com).
2. Connectez-vous avec votre compte Google.
3. Cliquez sur **Get API Key** (Obtenir une clé API).
4. Cliquez sur le bouton **Create API key** et copiez la clé générée.

### Étape 3 : Lancer l'Application

Dans votre terminal (avec l'environnement virtuel activé), lancez le serveur :

```bash
streamlit run app.py
```

Une fenêtre s'ouvrira automatiquement dans votre navigateur (généralement sur `http://localhost:8501`).

### Étape 4 : Configurer l'Interface (Menu Latéral)

Dans l'interface web, regardez la barre latérale gauche **"⚙️ Connexion"** :

1. **Adresse Gmail :** Entrez votre adresse email classique.
2. **Mot de passe d'App :** Collez le mot de passe à 16 lettres obtenu à l'Étape 1.
3. **Clé API Gemini :** Collez la clé obtenue à l'Étape 2.
4. **Personnalité de l'IA :** Modifiez le texte pour indiquer à l'IA comment elle doit réagir (ex: "Je suis développeur web freelance, je vouvoie mes clients et je suis très formel").

### Étape 5 : Traiter ses Emails

1. Cliquez sur le bouton **"🔄 Synchroniser les mails"** dans la partie gauche de l'écran. Vos derniers emails apparaîtront sous forme de liste.
2. Sélectionnez l'email que vous souhaitez traiter.
3. Dans la partie droite, cliquez sur le bouton rouge **"Générer l'analyse et la réponse"**.
4. L'IA va analyser le mail, lui attribuer un badge (URGENT, DEVIS, etc.), rédiger un résumé et préparer un brouillon.
5. **Modifiez le brouillon** si nécessaire directement dans la zone de texte.
6. Cliquez sur **"💾 Valider mes modifications"** pour sauvegarder vos changements.
7. Cliquez sur **"🚀 Ouvrir ma boîte mail"**. Votre logiciel de messagerie s'ouvrira avec l'adresse du client, le sujet et votre brouillon prêts à être envoyés !
