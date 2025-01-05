from telegram import Update
from telegram.ext import CallbackContext


async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "Available Commands:\n"
        "/search <course_code_or_name> - Search for a specific course.\n"
        "/filter <criteria> - Filter courses by faculty, section, or schedule.\n"
        "/watch <course> - Add a course to your watch list (e.g., CSE115 or CSE115.1).\n"
        "/remove <course> - Remove a course from your watch list.\n"
        "/reset - Clear your entire watch list.\n"
        "/show - Display your current watch list.\n"
        "/help - Show this help message."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)
