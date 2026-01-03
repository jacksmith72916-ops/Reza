import logging
import pytz
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, filters, CommandHandler
from flask import Flask
from threading import Thread

# --- تنظیمات سرور برای زنده نگه داشتن در Render ---
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"

def run():
    # پورت را از تنظیمات رندر می‌گیرد یا به صورت پیش‌فرض روی 10000 قرار می‌دهد
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- اطلاعات ربات ---
BOT_TOKEN = "8171932436:AAEv45_rsCrqnPtFP3putCoxN3CIRyGHeLw"
ADMIN_ID = 8354557890
ADMIN_USERNAME = "@RE3PJ"

game_data = {"target": 0, "active": False, "scores": {}, "game_type": None, "pattern_val": None, "mode": "IDLE"}

# --- بخش دستورات ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id == ADMIN_ID:
        keyboard = [[InlineKeyboardButton("🏀", callback_query_data="set_🏀"), InlineKeyboardButton("⚽️", callback_query_data="set_⚽️")],
                    [InlineKeyboardButton("🎯", callback_query_data="set_🎯"), InlineKeyboardButton("🎰", callback_query_data="set_🎰")]]
        await update.message.reply_text("💎 بازی را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(f"🎰 خوش آمدید ادمین: {ADMIN_USERNAME}")

# --- اجرای ربات ---
if __name__ == '__main__':
    keep_alive() # روشن کردن سرور داخلی
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    
    # نکته: اگر کدهای هندلر بازی (مثل MessageHandler یا CallbackQueryHandler) را داری، 
    # حتماً زیر همین خط اضافه کن تا بازی کار کند.
    
    print("Bot is running...")
    app_bot.run_polling()
