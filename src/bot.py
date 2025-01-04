from telegram.ext import Application, CommandHandler
import logging
from config import TOKEN
from handlers.search_course import search_course
from handlers.filter_course import filter_courses
from handlers.help import help_command

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error_handler(update, context):
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")


async def start(update, context):
    """Start command handler"""
    await help_command(update, context)


def main() -> None:
    # Initialize the bot
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search_course))
    application.add_handler(CommandHandler("filter", filter_courses))
    application.add_handler(CommandHandler("help", help_command))
    application.add_error_handler(error_handler)

    # Start the bot
    logger.info("Starting bot...")
    application.run_polling()


if __name__ == "__main__":
    main()
