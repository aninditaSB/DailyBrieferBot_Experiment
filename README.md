# Daily Brief Bot

A beginner-friendly Python bot that fetches today's top news headlines, writes a fun summary, and sends it to your Telegram — all in about 150 lines of code.

**No AI model needed.** Just Python + a free Google News feed + the Telegram API.

---

## What Does This Bot Do?

You pick a topic (like "artificial intelligence" or "sports"). The bot:

1. Fetches the latest headlines from Google News.
2. Picks the top 3 and wraps them in a short daily briefing with some personality.
3. Prints the briefing in your terminal.
4. Sends it to your Telegram chat.

That's it. One file, one command, instant results.

---

## How the Code Flows

```
 ┌────────────────────────┐
 │   1. LOAD SETTINGS     │  Read secrets from .env file
 └───────────┬────────────┘
             ▼
 ┌────────────────────────┐
 │   2. FETCH NEWS        │  Download headlines from Google News RSS
 └───────────┬────────────┘
             ▼
 ┌────────────────────────┐
 │   3. BUILD SUMMARY     │  Pick top 3, add greeting + closing
 └───────────┬────────────┘
             ▼
 ┌────────────────────────┐
 │   4. SEND TO TELEGRAM  │  POST the message via Telegram Bot API
 └────────────────────────┘
```

Each section is clearly labeled in `main.py` so you can follow along.

---

## Project Structure

```
DailyBrieferBot/
├── main.py            # The entire bot (fetch → summarize → send)
├── requirements.txt   # One dependency: python-dotenv
├── .env.example       # Template — copy this to .env
├── .env               # Your actual secrets (you create this)
└── README.md          # You are here
```

---

## Setup (Step by Step)

### 1. Make Sure Python Is Installed

```bash
python3 --version
```

You need Python 3.7 or newer.

### 2. Install the One Dependency

```bash
pip install -r requirements.txt
```

### 3. Create a Telegram Bot

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot`.
3. Give your bot a **name** (e.g., "My Daily Brief") and a **username** (e.g., `my_daily_brief_bot`).
4. BotFather replies with a **token** — it looks like:
   ```
   123456789:ABCdefGhIjKlmNoPqRsTuVwXyZ
   ```
5. Copy that token.

### 4. Get Your Chat ID

1. Search for **@userinfobot** on Telegram and open it.
2. It replies with your **Chat ID** (a number like `987654321`).
3. Copy that number.

> **Don't forget:** Find your new bot in Telegram and press **Start**. It can't message you until you do.

### 5. Create Your `.env` File

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIjKlmNoPqRsTuVwXyZ
TELEGRAM_CHAT_ID=987654321
TOPIC=artificial intelligence
DRY_RUN=false
```

### 6. Run the Bot!

**Full run** (prints + sends to Telegram):

```bash
python3 main.py
```

**Dry run** (prints only, no Telegram):

```bash
python3 main.py --dry-run
```

The dry-run mode is great for testing and live demos — you don't even need Telegram credentials to see the bot work.

---

## Example Output

```
==================================================
        🤖  Daily Brief Bot
==================================================

🔍 Searching for "artificial intelligence" headlines ...
✅ Found 5 headlines.

──────────────────────────────────────────────────
📰  DAILY BRIEF — Tuesday, March 31, 2026
Topic: Artificial Intelligence

Rise and shine!
I did the scrolling so you don't have to.

  1. OpenAI Announces New Model That Can Reason
  2. Google Brings AI Features to Search
  3. EU Passes Landmark AI Regulation Bill

Stay curious, stay caffeinated. ✌️
──────────────────────────────────────────────────

✅ Message delivered to Telegram!
```

---

## Change the Topic

Edit the `TOPIC` line in your `.env` file:

```
TOPIC=climate change
```

Ideas: `technology`, `sports`, `bitcoin`, `space exploration`, `AI`, `movies`, `startups`.

---

## Troubleshooting

| Problem | What To Do |
|---|---|
| "Missing settings" error | Open `.env` and make sure all values are filled in. |
| "Could not reach Google News" | Check your internet connection. |
| "Could not send to Telegram" | Verify token + chat ID. Make sure you pressed **Start** on the bot. |
| No headlines found | Try a broader topic like `technology` instead of something very niche. |

---

## Deploying to the Cloud (Next Steps)

Once the bot works locally, you can make it run automatically every morning using a free cloud platform.

### Option A: Replit

1. Create a free account at [replit.com](https://replit.com).
2. Create a new **Python** project and upload `main.py` and `requirements.txt`.
3. Go to the **Secrets** tab (lock icon) and add your three environment variables there instead of a `.env` file.
4. Click **Run**.
5. To make it run daily, use Replit's **Deployments** feature or add a simple scheduling service.

### Option B: Railway

1. Create a free account at [railway.app](https://railway.app).
2. Connect your GitHub repo (or upload the files).
3. Go to **Variables** and add `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, and `TOPIC`.
4. Railway will install dependencies and run `main.py` automatically.
5. Use Railway's **Cron** feature to schedule it (e.g., `0 8 * * *` for 8 AM daily).

### Option C: GitHub Actions (Free)

Add a file at `.github/workflows/daily.yml` to run the bot on a schedule:

```yaml
name: Daily Brief
on:
  schedule:
    - cron: '0 13 * * *'   # Runs daily at 8 AM EST (13:00 UTC)
  workflow_dispatch:        # Also allows manual runs

jobs:
  brief:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python main.py
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          TOPIC: 'artificial intelligence'
```

Store your secrets in **GitHub → Settings → Secrets → Actions**.

---

## How It Works (Plain English)

| Section | What It Does |
|---|---|
| **Load Settings** | Reads your Telegram token, chat ID, and topic from `.env`. |
| **Fetch News** | Visits a Google News URL and downloads headlines as XML. |
| **Build Summary** | Picks the top 3 headlines, adds a random greeting and closing. |
| **Send Telegram** | Calls the Telegram Bot API with an HTTP request to deliver the message. |

The whole thing is one Python file with zero magic — every line does something you can point to and explain.
