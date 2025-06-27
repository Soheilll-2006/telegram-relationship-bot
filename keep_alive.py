#!/usr/bin/env python3
"""
Keep-alive server for the Telegram relationship bot.
Runs a simple Flask server to keep the bot alive on Replit.
"""

from flask import Flask, jsonify, render_template_string
import threading
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple HTML template for the status page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ربات عاشقانه تلگرام</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #ff6b6b, #ee5a24, #ff7675);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
            width: 100%;
        }
        h1 {
            color: #2d3436;
            margin-bottom: 20px;
            font-size: 2.5em;
        }
        .status {
            font-size: 1.5em;
            margin: 20px 0;
            padding: 15px;
            background: #00b894;
            color: white;
            border-radius: 10px;
        }
        .info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #e17055;
        }
        .emoji {
            font-size: 3em;
            margin: 20px 0;
        }
        .time {
            color: #636e72;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">💕</div>
        <h1>ربات عاشقانه تلگرام</h1>
        <div class="status">
            ✅ ربات فعال و در حال اجرا است
        </div>
        <div class="info">
            <p><strong>📅 تاریخ:</strong> {{ current_date }}</p>
            <p><strong>⏰ زمان:</strong> {{ current_time }}</p>
            <p><strong>🤖 وضعیت:</strong> آنلاین</p>
            <p><strong>💌 پیام روزانه:</strong> فعال</p>
        </div>
        <div class="time">
            آخرین بروزرسانی: {{ current_datetime }}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page showing bot status."""
    try:
        now = datetime.now()
        return render_template_string(HTML_TEMPLATE, 
                                    current_date=now.strftime('%Y-%m-%d'),
                                    current_time=now.strftime('%H:%M:%S'),
                                    current_datetime=now.strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        logger.error(f"❌ Error rendering home page: {e}")
        return f"Bot is running! Error: {e}", 500

@app.route('/status')
def status():
    """API endpoint for bot status."""
    try:
        return jsonify({
            'status': 'online',
            'message': 'Telegram Relationship Bot is running',
            'timestamp': datetime.now().isoformat(),
            'uptime': 'Running'
        })
    except Exception as e:
        logger.error(f"❌ Error in status endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/ping')
def ping():
    """Simple ping endpoint."""
    return 'pong'

def keep_alive():
    """Start the Flask keep-alive server."""
    try:
        logger.info("🌐 Starting keep-alive server on port 5000...")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"❌ Error starting keep-alive server: {e}")

if __name__ == '__main__':
    keep_alive()
