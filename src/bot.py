from telegram.ext import Application, CommandHandler, JobQueue
import logging
import asyncio
import concurrent.futures
from config import TOKEN
from handlers.search_course import search_course
from handlers.filter_course import filter_courses
from handlers.help import help_command
from handlers.watch_commands import (
    watch_course,
    remove_course,
    reset_watchlist,
    show_watchlist,
)
from utils.formatter import format_courses
from utils.sorter import sort_courses
from scraper import scrape_courses
import state

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

executor = concurrent.futures.ThreadPoolExecutor()


async def check_watchlist_changes(chat_id, filtered_courses):
    if chat_id not in state.previous_filtered_data:
        state.previous_filtered_data[chat_id] = filtered_courses
        return True  # First time, always notify

    old_data = state.previous_filtered_data[chat_id]
    has_changes = False

    if len(old_data) != len(filtered_courses):
        has_changes = True
    else:
        for old, new in zip(old_data, filtered_courses):
            if old != new:
                has_changes = True
                break

    state.previous_filtered_data[chat_id] = filtered_courses
    return has_changes


async def notify_users():
    logger.info("Notifying users about watchlist changes")
    for chat_id, watchlist in state.user_watchlists.items():
        if not watchlist:
            logger.info(f"User {chat_id} has no courses in watchlist")
            continue

        filtered_courses = []
        for course in state.cached_courses:
            course_code = course["course_code_section"]
            base_code = course_code.rstrip("L")

            if course_code in watchlist or base_code in watchlist:
                filtered_courses.append(course)

        logger.info(f"User {chat_id} filtered courses: {len(filtered_courses)}")

        if filtered_courses and await check_watchlist_changes(
            chat_id, filtered_courses
        ):
            response = format_courses(sort_courses(filtered_courses))
            try:
                await state.application.bot.send_message(
                    chat_id=chat_id, text="⚠️ Watch List Update ⚠️\n\n" + response
                )
                logger.info(f"Notification sent to user {chat_id}")
            except Exception as e:
                logger.error(f"Failed to notify user {chat_id}: {str(e)}")
        else:
            logger.info(f"No changes detected for user {chat_id}")


async def periodic_scrape(context):
    logger.info("Periodic scrape triggered")
    try:
        logger.info("Scraping course data...")
        loop = asyncio.get_running_loop()
        new_courses = await loop.run_in_executor(executor, scrape_courses)
        if new_courses:
            state.cached_courses = new_courses
            logger.info(f"Successfully scraped {len(state.cached_courses)} courses")
            # Notify after each new scrape
            await notify_users()
        else:
            logger.warning("Scraping returned no courses, keeping cached data")
    except Exception as e:
        logger.error(f"Error in periodic scrape: {str(e)}")


def main() -> None:
    logger.info("Initializing bot application...")  # Add startup log

    # Build application with job queue
    job_queue = JobQueue()
    state.application = Application.builder().token(TOKEN).job_queue(job_queue).build()

    logger.info("Setting up job queue...")  # Add setup log
    state.application.job_queue.run_repeating(periodic_scrape, interval=300, first=15)

    # Register handlers
    state.application.add_handler(CommandHandler("start", help_command))
    state.application.add_handler(CommandHandler("search", search_course))
    state.application.add_handler(CommandHandler("filter", filter_courses))
    state.application.add_handler(CommandHandler("help", help_command))
    state.application.add_handler(CommandHandler("watch", watch_course))
    state.application.add_handler(CommandHandler("remove", remove_course))
    state.application.add_handler(CommandHandler("reset", reset_watchlist))
    state.application.add_handler(CommandHandler("show", show_watchlist))

    # Start the bot
    logger.info("Starting bot...")
    state.application.run_polling()


if __name__ == "__main__":
    main()
