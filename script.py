import requests
import feedparser
import time
import json
import os

# --- CONFIGURAZIONE ---
BOT_TOKEN = "[your-bot-token-here]"
CHANNEL_ID = "[your-channel-id-or-username-here]"
RSS_URL = "[your-rss-feed-url-here]"
CHECK_INTERVAL = 300  # every 5 minutes it checks for new posts
STORAGE_FILE = "sent_links.json"

# --- FUNZIONI BASE ---
def telegram_send_message(text: str):
    """Invia un messaggio HTML al canale."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    r = requests.post(url, data=payload)
    if not r.ok:
        print(f"❌ Errore Telegram: {r.text}")
    else:
        print("✅ Messaggio inviato")

def load_sent_links():
    """Carica i link già inviati da file JSON."""
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_sent_links(links):
    """Salva i link già inviati."""
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(links), f, indent=2)

def fetch_and_send():
    """Controlla il feed RSS e invia nuovi post."""
    feed = feedparser.parse(RSS_URL)
    new_links = False

    for entry in reversed(feed.entries):  # reversed = invia dal più vecchio al più nuovo
        if entry.link not in sent_links:
            # --- Personalizza il messaggio ---
            title = entry.title
            summary = getattr(entry, "summary", "")[:100]
            published = getattr(entry, "published", "Data sconosciuta")[:10]
            message = (
                f"<b>📢 Nuovo Post!</b>\n\n"
                f"<b>📰 {title}</b>\n\n"
                f"🗓️ {published}\n\n"
                f"{summary}\n\n"
                f"👉 <a href='{entry.link}'>Leggi l'articolo completo</a>"
            )

            telegram_send_message(message)
            sent_links.add(entry.link)
            new_links = True

    if new_links:
        save_sent_links(sent_links)

# --- MAIN LOOP ---
if __name__ == "__main__":
    sent_links = load_sent_links()
    print("🚀 Bot RSS avviato! Controllo ogni", CHECK_INTERVAL, "secondi.")
    while True:
        try:
            fetch_and_send()
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print("⚠️ Errore:", e)
            time.sleep(60)
