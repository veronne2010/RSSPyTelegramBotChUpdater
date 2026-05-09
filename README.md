# RSSPyTelegramBotChUpdater

A lightweight Python bot that monitors an RSS feed and automatically posts new articles to a Telegram channel via a Telegram Bot.

---

## Features

- Polls any RSS feed at a configurable interval (default: every 5 minutes)
- Sends new posts to a Telegram channel with a formatted HTML message including title, summary, date, and link
- Persists already-sent links to a local JSON file to avoid duplicate messages
- Posts are sent in chronological order (oldest first)
- Simple, dependency-light, single-file script

---

## Requirements

- Python 3.7+
- A Telegram Bot token (get one from [@BotFather](https://t.me/BotFather))
- A Telegram Channel where your bot is an admin

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies (`requirements.txt`):
```
feedparser==6.0.12
Requests==2.33.1
```

---

## Configuration

Open `script.py` and set the following variables at the top of the file:

| Variable | Description | Example |
|---|---|---|
| `BOT_TOKEN` | Your Telegram Bot token | `"123456:ABC-DEF..."` |
| `CHANNEL_ID` | Your channel username or numeric ID | `"@mychannel"` or `"-1001234567890"` |
| `RSS_URL` | The RSS feed URL to monitor | `"https://example.com/feed.xml"` |
| `CHECK_INTERVAL` | Polling interval in seconds | `300` (5 minutes) |
| `STORAGE_FILE` | Path to the JSON file for storing sent links | `"sent_links.json"` |

---

## Usage

```bash
python script.py
```

The bot will start polling the RSS feed and print status messages to the console:

```
🚀 Bot RSS avviato! Controllo ogni 300 secondi.
✅ Messaggio inviato
```

---

## Project Structure

```
RSSPyTelegramBotChUpdater/
├── script.py          # Main bot script
├── requirements.txt   # Python dependencies
├── sent_links.json    # Auto-generated — stores already-sent article links
└── README.md
```

---

## Message Format

Each new article is sent as an HTML-formatted Telegram message:

```
📢 Nuovo Post!

📰 Article Title

🗓️ 2025-01-15

Short summary of the article...

👉 Read the full article
```

---

## Tips

- **Keep it running**: use `nohup`, `screen`, `tmux`, or a systemd service to run the bot in the background on a server.
- **Customize the message**: edit the `message` string inside `fetch_and_send()` to change the format.
- **Multiple feeds**: duplicate the `fetch_and_send()` logic or refactor it to loop over a list of RSS URLs.

---

## License

This project is licensed under the [MIT License](LICENSE).