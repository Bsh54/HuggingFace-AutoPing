# 🚀 HuggingFace AutoPing

Un outil simple pour maintenir vos Hugging Face Spaces (et autres web apps) actifs 24h/24 gratuitement.

## 🛠️ Comment ça marche ?
1. **L'Interface (Streamlit)** : Vous permet de gérer vos URLs.
2. **L'Automatisation (GitHub Actions)** : Toutes les 12 heures, GitHub lance un script qui "visite" chaque URL pour empêcher la mise en veille.

## 🚀 Installation & Configuration

### Étape 1 : Créer le dépôt GitHub
- Créez un nouveau dépôt sur votre compte GitHub.
- Envoyez tous les fichiers de ce dossier sur le dépôt.

### Étape 2 : Configurer les Permissions & Secrets (CRUCIAL) ⚠️

1. **Permissions du Workflow** :
   - Sur votre dépôt GitHub, allez dans **Settings** > **Actions** > **General**.
   - Sélectionnez **"Read and write permissions"** et cliquez sur **Save**.

2. **Accès depuis l'Interface (Persistance des liens)** :
   - Pour que vos liens ne disparaissent pas, l'interface doit pouvoir enregistrer les changements sur GitHub.
   - Créez un **Personal Access Token (classic)** sur GitHub avec le scope **`repo`**.
   - Sur votre plateforme d'hébergement (Streamlit Cloud ou HF Spaces), ajoutez un secret nommé **`GH_TOKEN`** contenant votre token.

### Étape 3 : Héberger l'Interface
- Allez sur [Streamlit Cloud](https://share.streamlit.io/) ou créez un nouveau Space sur Hugging Face (type Streamlit).
- Connectez votre dépôt.
- Une fois en ligne, ajoutez l'URL de votre application elle-même dans la liste pour qu'elle reste aussi éveillée !

## 📝 Utilisation
- Ajoutez vos URLs via l'interface.
- Cliquez sur "Relancer tout maintenant" pour un test immédiat.
- Laissez GitHub travailler pour vous le reste du temps.
