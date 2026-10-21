import telebot
import random
import string
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# --- Web Server to Keep Render Alive ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Aktif!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- Telegram Bot Setup ---
TOKEN = "8855902728:AAE4lu0WAXU89fSJjR9mQLjvkRsK6afUwXM"
bot = telebot.TeleBot(TOKEN)

# Key Database (In-Memory)
keys_db = {}

def generate_key(duration_type):
    letters = string.ascii_uppercase + string.digits
    key = "SP4CEX-" + ''.join(random.choice(letters) for _ in range(8))
    
    now = datetime.now()
    if duration_type == "gunluk":
        expires = now + timedelta(days=1)
    elif duration_type == "haftalik":
        expires = now + timedelta(weeks=1)
    elif duration_type == "aylik":
        expires = now + timedelta(days=30)
    else:
        expires = now + timedelta(days=1)
        
    keys_db[key] = {"expires": expires, "used": False}
    return key

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "👑 sp4ceX VIP Key Botuna Hoş Geldiniz!\n\nKomutlar:\n/gunluk - 1 Günlük Key\n/haftalik - 7 Günlük Key\n/aylik - 30 Günlük Key"
    )

@bot.message_handler(commands=['gunluk'])
def get_daily_key(message):
    k = generate_key("gunluk")
    bot.reply_to(message, f"🔑 Günlük Keyiniz:\n`{k}`", parse_mode="Markdown")

@bot.message_handler(commands=['haftalik'])
def get_weekly_key(message):
    k = generate_key("haftalik")
    bot.reply_to(message, f"🔑 Haftalık Keyiniz:\n`{k}`", parse_mode="Markdown")

@bot.message_handler(commands=['aylik'])
def get_monthly_key(message):
    k = generate_key("aylik")
    bot.reply_to(message, f"🔑 Aylık Keyiniz:\n`{k}`", parse_mode="Markdown")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
