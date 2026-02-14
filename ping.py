import json
import requests
import os
from datetime import datetime

URLS_FILE = "urls.json"

def run_pings():
    if not os.path.exists(URLS_FILE):
        print("Aucun fichier urls.json trouvé.")
        return

    try:
        with open(URLS_FILE, "r") as f:
            urls_data = json.load(f)
    except Exception as e:
        print(f"Erreur lors de la lecture des URLs : {e}")
        return

    if not urls_data:
        print("Aucune URL à pinguer.")
        return

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Démarrage du ping automatique...")

    updated = False
    for item in urls_data:
        url = item['url']
        try:
            # On envoie une requête GET
            response = requests.get(url, timeout=20)
            item['status'] = f"OK ({response.status_code})"
            print(f"✅ {url} : {response.status_code}")
        except Exception as e:
            item['status'] = "Erreur"
            print(f"❌ {url} : {str(e)}")

        item['last_ping'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        updated = True

    if updated:
        with open(URLS_FILE, "w") as f:
            json.dump(urls_data, f, indent=4)
        print("Fichier urls.json mis à jour.")

if __name__ == "__main__":
    run_pings()
