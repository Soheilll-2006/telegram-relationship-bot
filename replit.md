# Telegram Relationship Bot

## Overview

This is a Telegram bot designed for couples to receive daily romantic messages and track relationship milestones. The bot sends scheduled messages in Persian/Farsi with love quotes and celebrates special occasions like anniversaries and birthdays. It's built with Python using the pyTelegramBotAPI library and runs on Replit with a Flask keep-alive server.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Bot Module**: Core Telegram bot functionality and command handlers
- **Scheduler Module**: Time-based message scheduling using the `schedule` library
- **Keep-Alive Server**: Flask web server to maintain bot availability on Replit
- **Configuration Management**: Environment-based configuration system
- **Utility Functions**: Helper functions for date calculations and message formatting

## Key Components

### Core Bot (`bot.py`)
- **Purpose**: Main bot class with message handlers
- **Key Features**: 
  - Command handlers for `/start`, `/milestone`, `/quote`
  - Daily message sending functionality
  - Integration with quotes and utilities
- **Dependencies**: pyTelegramBotAPI, config, quotes, utils

### Configuration Management (`config.py`)
- **Purpose**: Centralized configuration from environment variables
- **Key Settings**:
  - Bot token and group ID (required)
  - Relationship start date
  - Partner names and birthdays
  - Daily message timing (default: 9:00 AM)
- **Error Handling**: Validates required environment variables

### Message Scheduler (`scheduler.py`)
- **Purpose**: Automated daily message scheduling
- **Features**:
  - Daily messages at configured time
  - Birthday checking at midnight
  - Continuous scheduling loop with error handling
- **Technology**: Python `schedule` library

### Keep-Alive Server (`keep_alive.py`)
- **Purpose**: Maintains bot availability on Replit
- **Implementation**: Flask web server on port 5000
- **Features**: Status page with Persian UI showing bot status

### Quotes Database (`quotes.py`)
- **Purpose**: Collection of Persian and English love quotes
- **Content**: 35+ romantic quotes in Persian language
- **Usage**: Random quote selection for daily messages and commands

### Utility Functions (`utils.py`)
- **Purpose**: Helper functions for date calculations and formatting
- **Key Functions**:
  - Calculate days together since relationship start
  - Identify special milestones (100, 365, 1000+ days)
  - Format milestone messages with Persian text

## Data Flow

1. **Bot Initialization**: Configuration loaded from environment variables
2. **Server Start**: Flask keep-alive server starts on port 5000
3. **Scheduler Start**: Daily message scheduler begins monitoring
4. **Message Flow**:
   - Scheduled messages sent at configured time
   - Manual commands processed immediately
   - Birthday checks run daily at midnight
5. **Error Handling**: Comprehensive logging to `bot.log` file

## External Dependencies

### Required Python Packages
- **pyTelegramBotAPI**: Telegram bot API wrapper
- **Flask**: Web server for keep-alive functionality
- **schedule**: Task scheduling library

### Environment Variables (Required)
- `BOT_TOKEN`: Telegram bot token from BotFather
- `GROUP_ID`: Target Telegram group/chat ID

### Environment Variables (Optional)
- `RELATIONSHIP_START_DATE`: Start date (YYYY-MM-DD format, default: 2024-01-01)
- `PARTNER1_NAME`, `PARTNER2_NAME`: Partner names (default: Persian placeholders)
- `PARTNER1_BIRTHDAY`, `PARTNER2_BIRTHDAY`: Birthdays (MM-DD format)
- `DAILY_MESSAGE_HOUR`, `DAILY_MESSAGE_MINUTE`: Message timing (default: 9:00)

## Deployment Strategy

### Replit Configuration
- **Runtime**: Python 3.11 with Nix stable-24_05 channel
- **Workflow**: Parallel execution with automatic dependency installation
- **Port**: Flask server runs on port 5000 for keep-alive functionality
- **Process**: Single-threaded main process with multiple daemon threads

### Architecture Decisions

1. **Threading Model**: 
   - Keep-alive server runs in daemon thread
   - Scheduler runs in separate daemon thread
   - Main thread handles bot polling
   - **Rationale**: Allows concurrent operations while maintaining simplicity

2. **Persistence Strategy**:
   - No database implementation (stateless design)
   - Configuration via environment variables
   - **Rationale**: Reduces complexity for simple use case, could be extended with database later

3. **Error Handling**:
   - Comprehensive logging to file and console
   - Graceful degradation on configuration errors
   - **Rationale**: Ensures reliability and debugging capability

4. **Internationalization**:
   - Primary language: Persian/Farsi
   - RTL text support in web interface
   - **Rationale**: Designed for Persian-speaking couples

## Changelog

```
Changelog:
- June 27, 2025. Initial setup
- June 27, 2025. Configured for 24/7 operation with correct relationship dates:
  * Relationship start: June 22, 2025
  * Partner names: سهیل (September 23) and شمیم (November 7)
  * Daily messages scheduled at 9:00 AM UTC
  * Bot successfully running with command handlers and automatic scheduling
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```