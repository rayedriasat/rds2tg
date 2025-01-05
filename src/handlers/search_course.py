from telegram import Update
from telegram.ext import CallbackContext
from utils.formatter import format_courses
from utils.sorter import sort_courses
import logging
import state

logger = logging.getLogger(__name__)


async def search_course(update: Update, context: CallbackContext):
    query = " ".join(context.args).lower()
    if not query:
        await update.message.reply_text("Please provide a search query.")
        return

    logger.info(f"cached_courses length: {len(state.cached_courses)}")

    filtered_courses = [
        course
        for course in state.cached_courses
        if query in course["course_code_section"].lower()
    ]

    sorted_courses = sort_courses(filtered_courses)
    response = format_courses(sorted_courses)
    await update.message.reply_text(response)
