"""
Daily Brief Bot
================
A tiny bot that fetches news headlines, builds a fun summary,
and sends it to your Telegram.

Usage:
    python main.py "AI"             → fetch AI news + send to Telegram
    python main.py "sports"         → fetch sports news + send to Telegram
    python main.py "AI" --dry-run   → fetch + print only (no Telegram)
    python main.py                  → uses TOPIC from .env (or "technology")
"""

import os
import sys
import random
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
from datetime import datetime
from dotenv import load_dotenv


# ============================================================
#  SECTION 1 — LOAD SETTINGS
# ============================================================
# We keep secrets in a .env file so they never end up in the code.
# load_dotenv() reads that file and makes the values available.

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

# Dry-run mode: set DRY_RUN=true in .env OR pass --dry-run flag
DRY_RUN = (
    os.getenv("DRY_RUN", "false").lower() == "true"
    or "--dry-run" in sys.argv
)

# Topic priority: command-line argument → .env file → default "technology"
# We grab any arg that isn't "--dry-run" as the topic.
def get_topic():
    """Figures out which topic to use."""
    cli_args = [a for a in sys.argv[1:] if a != "--dry-run"]
    if cli_args:
        return cli_args[0]                          # from command line
    return os.getenv("TOPIC", "technology")         # from .env or default

TOPIC = get_topic()


def check_settings():
    """
    Checks that the required settings are present.
    In dry-run mode we only need a TOPIC, not Telegram credentials.
    """
    if DRY_RUN:
        # No Telegram credentials needed for a dry run
        return

    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")

    if missing:
        print()
        print("🚫 Oops! Some settings are missing from your .env file:\n")
        for var in missing:
            print(f"   ❌  {var}")
        print()
        print("👉 Quick fix:")
        print("   1. Open the file called  .env  in this folder.")
        print("   2. Fill in the missing values (see .env.example).")
        print("   3. Run this script again.")
        print()
        print("💡 Tip: You can also run  python main.py --dry-run")
        print("   to test without Telegram.\n")
        sys.exit(1)


# ============================================================
#  SECTION 2 — FETCH NEWS
# ============================================================
# We use Google News RSS — a free, public feed that returns
# headlines as XML. No API key needed!

def fetch_headlines(topic, count=5):
    """
    Goes to Google News, searches for our topic,
    and returns up to `count` headline strings.
    """
    encoded_topic = urllib.parse.quote(topic)
    url = (
        "https://news.google.com/rss/search"
        f"?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
    )

    print(f"🔍 Searching for \"{topic}\" headlines ...")

    # — Download the RSS feed —
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DailyBriefBot/1.0"})
        response = urllib.request.urlopen(req, timeout=10)
        xml_data = response.read()
    except Exception as error:
        print(f"\n⚠️  Could not reach Google News.")
        print(f"   Reason: {error}")
        print("   Are you connected to the internet?\n")
        return []

    # — Parse the XML to extract titles —
    try:
        root = ET.fromstring(xml_data)
        titles = root.findall(".//item/title")
        headlines = [t.text for t in titles[:count] if t.text]
    except Exception as error:
        print(f"\n⚠️  Got the data but couldn't read it.")
        print(f"   Reason: {error}\n")
        return []

    print(f"✅ Found {len(headlines)} headlines.\n")
    return headlines


# ============================================================
#  SECTION 3 — BUILD SUMMARY
# ============================================================
# No AI model here — just string formatting with personality.

# Greetings that rotate randomly each run
GREETINGS = [
    "Good morning, human.",
    "Rise and shine!",
    "Hey there, busy person.",
    "Greetings, fellow earthling.",
    "Top of the morning to you!",
]

# Fixed closing line — because this one's perfect
CLOSING = "End of briefing. You may return to your coffee. ☕"


def build_summary(topic, headlines):
    """
    Picks the top 3 headlines and wraps them in a short,
    clean daily briefing message.
    """
    today    = datetime.now().strftime("%A, %B %d, %Y")
    greeting = random.choice(GREETINGS)
    closing  = CLOSING
    top3     = headlines[:3]

    # Assemble the message line by line
    msg  = f"📰  *DAILY BRIEF — {today}*\n"
    msg += f"Topic: *{topic.title()}*\n\n"
    msg += f"_{greeting}_\n"
    msg += "I did the scrolling so you don't have to.\n\n"

    for i, headline in enumerate(top3, start=1):
        msg += f"  {i}. {headline}\n"

    msg += f"\n_{closing}_"
    return msg


# ============================================================
#  SECTION 4 — SEND TELEGRAM MESSAGE
# ============================================================
# Telegram bots have a simple HTTP API:
#   POST https://api.telegram.org/bot<TOKEN>/sendMessage
# We send JSON with the chat_id and the text.

def send_telegram(message):
    """Sends the summary to your Telegram chat."""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = json.dumps({
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       message,
        "parse_mode": "Markdown",
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            url, data=payload,
            headers={"Content-Type": "application/json"},
        )
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())

        if result.get("ok"):
            print("✅ Message delivered to Telegram!")
        else:
            print("⚠️  Telegram said something unexpected:")
            print(f"   {result}")

    except Exception as error:
        print(f"\n❌ Could not send the message to Telegram.")
        print(f"   Reason: {error}\n")
        print("   Checklist:")
        print("   • Is your TELEGRAM_BOT_TOKEN correct?")
        print("   • Is your TELEGRAM_CHAT_ID correct?")
        print("   • Did you press  Start  on your bot in Telegram?\n")


# ============================================================
#  SECTION 5 — RUN THE BOT
# ============================================================

def main():
    """Runs the whole bot: load → fetch → build → send."""

    # ---- Banner ----
    print()
    print("=" * 50)
    print("        🤖  Daily Brief Bot")
    if DRY_RUN:
        print("           (dry-run mode)")
    print("=" * 50)
    print()

    # Step 1 — Check settings
    check_settings()

    # Step 2 — Fetch headlines
    headlines = fetch_headlines(TOPIC)

    if not headlines:
        print("😕 No headlines found.")
        print(f"   Try a different topic:  python main.py \"something else\"\n")
        sys.exit(0)

    # Step 3 — Build the summary
    summary = build_summary(TOPIC, headlines)

    # Step 4 — Print it in the terminal
    print("─" * 50)
    print(summary)
    print("─" * 50)
    print()

    # Step 5 — Send to Telegram (unless dry-run)
    if DRY_RUN:
        print("📋 Dry-run mode — message was NOT sent to Telegram.")
        print("   Remove --dry-run to send it for real.\n")
    else:
        send_telegram(summary)


# This is the entry point — Python starts here.
if __name__ == "__main__":
    main()
