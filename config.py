#!/usr/bin/env python3
"""
Configuration management for the Telegram relationship bot.
Handles environment variables and bot settings.
"""

import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.bot_token = self.get_env_var('BOT_TOKEN')
        self.group_id = self.get_env_var('GROUP_ID')
        
        # Relationship start date
        self.relationship_start_date = self.get_relationship_start_date()
        
        # Partner birthdays (format: MM-DD)
        self.partner1_birthday = os.getenv('PARTNER1_BIRTHDAY', '09-22')  # September 22
        self.partner2_birthday = os.getenv('PARTNER2_BIRTHDAY', '11-05')  # November 5
        
        # Partner names
        self.partner1_name = os.getenv('PARTNER1_NAME', 'سهیل')
        self.partner2_name = os.getenv('PARTNER2_NAME', 'شمیم')
        
        # Daily message time (24-hour format, Asia/Tehran)
        self.daily_message_hour = int(os.getenv('DAILY_MESSAGE_HOUR', '9'))
        self.daily_message_minute = int(os.getenv('DAILY_MESSAGE_MINUTE', '0'))
        
        logger.info("✅ Configuration loaded successfully")
    
    def get_env_var(self, var_name, default=None):
        """Get environment variable with error handling."""
        value = os.getenv(var_name, default)
        if not value:
            logger.error(f"❌ Environment variable {var_name} is not set!")
            raise ValueError(f"Environment variable {var_name} is required")
        return value
    
    def get_relationship_start_date(self):
        """Get relationship start date from environment or use default."""
        date_str = os.getenv('RELATIONSHIP_START_DATE', '2025-06-22')  # Default: June 22, 2025
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            logger.error(f"❌ Invalid date format for RELATIONSHIP_START_DATE: {date_str}")
            logger.info("Using default date: 2025-06-22")
            return datetime.strptime('2025-06-22', '%Y-%m-%d').date()
    
    def is_partner_birthday(self, date_obj):
        """Check if the given date is a partner's birthday."""
        date_str = date_obj.strftime('%m-%d')
        return date_str in [self.partner1_birthday, self.partner2_birthday]
    
    def get_birthday_partner_name(self, date_obj):
        """Get the name of the partner whose birthday it is."""
        date_str = date_obj.strftime('%m-%d')
        if date_str == self.partner1_birthday:
            return self.partner1_name
        elif date_str == self.partner2_birthday:
            return self.partner2_name
        return None