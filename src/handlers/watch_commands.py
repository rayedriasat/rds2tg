from telegram import Update
from telegram.ext import CallbackContext
import state
from state import save_watchlists


async def watch_course(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    if not context.args:
        await update.message.reply_text("Please specify a course code to watch.")
        return

    course = context.args[0].upper()
    base_course = course.rstrip("L")
    lab_course = f"{base_course}L"

    if chat_id not in state.user_watchlists:
        state.user_watchlists[chat_id] = set()

    state.user_watchlists[chat_id].add(base_course)
    state.user_watchlists[chat_id].add(lab_course)
    save_watchlists()
    await update.message.reply_text(
        f"Added {base_course} and {lab_course} to your watch list."
    )


async def remove_course(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    if not context.args:
        await update.message.reply_text("Please specify a course code to remove.")
        return

    course = context.args[0].upper()
    base_course = course.rstrip("L")
    lab_course = f"{base_course}L"

    if chat_id in state.user_watchlists:
        state.user_watchlists[chat_id].discard(base_course)
        state.user_watchlists[chat_id].discard(lab_course)
        save_watchlists()
        await update.message.reply_text(
            f"Removed {base_course} and {lab_course} from your watch list."
        )
    else:
        await update.message.reply_text(
            f"Course {course} not found in your watch list."
        )


async def reset_watchlist(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    state.user_watchlists[chat_id] = set()
    save_watchlists()
    await update.message.reply_text("Your watch list has been cleared.")


async def show_watchlist(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in state.user_watchlists or not state.user_watchlists[chat_id]:
        await update.message.reply_text("Your watch list is empty.")
        return

    watchlist = sorted(state.user_watchlists[chat_id])
    response = "Your Watch List:\n" + "\n".join(watchlist)
    await update.message.reply_text(response)
