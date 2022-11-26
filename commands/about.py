from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


async def about(update: Update, context: CallbackContext) -> None:
    """About the app"""
    about_message = (
        "All data was extracted from ebird.\n\n"
        "If you wanna learn more about birds, visit their website\n\n"
        "Every contributor (photo or audio) retains full copyright about the material\n\n"
        "This bot does not have any commercial or monetary purpose\n\n"
        "Made by: Isaac152, a bird lover\n\n"
        "Long live the birds \U0001F989 \U0001F427 \U0001F986\n\n"
    )
    await update.message.reply_text(about_message)


about_command = CommandHandler("about", about)
