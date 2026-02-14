# 🚀 HuggingFace AutoPing

Un outil simple pour maintenir vos Hugging Face Spaces (et autres web apps) actifs 24h/24 gratuitement.

## 🛠️ Comment ça marche ?
1. **L'Interface (Streamlit)** : Vous permet de gérer vos URLs.
2. **L'Automatisation (GitHub Actions)** : Toutes les 12 heures, GitHub lance un script qui "visite" chaque URL pour empêcher la mise en veille.

## 🚀 Installation & Configuration

### Étape 1 : Créer le dépôt GitHub
- Créez un nouveau dépôt sur votre compte GitHub.
- Envoyez tous les fichiers de ce dossier sur le dépôt.

### Étape 2 : Configurer les Permissions (CRUCIAL) ⚠️
Pour que l'automatisme puisse mettre à jour les statuts dans l'interface, il doit avoir le droit d'écrire sur votre dépôt :
1. Sur votre dépôt GitHub, allez dans **Settings**.
2. Dans le menu de gauche, cliquez sur **Actions** > **General**.
3. Faites défiler jusqu'à **Workflow permissions**.
4. Sélectionnez **"Read and write permissions"**.
5. Cliquez sur **Save**.

### Étape 3 : Héberger l'Interface
- Allez sur [Streamlit Cloud](https://share.streamlit.io/) ou créez un nouveau Space sur Hugging Face (type Streamlit).
- Connectez votre dépôt.
- Une fois en ligne, ajoutez l'URL de votre application elle-même dans la liste pour qu'elle reste aussi éveillée !

## 📝 Utilisation
- Ajoutez vos URLs via l'interface.
- Cliquez sur "Relancer tout maintenant" pour un test immédiat.
- Laissez GitHub travailler pour vous le reste du temps.
