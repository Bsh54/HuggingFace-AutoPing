import json
import requests
import time
import sys
from datetime import datetime

URLS_FILE = "urls.json"

def load_urls():
    try:
        with open(URLS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_urls(urls):
    with open(URLS_FILE, "w") as f:
        json.dump(urls, f, indent=4)

def add_url(url):
    urls = load_urls()
    if url not in [u['url'] for u in urls]:
        urls.append({"url": url, "last_ping": None, "status": "unknown"})
        save_urls(urls)
        print(f"Ajouté : {url}")
    else:
        print(f"L'URL existe déjà.")

def list_urls():
    urls = load_urls()
    if not urls:
        print("Aucune URL enregistrée.")
        return
    print("\n--- Liste des Spaces ---")
    for i, u in enumerate(urls):
        print(f"{i}. {u['url']} | Last: {u.get('last_ping', 'Jamais')} | Status: {u.get('status', 'N/A')}")

def ping_all():
    urls = load_urls()
    if not urls:
        print("Rien à pinguer.")
        return

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Lancement du réveil...")
    for u in urls:
        try:
            # On utilise un timeout de 15s pour laisser le temps au Space de démarrer
            response = requests.get(u['url'], timeout=15)
            u['status'] = f"OK ({response.status_code})"
            u['last_ping'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"✅ {u['url']} : {u['status']}")
        except Exception as e:
            u['status'] = f"Erreur: {str(e)}"
            u['last_ping'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"❌ {u['url']} : {u['status']}")

    save_urls(urls)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manager.py add <url>")
        print("  python manager.py list")
        print("  python manager.py run")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) > 2:
        add_url(sys.argv[2])
    elif cmd == "list":
        list_urls()
    elif cmd == "run":
        ping_all()
    else:
        print("Commande inconnue.")
