#!/usr/bin/env python3
"""
Utility functions for the Telegram relationship bot.
Contains helper functions for date calculations and message formatting.
"""

from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

def calculate_days_together(start_date):
    """Calculate the number of days since the relationship started."""
    try:
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        
        today = date.today()
        delta = today - start_date
        return delta.days + 1  # +1 to include the start date
    
    except Exception as e:
        logger.error(f"❌ Error calculating days together: {e}")
        return 0

def is_special_milestone(days):
    """Check if the current day count is a special milestone."""
    special_milestones = [
        7, 30, 60, 90, 100, 200, 365, 500, 730,  # Week, month, 2 months, 3 months, etc.
        1000, 1095, 1500, 1825, 2000, 2555, 3000, 3650  # 1000 days, 3 years, etc.
    ]
    return days in special_milestones

def format_milestone_message(days):
    """Format a milestone message with proper Persian text."""
    try:
        from quotes import get_random_quote, get_random_advice
        quote = get_random_quote()
        advice = get_random_advice()
        
        message = f"""
🌹 تبریک! 🌹

💕 امروز روز {days} از عشق زیبای شماست!

"""
        
        # Add special notes for certain milestones
        if days == 7:
            message += "🌸 یک هفته کامل عشق! 🌸\n"
        elif days == 30:
            message += "🌟 یک ماه عاشقانه! 🌟\n"
        elif days == 100:
            message += "🎯 صد روز کامل عشق! 🎯\n"
        elif days == 365:
            message += "🎂 یک سال کامل عاشقی! 🎂\n"
        elif days == 1000:
            message += "👑 هزار روز فوق‌العاده! 👑\n"
        elif days % 100 == 0:
            message += f"✨ {days} روز درخشان! ✨\n"
        elif is_special_milestone(days):
            message += f"🎉 {days} روز پر از عشق! 🎉\n"
        
        # Calculate years, months, and remaining days
        years = days // 365
        remaining_days = days % 365
        months = remaining_days // 30
        final_days = remaining_days % 30
        
        if years > 0:
            message += f"📅 {years} سال"
            if months > 0:
                message += f" و {months} ماه"
            if final_days > 0:
                message += f" و {final_days} روز"
            message += " از عشق شما!\n"
        elif months > 0:
            message += f"📅 {months} ماه"
            if final_days > 0:
                message += f" و {final_days} روز"
            message += " از عشق شما!\n"
        
        # Add next milestone
        next_milestone = get_next_milestone(days)
        message += f"\n⏳ {next_milestone - days} روز تا نقطه عطف بعدی ({next_milestone} روز) باقی مانده!"
        
        message += f"\n\n💝 {quote}\n\n💡 توصیه امروز: {advice}\n\n💖 عشق شما همچنان زیبا و قوی است!"
        
        return message.strip()
    
    except Exception as e:
        logger.error(f"❌ Error formatting milestone message: {e}")
        return f"💕 امروز روز {days} از عشق شماست! 💕"

def format_number_persian(number):
    """Convert English numbers to Persian numbers."""
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    
    result = str(number)
    for i, digit in enumerate(english_digits):
        result = result.replace(digit, persian_digits[i])
    
    return result

def get_persian_day_name(date_obj):
    """Get Persian day name for a given date."""
    days = {
        0: 'دوشنبه',
        1: 'سه‌شنبه',
        2: 'چهارشنبه',
        3: 'پنج‌شنبه',
        4: 'جمعه',
        5: 'شنبه',
        6: 'یکشنبه'
    }
    return days.get(date_obj.weekday(), 'نامشخص')

def get_persian_month_name(month_number):
    """Get Persian month name for a given month number."""
    months = {
        1: 'ژانویه', 2: 'فوریه', 3: 'مارس', 4: 'آپریل',
        5: 'مه', 6: 'ژوئن', 7: 'ژوئیه', 8: 'آگوست',
        9: 'سپتامبر', 10: 'اکتبر', 11: 'نوامبر', 12: 'دسامبر'
    }
    return months.get(month_number, 'نامشخص')

def validate_date_format(date_string, format_string='%Y-%m-%d'):
    """Validate if a date string matches the expected format."""
    try:
        datetime.strptime(date_string, format_string)
        return True
    except ValueError:
        return False

def get_next_milestone(current_days):
    """Get the next milestone day count."""
    milestones = [7, 30, 60, 90, 100, 200, 365, 500, 730, 1000, 1095, 1500, 1825, 2000, 2555, 3000, 3650]
    
    for milestone in milestones:
        if milestone > current_days:
            return milestone
    
    # If all milestones are passed, return the next thousand
    return ((current_days // 1000) + 1) * 1000