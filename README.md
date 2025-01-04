# Telegram Course Bot

This project is a Telegram bot that scrapes course data from North South University and allows students to retrieve filtered course information in a concise, spreadsheet-like format.

## Features

- Scrapes course data including course code, faculty name, schedule, and available seats.
- Allows users to search for specific courses and filter results by faculty, section, or schedule.
- Provides a help command to guide users on how to use the bot.

## Project Structure

```
telegram-course-bot
├── src
│   ├── bot.py               # Main entry point for the Telegram bot
│   ├── scraper.py           # Logic for scraping course data
|   ├── config.py                # Configuration settings for the bot
│   ├── handlers
│   │   ├── search_course.py  # Handles the /searchcourse command
│   │   ├── filter_course.py  # Handles the /filter command
│   │   └── help.py          # Handles the /help command
│   └── utils
│       └── formatter.py     # Utility functions for formatting data
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd telegram-course-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your bot token in `config.py`.

## Usage

- Start the bot by running:
  ```
  python src/bot.py
  ```

- Use the following commands in Telegram:
  - `/search <course_code>`: Search for a specific course.
  - `/filter <criteria>`: Filter courses by faculty, section, or schedule.
  - `/help`: Get a list of available commands.

## Deployment

To deploy the bot, consider using a cloud platform like Heroku, AWS, or Google Cloud. Ensure that the bot is running continuously to handle user requests.

## Contributing

Feel free to submit issues or pull requests to improve the bot's functionality.
