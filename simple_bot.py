#!/usr/bin/env python3
"""
Simple Telegram relationship bot that can be run on-demand.
No continuous polling - just runs when needed.
"""

import os
import telebot
from datetime import datetime, date
import random
import logging
from config import Config
from quotes import get_random_quote, get_random_advice
from utils import calculate_days_together, is_special_milestone

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Bot configuration
config = Config()
bot = telebot.TeleBot(config.bot_token)

def is_birthday_today():
    """Check if today is someone's birthday."""
    today = date.today()
    date_str = today.strftime('%m-%d')
    if date_str == config.partner1_birthday:
        return config.partner1_name
    elif date_str == config.partner2_birthday:
        return config.partner2_name
    return None

def create_daily_message():
    """Create daily relationship message."""
    days = calculate_days_together(config.relationship_start_date)
    quote = get_random_quote()
    advice = get_random_advice()
    
    message = f"""🌅 صبح بخیر عزیزان! 🌅

💕 امروز روز {days} از عشق زیبای شماست!

💝 {quote}

💡 توصیه امروز: {advice}

با عشق و احترام ❤️"""
    
    # Check for special milestone
    if is_special_milestone(days):
        celebration_emojis = "🎉🎊🥳🎈🎁💐🌹"
        message += f"\n\n{celebration_emojis}\n"
        
        if days == 7:
            message += "🌸 یک هفته کامل عشق! 🌸"
        elif days == 30:
            message += "🌟 یک ماه عاشقانه! 🌟"
        elif days == 100:
            message += "🎯 صد روز عشق! 🎯"
        elif days == 200:
            message += "🌟 دویست روز عاشقی! 🌟"
        elif days == 365:
            message += "🎂 یک سال کامل عشق! 🎂"
        elif days == 500:
            message += "💎 پانصد روز درخشان! 💎"
        elif days == 1000:
            message += "👑 هزار روز عاشقی! 👑"
        else:
            message += f"✨ {days} روز فوق‌العاده! ✨"
        
        message += f"\n{celebration_emojis}"
    
    # Check for birthdays
    birthday_person = is_birthday_today()
    if birthday_person:
        message += f"\n\n🎂🎉 تولد {birthday_person} عزیز مبارک! 🎉🎂"
        message += "\n💝 امیدوارم این سال جدید پر از عشق، شادی و لحظات خوشبختی باشد!"
    
    return message

def send_message_to_group(message):
    """Send message to Telegram group."""
    try:
        bot.send_message(config.group_id, message)
        logger.info("✅ Message sent successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Error sending message: {e}")
        return False

def main():
    """Main function to send daily message."""
    if not config.bot_token or not config.group_id:
        logger.error("❌ BOT_TOKEN or GROUP_ID not set!")
        return
    
    logger.info("🚀 Creating daily relationship message...")
    message = create_daily_message()
    
    logger.info("📤 Sending message to group...")
    success = send_message_to_group(message)
    
    if success:
        days = calculate_days_together(config.relationship_start_date)
        logger.info(f"✅ Daily message sent successfully for day {days}!")
    else:
        logger.error("❌ Failed to send message!")

if __name__ == "__main__":
    main()