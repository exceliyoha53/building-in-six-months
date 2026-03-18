import os
import sys
import telebot
import requests
from dotenv import load_dotenv
from pathlib import Path

current_dir = Path(__file__).resolve().parent
master_project_dir = current_dir.parent / "Month_01_Automation" / "Month_01_Master_Project"
sys.path.append(str(master_project_dir))

from lead_scraper import B2BLeadExtractor  # noqa: E402

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    """
    Responds when the user first joins or asks fro help.
    """
    welcome_text = (
        "🤖 **Master Engine Command Center**\n\n"
        "Available Commands:\n"
        "/status - Check engine health\n"
        "/ping - Test comms latency"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")


@bot.message_handler(commands=["status"])
def engine_status(message):
    """Simulates checking the health of your Month 1 database."""
    user_id = message.chat.id
    print(f"Status requested by Authorized ID: {user_id}")
    bot.reply_to(
        message, "✅ All systems operational. B2B Vault secured. No active scrapers running."
    )


@bot.message_handler(commands=["ping"])
def ping_pong(message):
    """A simple test command."""
    bot.reply_to(message, "Pong the server hears you loud and clear.")


@bot.message_handler(commands=["scrape"])
def excecute_b2b_scraping(message):
    """Wakes up the Playwright ghost browser and executes the scrape."""
    user_id = message.chat.id
    bot.reply_to(
        message,
        "⚙️ Command received. Booting up Playwright Ghost Browser...\nTarget: B2B Sandbox Directory.",
    )

    try:
        sandbox_target = "https://scrapethissite.com/pages/"
        engine = B2BLeadExtractor(target_url=sandbox_target)
        engine.extract_directory()
        bot.send_message(
            user_id,
            f"✅ Extraction Complete!\nSecured {engine.total_leads_secured} leads and synced them to the SQLite Vault.",
        )

    except Exception as e:
        bot.send_message(user_id, f"❌ Critical failure during extraction:\n{str(e)}")


@bot.message_handler(commands=["price"])
def get_crypto_price(message):
    """Extracts the arguments from the user's text and hits a public API."""
    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot.reply_to(
            message,
            "⚠️ Please provide a coin name. Example: `/price bitcoin`",
            parse_mode="Markdown",
        )
        return
    target_coin = command_parts[1].lower()
    bot.reply_to(message, f"🔍 Fetching live API data for {target_coin}...")
    api_url = f"https://api.coingecko.com/api/v3/simple/price?ids={target_coin}&vs_currencies=eur"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        if target_coin in data:
            current_price = data[target_coin]["eur"]
            bot.send_message(
                message.chat.id,
                f"📈 The current price of **{target_coin.title()}** is **€{current_price:,}**",
                parse_mode="Markdown",
            )
        else:
            bot.send_message(
                message.chat.id, f"❌ Could not find data for '{target_coin}'. Check the spelling."
            )

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ API Error: {str(e)}")


if __name__ == "__main__":
    print("\n📡 Command Center is online and listening... (Press Ctrl+C to shutdown)")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
