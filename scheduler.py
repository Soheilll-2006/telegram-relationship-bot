#!/usr/bin/env python3
"""
Scheduler module for the Telegram relationship bot.
Handles daily message scheduling and special occasion detection.
"""

import schedule
import time
import threading
from datetime import datetime, date
import logging
import pytz
from config import Config
from utils import calculate_days_together

logger = logging.getLogger(__name__)

def start_scheduler(bot):
    """Start the message scheduler."""
    config = Config()
    
    # Schedule daily messages at 9:00 AM Asia/Tehran
    tz = pytz.timezone('Asia/Tehran')
    schedule_time = datetime.now(tz).replace(
        hour=config.daily_message_hour,
        minute=config.daily_message_minute,
        second=0,
        microsecond=0
    ).strftime('%H:%M')
    schedule.every().day.at(schedule_time, tz).do(send_scheduled_message, bot)
    
    # Schedule birthday checks at midnight Asia/Tehran
    schedule.every().day.at("00:01", tz).do(check_birthdays, bot)
    
    logger.info(f"✅ Scheduler started - Daily messages at {schedule_time} Asia/Tehran")
    
    # Run scheduler in a loop
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except Exception as e:
            logger.error(f"❌ Error in scheduler: {e}")
            time.sleep(60)

def send_scheduled_message(bot):
    """Send the scheduled daily message."""
    try:
        logger.info("⏰ Sending scheduled daily message...")
        bot.send_daily_message()
    except Exception as e:
        logger.error(f"❌ Error sending scheduled message: {e}")

def check_birthdays(bot):
    """Check if today is anyone's birthday."""
    try:
        config = Config()
        today = date.today()
        
        if config.is_partner_birthday(today):
            partner_name = config.get_birthday_partner_name(today)
            logger.info(f"🎂 Today is {partner_name}'s birthday!")
            bot.send_birthday_message(partner_name)
        
    except Exception as e:
        logger.error(f"❌ Error checking birthdays: {e}")

def manual_send_message(bot):
    """Manually send a message (for testing purposes)."""
    try:
        logger.info("📤 Manually sending message...")
        bot.send_daily_message()
    except Exception as e:
        logger.error(f"❌ Error manually sending message: {e}")