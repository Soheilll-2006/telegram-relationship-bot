#!/usr/bin/env python3
"""
Main bot functionality for the Telegram relationship bot.
Handles message sending, milestone calculations, and bot commands.
"""

import telebot
from datetime import datetime, timedelta
import logging
import random
from config import Config
from quotes import get_random_quote, get_random_advice
from utils import calculate_days_together, format_milestone_message, is_special_milestone

logger = logging.getLogger(__name__)

class RelationshipBot:
    def __init__(self):
        """Initialize the bot with configuration."""
        self.config = Config()
        self.bot = telebot.TeleBot(self.config.bot_token)
        self.setup_handlers()
        
    def setup_handlers(self):
        """Set up bot command handlers."""
        
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            """Handle /start command."""
            welcome_message = """
🌹 سلام عزیزان! 🌹

من ربات خاص رابطه شما هستم! 💕
هر روز در ساعت ۹ صبح به وقت تهران، پیام عاشقانه‌ای همراه با توصیه‌ای برای رابطه‌تان می‌فرستم.

دستورات موجود:
/milestone - نمایش روزهای گذشته از رابطه
/quote - دریافت جمله عاشقانه تصادفی
/advice - دریافت توصیه عاشقانه روزانه
/help - راهنمای استفاده

با عشق، ربات شما 💖
            """
            self.bot.reply_to(message, welcome_message)
            
        @self.bot.message_handler(commands=['milestone'])
        def handle_milestone(message):
            """Handle /milestone command."""
            try:
                days = calculate_days_together(self.config.relationship_start_date)
                milestone_msg = format_milestone_message(days)
                self.bot.reply_to(message, milestone_msg)
            except Exception as e:
                logger.error(f"Error handling milestone command: {e}")
                self.bot.reply_to(message, "❌ خطا در محاسبه روزهای رابطه")
                
        @self.bot.message_handler(commands=['quote'])
        def handle_quote(message):
            """Handle /quote command."""
            try:
                quote = get_random_quote()
                self.bot.reply_to(message, f"💝 {quote}")
            except Exception as e:
                logger.error(f"Error handling quote command: {e}")
                self.bot.reply_to(message, "❌ خطا در دریافت جمله عاشقانه")
                
        @self.bot.message_handler(commands=['advice'])
        def handle_advice(message):
            """Handle /advice command."""
            try:
                advice = get_random_advice()
                self.bot.reply_to(message, f"💡 توصیه امروز: {advice}")
            except Exception as e:
                logger.error(f"Error handling advice command: {e}")
                self.bot.reply_to(message, "❌ خطا در دریافت توصیه روزانه")
                
        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            """Handle /help command."""
            help_message = """
📋 راهنمای استفاده:

/start - شروع ربات
/milestone - نمایش روزهای گذشته از رابطه
/quote - دریافت جمله عاشقانه تصادفی
/advice - دریافت توصیه عاشقانه روزانه
/test - ارسال پیام تست
/help - نمایش این راهنما

ربات هر روز ساعت ۹ صبح به وقت تهران پیام عاشقانه و توصیه می‌فرستد 💕
            """
            self.bot.reply_to(message, help_message)
            
        @self.bot.message_handler(commands=['test'])
        def handle_test(message):
            """Handle /test command - send a test message."""
            try:
                days = calculate_days_together(self.config.relationship_start_date)
                test_message = f"""
🧪 پیام تست ربات 🧪

✅ ربات به درستی کار می‌کند!
💕 امروز روز {days} از رابطه شماست
🤖 همه سیستم‌ها عملیاتی هستند

این پیام تست بود - ربات شما آماده است! 🎉
                """
                self.bot.reply_to(message, test_message.strip())
                logger.info(f"✅ Test message sent successfully for day {days}")
            except Exception as e:
                logger.error(f"❌ Error sending test message: {e}")
                self.bot.reply_to(message, "❌ خطا در ارسال پیام تست")
    
    def send_daily_message(self):
        """Send daily relationship milestone message."""
        try:
            days = calculate_days_together(self.config.relationship_start_date)
            
            # Check if it's a special milestone
            if is_special_milestone(days):
                message = self.create_special_milestone_message(days)
            else:
                message = self.create_daily_message(days)
            
            self.bot.send_message(self.config.group_id, message)
            logger.info(f"✅ Daily message sent successfully for day {days}")
            
        except Exception as e:
            logger.error(f"❌ Error sending daily message: {e}")
    
    def create_daily_message(self, days):
        """Create a regular daily message with random quote and advice."""
        quote = get_random_quote()
        advice = get_random_advice()
        
        # Random greeting variations
        greetings = [
            "🌅 صبح بخیر عزیزان! 🌅",
            "☀️ سلام صبح عاشقان! ☀️", 
            "🌸 صبحتان بخیر و پر از عشق! 🌸",
            "💫 صبح امروز هم با عشق شما زیبا شد! 💫",
            "🌺 صبح پر از عشق و شادی! 🌺",
            "🌼 روزی جدید با عشق شما آغاز شد! 🌼",
            "💖 صبحی عاشقانه برای شما! 💖"
        ]
        
        # Random day descriptions
        day_descriptions = [
            f"💕 امروز روز {days} از عشق زیبای شماست!",
            f"❤️ {days} روز از این عشق قشنگ گذشته!",
            f"💖 امروز {days} روز است که عاشق هستید!",
            f"🥰 {days} روز عشق و خوشبختی!",
            f"💝 روز {days} از داستان عاشقانه‌تان!",
            f"🌹 {days} روز از این عشق بی‌نظیر!",
            f"💞 {days} روز پر از لحظه‌های عاشقانه!"
        ]
        
        # Random closing messages
        closings = [
            "با عشق و احترام ❤️",
            "عاشقانه برای شما 💕",
            "با آرزوی روزی پر از عشق 🌹",
            "همیشه عاشق و خوشبخت باشید 💖",
            "عشق شما جاودانه باد 💞",
            "برای همیشه عاشق بمانید 🌟",
            "با تمام عشق، ربات شما 🥰"
        ]
        
        greeting = random.choice(greetings)
        day_desc = random.choice(day_descriptions)
        closing = random.choice(closings)
        
        message = f"""
{greeting}

{day_desc}

💝 {quote}

💡 توصیه امروز: {advice}

{closing}
        """
        return message.strip()
    
    def create_special_milestone_message(self, days):
        """Create a special milestone celebration message with random variations."""
        quote = get_random_quote()
        advice = get_random_advice()
        
        celebration_emojis = [
            "🎉🎊🥳🎈🎁💐🌹",
            "✨🎯🌟💎👑🎂🎈",
            "🥂🍾🎊🎉💝🌺🌸",
            "💖🎉🌟🥳🎁💞🎈",
            "🌹🎂✨💐🥂🎊🌸"
        ]
        
        # Different celebration texts for milestones
        milestone_texts = {
            7: [
                "🌸 یک هفته عشق کامل! 🌸",
                "💞 هفت روز عاشقی! 💞",
                "🎉 هفت روز پر از عشق! 🎉"
            ],
            30: [
                "🌟 یک ماه عاشقانه! 🌟",
                "💖 سی روز عشق و شادی! 💖",
                "🥳 یک ماه از عشق شما! 🥳"
            ],
            100: [
                "🎯 صد روز عشق کامل! 🎯",
                "💯 یکصد روز زیبا! 💯",
                "🌟 صد روز درخشان! 🌟"
            ],
            200: [
                "🌟 دویست روز عاشقی! 🌟",
                "💫 دویست روز پر از عشق! 💫",
                "✨ دویست روز خوشبختی! ✨"
            ],
            365: [
                "🎂 یک سال کامل عشق! 🎂",
                "👑 ۳۶۵ روز عاشقی! 👑",
                "🥳 یک سال خوشبختی! 🥳"
            ],
            500: [
                "💎 پانصد روز درخشان! 💎",
                "🌟 ۵۰۰ روز فوق‌العاده! 🌟",
                "✨ پانصد روز زیبا! ✨"
            ],
            1000: [
                "👑 هزار روز عاشقی! 👑",
                "🏆 ۱۰۰۰ روز عشق! 🏆",
                "💎 هزار روز خوشبختی! 💎"
            ]
        }
        
        # Random celebration messages
        celebration_messages = [
            f"💕 امروز روز خاصی است! {days} روز از عشق زیبای شما می‌گذرد!",
            f"🎊 چه روز فوق‌العاده‌ای! {days} روز عشق و خوشبختی!",
            f"✨ این یک نقطه عطف است! {days} روز عاشقی!",
            f"🥳 جشن گرفتنی است! {days} روز عشق جاودان!",
            f"💖 لحظه‌ای ویژه! {days} روز از داستان عاشقانه‌تان!",
            f"🌹 روزی برای جشن! {days} روز عشق بی‌نهایت!",
            f"💞 یک روز خاص دیگر! {days} روز از عشق شما!"
        ]
        
        # Random endings
        endings = [
            "این لحظه‌های خاص را جشن بگیرید! 🥂",
            "عشق شما قابل ستایش است! 🌹",
            "به این مسیر زیبا ادامه دهید! 💕",
            "عاشقانه‌تان جاودانه باد! 💖",
            "لحظات خوشبختی‌تان بی‌پایان! ✨",
            "این عشق را برای همیشه گرامی بدارید! 💞",
            "عشق شما همیشه می‌درخشد! 🌟"
        ]
        
        emoji_set = random.choice(celebration_emojis)
        
        if days in milestone_texts:
            special_text = random.choice(milestone_texts[days])
        else:
            special_text = f"✨ {days} روز فوق‌العاده! ✨"
        
        celebration_msg = random.choice(celebration_messages)
        ending = random.choice(endings)
        
        message = f"""
{emoji_set}

{special_text}

{celebration_msg}

💝 {quote}

💡 توصیه امروز: {advice}

{ending}

{emoji_set}
        """
        return message.strip()
    
    def send_birthday_message(self, partner_name):
        """Send birthday message for a partner."""
        try:
            days = calculate_days_together(self.config.relationship_start_date)
            quote = get_random_quote()
            advice = get_random_advice()
            
            message = f"""
🎂🎉 تولدت مبارک {partner_name} عزیز! 🎉🎂

🌹 امروز روز {days} از عشق شماست و همزمان روز تولد یکی از عاشقان زیبای این رابطه!

💝 {quote}

💡 توصیه امروز: {advice}

🎁 با عشق فراوان تولدت را تبریک می‌گویم!

🥳🎈🎊
            """
            
            self.bot.send_message(self.config.group_id, message)
            logger.info(f"✅ Birthday message sent for {partner_name}")
            
        except Exception as e:
            logger.error(f"❌ Error sending birthday message: {e}")
    
    def start_polling(self):
        """Start the bot polling."""
        try:
            # Clear any existing webhooks to avoid conflicts
            self.bot.remove_webhook()
            logger.info("✅ Cleared any existing webhooks")
            
            # Start polling with error recovery
            self.bot.infinity_polling(
                timeout=10, 
                long_polling_timeout=5,
                restart_on_change=False,
                skip_pending=True
            )
        except Exception as e:
            logger.error(f"❌ Error in bot polling: {e}")
            # Wait before retrying
            import time
            time.sleep(30)
            logger.info("🔄 Restarting bot polling...")
            self.start_polling()