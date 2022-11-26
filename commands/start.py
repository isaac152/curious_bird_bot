from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


async def start(update: Update, context: CallbackContext) -> None:
    """Starts the conversation"""
    welcome_message = (
        "So you like birds? Me too!\n\n"
        "You can interact with me by the following commands: \n\n"
        "/game -> Guess the bird by sound or photo, is really fun, you should try it\n\n"
        "/surpriseme -> I will send you a random bird with their description, photo and audio\n\n"
        "/about -> Copyright about the content\n\n"
        "I hope we can learn a lot together.\n\n"
    )
    await update.message.reply_text(welcome_message)


start_command = CommandHandler(["start", "help"], start)
