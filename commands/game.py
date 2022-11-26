import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

SELECT_GAME, GUESS_AUDIO, GUESS_IMAGE, CHECK_ANSWER = range(4)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

GAME_OPTIONS = ["Guess by sound", "Guess by image"]


async def start_game(update: Update, context: CallbackContext) -> int:
    """Start the guess game"""
    reply_markup = ReplyKeyboardMarkup.from_row(GAME_OPTIONS, one_time_keyboard=True)

    await update.message.reply_text(
        "Which game do you want to play?",
        reply_markup=reply_markup,
    )
    return SELECT_GAME


async def select_game(update: Update, context: CallbackContext) -> int:
    type_game = guess_audio if "sound" in update.message.text else guess_image
    context.user_data["type_game"] = type_game

    return await type_game(update, context)


async def guess_audio(update: Update, context: CallbackContext) -> int:
    """Guess bird by audio"""

    score = context.user_data.get("score", 1)
    user = update.message.from_user.first_name

    await update.message.reply_text(
        f"Round {score}",
        reply_markup=ReplyKeyboardRemove(),
    )

    bird_container = context.bot_data["bird_container"]
    random_birds = bird_container.get_random_bird_audios()
    selected_bird = bird_container.get_random_bird(random_birds)

    random_birds_options = [bird.common_name for bird in random_birds]
    answer = selected_bird.common_name

    logger.info(f"{user} Round {score} - {answer}")

    await update.message.reply_text("Wait please,the sound is loading \U0001F62C")
    await update.message.reply_audio(selected_bird.get_audio(), title=f"Audio {score}")

    markup_options = ReplyKeyboardMarkup.from_column(
        random_birds_options, one_time_keyboard=True, selective=True
    )

    await update.message.reply_text("Guess the bird", reply_markup=markup_options)

    context.user_data["score"] = score
    context.user_data["answer"] = answer

    return CHECK_ANSWER


async def guess_image(update: Update, context: CallbackContext) -> int:
    """Guess the bird by its photo"""
    score = context.user_data.get("score", 1)
    user = update.message.from_user.first_name

    await update.message.reply_text(
        f"Round {score}",
        reply_markup=ReplyKeyboardRemove(),
    )
    bird_container = context.bot_data["bird_container"]
    random_birds = bird_container.get_random_bird_list()
    selected_bird = bird_container.get_random_bird(random_birds)

    random_birds_options = [bird.common_name for bird in random_birds]
    answer = selected_bird.common_name

    logger.info(f"{user} Round {score} - {answer}")

    await update.message.reply_text("Wait please, the image is loading \U0001F62C")

    await update.message.reply_photo(selected_bird.get_image())

    markup_options = ReplyKeyboardMarkup.from_column(
        random_birds_options, one_time_keyboard=True, selective=True
    )

    await update.message.reply_text("Guess the bird", reply_markup=markup_options)

    context.user_data["score"] = score
    context.user_data["answer"] = answer

    return CHECK_ANSWER


async def check_answer(update: Update, context: CallbackContext) -> int:
    """Check the answer to continue the game"""

    score = context.user_data.get("score")
    answer = context.user_data.get("answer")

    if update.message.text != answer:
        max_score = context.user_data.get("max_score", 0)
        context.user_data["max_score"] = score if max_score < score else max_score

        await update.message.reply_text(
            "Wrong answer, sorry \U0001F614 \n\n"
            f"The answer was {answer}]\n\n"
            f"Your score was: {score}\n\n"
            f"Your max score is: {max_score}\n\n",
            reply_markup=ReplyKeyboardRemove(),
        )
        del context.user_data["score"]

        return ConversationHandler.END

    await update.message.reply_text(
        "Nice one \U0001F601",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data["score"] += 1

    type_game = context.user_data["type_game"]

    return await type_game(update, context)


async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Bye! Have a nice day", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


start_game_command = ConversationHandler(
    entry_points=[CommandHandler("game", start_game)],
    states={
        SELECT_GAME: [
            MessageHandler(filters.Text(GAME_OPTIONS) & ~filters.COMMAND, select_game)
        ],
        CHECK_ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
