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

def is_birthday_today():
    """Check if today is someone's birthday."""
    today = date.today()
    if (today.month, today.day) == SOHEIL_BIRTHDAY:
        return "سهیل"
    elif (today.month, today.day) == SHAMIM_BIRTHDAY:
        return "شمیم"
    return None

def create_daily_message():
    """Create daily relationship message."""
    days = calculate_days_together()
    quote = random.choice(LOVE_QUOTES)
    
    message = f"""🌅 صبح بخیر عزیزان! 🌅

💕 امروز روز {days} از عشق زیبای شماست!

{quote}

با عشق و احترام ❤️"""
    
    # Check for special milestone
    if is_special_milestone(days):
        celebration_emojis = "🎉🎊🥳🎈🎁💐🌹"
        message += f"\n\n{celebration_emojis}\n"
        
        if days == 100:
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
        bot = telebot.TeleBot(BOT_TOKEN)
        bot.send_message(GROUP_ID, message)
        logger.info("✅ Message sent successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Error sending message: {e}")
        return False

def main():
    """Main function to send daily message."""
    if not BOT_TOKEN or not GROUP_ID:
        logger.error("❌ BOT_TOKEN or GROUP_ID not set!")
        return
    
    logger.info("🚀 Creating daily relationship message...")
    message = create_daily_message()
    
    logger.info("📤 Sending message to group...")
    success = send_message_to_group(message)
    
    if success:
        days = calculate_days_together()
        logger.info(f"✅ Daily message sent successfully for day {days}!")
    else:
        logger.error("❌ Failed to send message!")

if __name__ == "__main__":
    main()