from telegram import Update
from telegram.ext import CallbackContext


async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "Available Commands:\n"
        "/search <course_code_or_name> - Search for a specific course.\n"
        "/filter <criteria> - Filter courses by faculty, section, or schedule.\n"
        "/help - Show this help message."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)
