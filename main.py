#!/usr/bin/env python3
"""
Main entry point for the Telegram relationship bot.
This file starts the Flask keep-alive server and the bot scheduler.
"""

import threading
import time
import logging
from bot import RelationshipBot
from keep_alive import keep_alive
from scheduler import start_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot and keep-alive server."""
    try:
        logger.info("🚀 Starting Telegram Relationship Bot...")
        
        # Start the keep-alive server in a separate thread
        keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
        keep_alive_thread.start()
        logger.info("✅ Keep-alive server started")
        
        # Initialize the bot
        bot = RelationshipBot()
        
        # Start the scheduler in a separate thread
        scheduler_thread = threading.Thread(target=start_scheduler, args=(bot,), daemon=True)
        scheduler_thread.start()
        logger.info("✅ Message scheduler started")
        
        # Start the bot polling
        logger.info("✅ Bot is now running and listening for messages...")
        bot.start_polling()
        
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
        raise

if __name__ == "__main__":
    main()
