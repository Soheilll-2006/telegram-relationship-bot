#!/usr/bin/env python3
"""
Interactive Telegram relationship bot.
Run this when you want to respond to commands like /start, /test, /quote
"""

import os
import telebot
from datetime import datetime, date
import random
import logging
import signal
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUP_ID = int(os.getenv('GROUP_ID'))

# Relationship info
RELATIONSHIP_START_DATE = date(2025, 6, 22)
SOHEIL_BIRTHDAY = (9, 23)  # September 23
SHAMIM_BIRTHDAY = (11, 7)  # November 7

# Love quotes
LOVE_QUOTES = [
    "عشق تنها احساسی است که هرچه بیشتر بدهی، بیشتر داری. 💕",
    "در عشق، کوچکترین لحظه‌ها بزرگترین خاطره‌ها می‌شوند. 🌹",
    "عشق یعنی دیدن آینده در چشمان کسی که دوستش داری. 👁️‍🗨️",
    "هر صبح که چشمانم را باز می‌کنم، خوشحالم که تو در زندگی‌ام هستی. ☀️",
    "عشق واقعی نیازی به کلمات ندارد، صدای قلب کافی است. 💗",
    "تو نه تنها عشق زندگی‌ام، بلکه زندگی عشق‌ام هستی. 💖",
    "عشق زبان مشترک همه قلب‌هاست. 💞",
    "در دنیای پر از سر و صدا، عشق تو آرامش من است. 🕊️",
    "عشق یعنی مراقبت، احترام و درک متقابل. 🤝",
    "هر روز با تو، هدیه‌ای از آسمان است. 🎁"
]

def calculate_days_together():
    """Calculate days since relationship started."""
    today = date.today()
    delta = today - RELATIONSHIP_START_DATE
    return delta.days + 1

def is_special_milestone(days):
    """Check if it's a special milestone."""
    return days in [100, 200, 365, 500, 730, 1000, 1095, 1500, 1825, 2000]

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    logger.info('🛑 Stopping bot...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

@bot.message_handler(commands=['start'])
def handle_start(message):
    """Handle /start command."""
    welcome_message = """
🌹 سلام عزیزان! 🌹

من ربات خاص رابطه شما هستم! 💕

دستورات موجود:
/milestone - نمایش روزهای گذشته از رابطه
/quote - دریافت جمله عاشقانه تصادفی
/test - ارسال پیام تست
/daily - ارسال پیام روزانه
/help - راهنمای استفاده

با عشق، ربات شما 💖
    """
    bot.reply_to(message, welcome_message)

@bot.message_handler(commands=['milestone'])
def handle_milestone(message):
    """Handle /milestone command."""
    try:
        days = calculate_days_together()
        
        message_text = f"""
🌹 تبریک! 🌹

💕 امروز روز {days} از عشق زیبای شماست!

"""
        
        # Add special notes for certain milestones
        if days == 100:
            message_text += "🎯 صد روز کامل عشق! 🎯\n"
        elif days == 365:
            message_text += "🎂 یک سال کامل عاشقی! 🎂\n"
        elif days == 1000:
            message_text += "👑 هزار روز فوق‌العاده! 👑\n"
        elif days % 100 == 0:
            message_text += f"✨ {days} روز درخشان! ✨\n"
        
        # Calculate years, months, and remaining days
        years = days // 365
        remaining_days = days % 365
        months = remaining_days // 30
        final_days = remaining_days % 30
        
        if years > 0:
            message_text += f"📅 {years} سال"
            if months > 0:
                message_text += f" و {months} ماه"
            if final_days > 0:
                message_text += f" و {final_days} روز"
            message_text += " از عشق شما!\n"
        elif months > 0:
            message_text += f"📅 {months} ماه"
            if final_days > 0:
                message_text += f" و {final_days} روز"
            message_text += " از عشق شما!\n"
        
        message_text += "\n💖 عشق شما همچنان زیبا و قوی است!"
        
        bot.reply_to(message, message_text.strip())
    except Exception as e:
        logger.error(f"Error handling milestone command: {e}")
        bot.reply_to(message, "❌ خطا در محاسبه روزهای رابطه")

@bot.message_handler(commands=['quote'])
def handle_quote(message):
    """Handle /quote command."""
    try:
        quote = random.choice(LOVE_QUOTES)
        bot.reply_to(message, f"💝 {quote}")
    except Exception as e:
        logger.error(f"Error handling quote command: {e}")
        bot.reply_to(message, "❌ خطا در دریافت جمله عاشقانه")

@bot.message_handler(commands=['test'])
def handle_test(message):
    """Handle /test command."""
    try:
        days = calculate_days_together()
        test_message = f"""
🧪 پیام تست ربات 🧪

✅ ربات به درستی کار می‌کند!
💕 امروز روز {days} از رابطه شماست
🤖 همه سیستم‌ها عملیاتی هستند

این پیام تست بود - ربات شما آماده است! 🎉
        """
        bot.reply_to(message, test_message.strip())
        logger.info(f"✅ Test message sent successfully for day {days}")
    except Exception as e:
        logger.error(f"❌ Error sending test message: {e}")
        bot.reply_to(message, "❌ خطا در ارسال پیام تست")

@bot.message_handler(commands=['daily'])
def handle_daily(message):
    """Handle /daily command - send daily message manually."""
    try:
        from simple_bot import create_daily_message
        daily_msg = create_daily_message()
        bot.send_message(GROUP_ID, daily_msg)
        bot.reply_to(message, "✅ پیام روزانه ارسال شد!")
    except Exception as e:
        logger.error(f"❌ Error sending daily message: {e}")
        bot.reply_to(message, "❌ خطا در ارسال پیام روزانه")

@bot.message_handler(commands=['help'])
def handle_help(message):
    """Handle /help command."""
    help_message = """
📋 راهنمای استفاده:

/start - شروع ربات
/milestone - نمایش روزهای گذشته از رابطه
/quote - دریافت جمله عاشقانه تصادفی
/test - ارسال پیام تست
/daily - ارسال پیام روزانه
/help - نمایش این راهنما

برای خروج از ربات: Ctrl+C 💕
    """
    bot.reply_to(message, help_message)

def main():
    """Main function to start interactive bot."""
    logger.info("🚀 Starting interactive relationship bot...")
    logger.info("💡 The bot will respond to commands in your group")
    logger.info("🛑 Press Ctrl+C to stop the bot")
    
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        logger.error(f"❌ Error in bot polling: {e}")

if __name__ == "__main__":
    main()