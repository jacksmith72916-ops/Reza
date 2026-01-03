import telebot
from datetime import datetime

# --- تنظیمات اولیه ---
TOKEN = "8171932436:AAEv45_rsCrqnPtFP3putCoxN3CIRyGHeLw"
ADMIN_ID = 8354557890
ADMIN_USERNAME = "@RE3PJ"

bot = telebot.TeleBot(TOKEN)

# متغیر برای ذخیره وضعیت بازی‌ها
# ساختار: chat_id -> {game_type, target, current_scores: {user_id: score}, setting_mode: bool}
games = {}

# --- لیست دستورات ادمین ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ربات فعال است. ادمین می‌تواند بازی‌ها را تنظیم کند.")

# 1. تنظیم کازینو (اسلات ماشین)
@bot.message_handler(commands=['set_casino'])
def set_casino(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    games[message.chat.id] = {
        'type': 'casino',
        'step': 'waiting_for_spin',
        'target': 0
    }
    
    text = (
        "🎲 ثبت مقدار انتخابی کازینو\n\n"
        "لطفا یکبار کازینو (🎰) بزنید تا مقدار آن ذخیره شود."
    )
    bot.reply_to(message, text)

# 2. تنظیم تاس
@bot.message_handler(commands=['set_dice'])
def set_dice(message):
    if message.from_user.id != ADMIN_ID:
        return
    games[message.chat.id] = {'type': 'dice', 'step': 'waiting_for_target', 'scores': {}}
    text = (
        "🎯 تنظیم تعداد گل هدف برای 🎲 تاس\n\n"
        "لطفاً تعداد گل هدف را وارد کنید:\n\n"
        "مثال: برای هدف ۱۰ گل، عدد ۱۰ را ارسال کنید.\n"
        "📝 توجه: محاسبه‌گر وقتی متوقف می‌شود که یک کاربر به این تعداد گل برسد.\n"
        "📝 هر گل = 1 امتیاز\n"
        "⚠️ توجه: هر کسی که این مقدار را بیاورد برنده خواهد شد."
    )
    bot.reply_to(message, text)

# 3. تنظیم دارت
@bot.message_handler(commands=['set_dart'])
def set_dart(message):
    if message.from_user.id != ADMIN_ID:
        return
    games[message.chat.id] = {'type': 'dart', 'step': 'waiting_for_target', 'scores': {}}
    text = (
        "🎯 تنظیم تعداد گل هدف برای 🎯 دارت\n\n"
        "لطفاً تعداد گل هدف را وارد کنید:\n\n"
        "مثال: برای هدف ۱۰ گل، عدد ۱۰ را ارسال کنید.\n"
        "📝 توجه: محاسبه‌گر وقتی متوقف می‌شود که یک کاربر به این تعداد گل برسد.\n"
        "📝 هر گل = 1 امتیاز"
    )
    bot.reply_to(message, text)

# 4. تنظیم بولینگ
@bot.message_handler(commands=['set_bowling'])
def set_bowling(message):
    if message.from_user.id != ADMIN_ID:
        return
    games[message.chat.id] = {'type': 'bowling', 'step': 'waiting_for_target', 'scores': {}}
    text = (
        "🎯 تنظیم تعداد گل هدف برای بولینگ🎳\n\n"
        "لطفاً تعداد افتادن هدف را وارد کنید:\n\n"
        "مثال: برای هدف ۱۰ افتادن، عدد ۱۰ را ارسال کنید.\n"
        "📝 توجه: محاسبه‌گر وقتی متوقف می‌شود که یک کاربر به این تعداد افتادن برسد.\n"
        "📝 هر افتادن = 1 امتیاز"
    )
    bot.reply_to(message, text)

# 5. تنظیم فوتبال
@bot.message_handler(commands=['set_football'])
def set_football(message):
    if message.from_user.id != ADMIN_ID:
        return
    games[message.chat.id] = {'type': 'football', 'step': 'waiting_for_target', 'scores': {}}
    text = (
        "🎯 تنظیم تعداد گل هدف برای فوتبال⚽️\n\n"
        "لطفاً تعداد گل هدف را وارد کنید:\n\n"
        "مثال: برای هدف ۱۰ گل، عدد ۱۰ را ارسال کنید.\n"
        "📝 توجه: محاسبه‌گر وقتی متوقف می‌شود که یک کاربر به این تعداد گل برسد.\n"
        "📝 هر گل = 1 امتیاز"
    )
    bot.reply_to(message, text)

# 6. تنظیم بسکتبال
@bot.message_handler(commands=['set_basketball'])
def set_basketball(message):
    if message.from_user.id != ADMIN_ID:
        return
    games[message.chat.id] = {'type': 'basketball', 'step': 'waiting_for_target', 'scores': {}}
    text = (
        "🎯 تنظیم تعداد گل هدف برای بسکتبال 🏀\n\n"
        "لطفاً تعداد گل هدف را وارد کنید:\n\n"
        "مثال: برای هدف ۱۰ گل، عدد ۱۰ را ارسال کنید.\n"
        "📝 توجه: محاسبه‌گر وقتی متوقف می‌شود که یک کاربر به این تعداد گل برسد.\n"
        "📝 هر گل = 1 امتیاز"
    )
    bot.reply_to(message, text)


# --- دریافت ورودی‌ها (تعداد گل یا چرخش کازینو ادمین) ---

@bot.message_handler(content_types=['text'])
def handle_text_settings(message):
    # فقط ادمین
    if message.from_user.id != ADMIN_ID:
        return
    
    chat_id = message.chat.id
    if chat_id not in games:
        return
    
    game = games[chat_id]
    
    # اگر منتظر عدد هدف هستیم (برای بازی‌های امتیازی)
    if game.get('step') == 'waiting_for_target' and message.text.isdigit():
        target = int(message.text)
        game['target'] = target
        game['step'] = 'active' # بازی شروع شد
        bot.reply_to(message, f"✅ هدف روی {target} تنظیم شد! بازی شروع شد.")

@bot.message_handler(content_types=['dice'])
def handle_dice_events(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    # بررسی اینکه آیا بازی در این گروه فعال است
    if chat_id not in games:
        return
    
    game = games[chat_id]
    dice_value = message.dice.value
    emoji = message.dice.emoji

    # --- سناریو ۱: ادمین دارد کازینو را تنظیم می‌کند ---
    if game.get('step') == 'waiting_for_spin' and user_id == ADMIN_ID and emoji == '🎰':
        game['target'] = dice_value
        game['step'] = 'active'
        text = (
            f"✅ مقدار انتخابی کازینو به {dice_value} تنظیم شد!\n"
            "هر کسی که این مقدار را بیاورد برنده خواهد شد."
        )
        bot.reply_to(message, text)
        return

    # --- سناریو ۲: بازی فعال است و کاربران بازی می‌کنند ---
    if game.get('step') != 'active':
        return

    # منطق کازینو (برد لحظه‌ای)
    if game['type'] == 'casino' and emoji == '🎰':
        if dice_value == game['target']:
            # برنده شد!
            now_time = datetime.now().strftime("%H:%M:%S")
            username = message.from_user.username if message.from_user.username else "ندارد"
            
            win_msg = (
                "✅ درخواست شما ثبت شد! ✅\n\n"
                f"🏆 برنده: {first_name}\n"
                f"🆔 آیدی: @{username}\n"
                "🎁 درخواست: استارز\n"
                f"⏰ زمان: {now_time}\n\n"
                "📞 درخواست شما به ادمین‌ها ارسال شد.\n\n"
                "────────────────\n"
                "⚠️ توجه: ادمین‌ها به زودی با شما تماس خواهند گرفت."
            )
            bot.reply_to(message, win_msg)
            # پایان بازی یا ریست (در اینجا فقط پیام می‌دهد)
        return

    # منطق بازی‌های امتیازی (تاس، فوتبال، بسکتبال و ...)
    # تطبیق ایموجی بازی با تنظیمات
    emoji_map = {
        'dice': '🎲',
        'dart': '🎯',
        'bowling': '🎳',
        'football': '⚽',
        'basketball': '🏀'
    }
    
    if game['type'] in emoji_map and emoji == emoji_map[game['type']]:
        # شرط امتیاز گرفتن:
        # برای سادگی و "چالش"، هر پرتاب موفق را 1 امتیاز حساب می‌کنیم
        # یا طبق دستور: "هر گل = 1 امتیاز". 
        # منطق گل در تلگرام:
        is_goal = False
        if game['type'] == 'basketball' and dice_value in [4, 5]: is_goal = True
        elif game['type'] == 'football' and dice_value in [3, 4, 5]: is_goal = True
        elif game['type'] == 'bowling' and dice_value == 6: is_goal = True # استرایک
        elif game['type'] == 'dart' and dice_value == 6: is_goal = True # مرکز
        elif game['type'] == 'dice' and dice_value >= 1: is_goal = True # هر پرتاب برای تاس (چون تاس گل ندارد، شمارش مهم است)
        # اگر می‌خواهید برای بقیه هم "هر پرتاب" امتیاز داشته باشد، شرط بالا را تغییر دهید.
        # اما معمولاً "گل" یعنی موفقیت. با توجه به متن "هر گل = 1 امتیاز"، من موفقیت را شرط می‌گذارم
        # بجز تاس که گفته "هر کسی مقدار را بیاورد" (که کازینو بود) اما برای تاس "تعداد گل هدف" گفته.
        # پس برای تاس هر پرتاب را 1 امتیاز می‌گیریم تا بازی جلو برود.
        
        # اصلاحیه: برای اینکه بازی سخت نباشد و "شمارشگر" باشد طبق مثال (هدف 500)،
        # فرض می‌کنیم هر بار که کاربر تاس انداخت 1 امتیاز می‌گیرد.
        scored = 1
        
        # ذخیره امتیاز
        if user_id not in game['scores']:
            game['scores'][user_id] = {'name': first_name, 'score': 0}
        
        game['scores'][user_id]['score'] += scored
        user_score = game['scores'][user_id]['score']
        target_score = game['target']
        remaining = target_score - user_score
        
        # اگر امتیاز از هدف رد شد، 0 نشان بده
        if remaining < 0: remaining = 0

        # پیام امتیاز دقیقاً طبق الگو
        score_msg = (
            f"🎯 {first_name} گل زد!\n\n"
            f"🏆 تعداد گل‌های شما: {user_score}\n"
            f"🎯 تا برنده شدن: {remaining} گل دیگر\n"
            f"📊 هدف: {target_score} گل"
        )
        bot.reply_to(message, score_msg)
        
        # بررسی برنده شدن نهایی
        if user_score >= target_score:
            bot.send_message(chat_id, f"🏆 پایان بازی! {first_name} به هدف رسید و برنده شد!")
            # پاک کردن بازی (اختیاری)
            # del games[chat_id]

# روشن نگه داشتن ربات
print("Robot is running...")
bot.infinity_polling()
