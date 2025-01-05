from telegram import Update
from telegram.ext import CallbackContext
from utils.formatter import format_courses
from utils.sorter import sort_courses
import state


async def filter_courses(update: Update, context: CallbackContext):
    """Filter courses by criteria"""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide filter criteria.")
        return

    filtered_courses = [
        course
        for course in state.cached_courses
        if (
            query.lower() in course["faculty_name"].lower()
            or query.lower() in course["course_code_section"].lower()
            or query.lower() in course["schedule"].lower()
        )
    ]

    sorted_courses = sort_courses(filtered_courses)
    response = format_courses(sorted_courses)
    await update.message.reply_text(response)
