import streamlit as st
import json
import requests
from datetime import datetime
import os
import subprocess

URLS_FILE = "urls.json"

def git_commit_push():
    """Commit et push le fichier urls.json vers GitHub."""
    try:
        # On vérifie si on est dans un dépôt Git
        if not os.path.exists(".git"):
            st.warning("⚠️ Pas un dépôt Git. Sauvegarde locale uniquement.")
            return

        # Configuration de l'utilisateur pour le commit
        subprocess.run(["git", "config", "--local", "user.email", "action@github.com"], check=True)
        subprocess.run(["git", "config", "--local", "user.name", "Streamlit App"], check=True)

        # Ajout et commit
        subprocess.run(["git", "add", URLS_FILE], check=True)
        commit_msg = f"Update via UI: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # On vérifie s'il y a des changements avant de commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout
        if not status:
            return

        subprocess.run(["git", "commit", "-m", commit_msg], check=True)

        # On récupère les dernières modifications de GitHub pour éviter les conflits
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)

        # Tentative de push avec gestion du Token
        # Si un token est configuré dans les secrets Streamlit, on l'utilise
        github_token = st.secrets.get("GH_TOKEN")
        if github_token:
            # On récupère l'URL du remote actuel
            remote_url = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
            # On insère le token dans l'URL (format: https://token@github.com/user/repo.git)
            if "github.com" in remote_url and "@" not in remote_url:
                new_remote_url = remote_url.replace("https://", f"https://{github_token}@")
                subprocess.run(["git", "remote", "set-url", "origin", new_remote_url], check=True)

        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if result.returncode == 0:
            st.toast("✅ Synchronisé avec GitHub !")
        else:
            st.error(f"Erreur de synchronisation : {result.stderr}")
            st.info("💡 Avez-vous configuré le GH_TOKEN dans les secrets Streamlit ?")
    except Exception as e:
        st.error(f"Erreur Git : {e}")

def load_urls():
    if os.path.exists(URLS_FILE):
        try:
            with open(URLS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_urls(urls, sync=True):
    with open(URLS_FILE, "w") as f:
        json.dump(urls, f, indent=4)
    if sync:
        git_commit_push()

st.set_page_config(page_title="HuggingFace AutoPing", page_icon="🚀")

st.title("🚀 HuggingFace AutoPing")
st.write("Maintenez vos Spaces actifs gratuitement 24h/24.")

# --- Gestion des URLs ---
if "urls" not in st.session_state:
    st.session_state.urls = load_urls()

with st.sidebar:
    st.header("Ajouter un Space")
    new_url = st.text_input("URL du Space (ex: https://user-name.hf.space)")
    if st.button("Ajouter"):
        if new_url and new_url not in [u['url'] for u in st.session_state.urls]:
            st.session_state.urls.append({
                "url": new_url,
                "last_ping": "Jamais",
                "status": "Inconnu"
            })
            save_urls(st.session_state.urls)
            st.success("Ajouté !")
            st.rerun()
        else:
            st.warning("URL vide ou déjà présente.")

# --- Affichage et Actions ---
st.subheader("Mes Spaces")
if not st.session_state.urls:
    st.info("Aucun Space enregistré. Utilisez la barre latérale pour en ajouter.")
else:
    # Vérification si l'URL actuelle est dans la liste (auto-relance)
    current_url = st.query_params.get("url", "")

    for i, u in enumerate(st.session_state.urls):
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            col1.write(f"**{u['url']}**")
            col2.write(f"🕒 {u['last_ping']}")

            # Couleur du statut
            status_text = u.get('status', 'Inconnu')
            if "OK" in status_text:
                col3.success(status_text)
            elif "Erreur" in status_text:
                col3.error(status_text)
            else:
                col3.info(status_text)

            if col4.button("🗑️", key=f"del_{i}"):
                st.session_state.urls.pop(i)
                save_urls(st.session_state.urls)
                st.rerun()
        st.divider()

    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("🔄 Relancer tout maintenant", type="primary", use_container_width=True):
        with st.spinner("Réveil des Spaces en cours..."):
            for u in st.session_state.urls:
                try:
                    r = requests.get(u['url'], timeout=20)
                    u['status'] = f"OK ({r.status_code})"
                except Exception as e:
                    u['status'] = "Erreur"
                u['last_ping'] = datetime.now().strftime("%d/%m %H:%M")
            save_urls(st.session_state.urls)
            st.success("Tous les Spaces ont été sollicités !")
            st.rerun()

    if col_btn2.button("🧹 Effacer les logs", use_container_width=True):
        for u in st.session_state.urls:
            u['status'] = "Inconnu"
            u['last_ping'] = "Jamais"
        save_urls(st.session_state.urls)
        st.rerun()

st.divider()
st.info("💡 **Note pour l'hébergement :** Si vous hébergez ceci sur Streamlit Cloud, connectez votre repo GitHub. Pour l'auto-ping toutes les 12h, assurez-vous que le dossier `.github/workflows` est présent.")
