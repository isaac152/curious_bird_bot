from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from models import Bird


async def send_html(update: Update, bird: Bird) -> None:
    description = bird.description if bird.description else "Not available \U0001F615"

    bird_info = (
        f"<b>Scientific Name: </b> {bird.scientific_name}\n\n"
        f"<b>Common Name: </b> {bird.common_name}\n\n"
        f"<b>Description: </b> {description}\n\n"
        f'Learn more about this awesome bird, <a href="{bird.url}">here</a>\n\n'
    )

    await update.message.reply_html(bird_info)


async def surprise_me(update: Update, context: CallbackContext) -> None:
    """Get a random bird info"""

    bird_container = context.bot_data["bird_container"]
    selected_bird = bird_container.get_random_bird()

    await update.message.reply_text("Wait please \U0001F62C")
    await update.message.reply_photo(selected_bird.get_image())
    if selected_bird.audio_id:
        await update.message.reply_audio(
            selected_bird.get_audio(), title=selected_bird.common_name
        )
    else:
        await update.message.reply_text(
            "This bird has not been recorded yet. Crazy, huh? \U0001F612 "
        )

    await send_html(update, selected_bird)


surpriseme_command = CommandHandler("surpriseme", surprise_me)
