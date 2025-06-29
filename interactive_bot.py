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
from config import Config
from quotes import get_random_quote, get_random_advice
from utils import calculate_days_together, format_milestone_message, is_special_milestone

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Initialize bot and config
config = Config()
bot = telebot.TeleBot(config.bot_token)

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
/advice - دریافت توصیه عاشقانه روزانه
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
        days = calculate_days_together(config.relationship_start_date)
        message_text = format_milestone_message(days)
        bot.reply_to(message, message_text.strip())
    except Exception as e:
        logger.error(f"Error handling milestone command: {e}")
        bot.reply_to(message, "❌ خطا در محاسبه روزهای رابطه")

@bot.message_handler(commands=['quote'])
def handle_quote(message):
    """Handle /quote command."""
    try:
        quote = get_random_quote()
        bot.reply_to(message, f"💝 {quote}")
    except Exception as e:
        logger.error(f"Error handling quote command: {e}")
        bot.reply_to(message, "❌ خطا در دریافت جمله عاشقانه")

@bot.message_handler(commands=['advice'])
def handle_advice(message):
    """Handle /advice command."""
    try:
        advice = get_random_advice()
        bot.reply_to(message, f"💡 توصیه امروز: {advice}")
    except Exception as e:
        logger.error(f"Error handling advice command: {e}")
        bot.reply_to(message, "❌ خطا در دریافت توصیه روزانه")

@bot.message_handler(commands=['test'])
def handle_test(message):
    """Handle /test command."""
    try:
        days = calculate_days_together(config.relationship_start_date)
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
        from bot import RelationshipBot
        bot_instance = RelationshipBot()
        daily_msg = bot_instance.create_daily_message(calculate_days_together(config.relationship_start_date))
        bot.send_message(config.group_id, daily_msg)
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
/advice - دریافت توصیه عاشقانه روزانه
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