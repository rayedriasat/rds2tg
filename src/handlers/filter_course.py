from telegram import Update
from telegram.ext import CallbackContext
from scraper import scrape_courses
from utils.formatter import format_courses
from utils.sorter import sort_courses


async def filter_courses(update, context):
    """Filter courses by criteria"""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide filter criteria.")
        return

    courses = scrape_courses()
    filtered_courses = [
        course
        for course in courses
        if (
            query.lower() in course["faculty_name"].lower()
            or query.lower() in course["course_code_section"].lower()
            or query.lower() in course["schedule"].lower()
        )
    ]

    # Sort the filtered courses
    sorted_courses = sort_courses(filtered_courses)

    response = format_courses(sorted_courses)
    await update.message.reply_text(response)
