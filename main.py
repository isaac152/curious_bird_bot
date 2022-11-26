from telegram.ext import ApplicationBuilder

from commands import (
    about_command,
    start_command,
    start_game_command,
    surpriseme_command,
)
from constants import TELEGRAM_KEY, TIMEOUT_SECONDS
from models import BirdContainer
from utils import load_file


def main() -> None:
    """Create and run the bot."""
    bot = (
        ApplicationBuilder()
        .token(TELEGRAM_KEY)
        .read_timeout(TIMEOUT_SECONDS)
        .write_timeout(TIMEOUT_SECONDS)
    )
    bot = bot.build()
    bot.bot_data["bird_container"] = BirdContainer(load_file())
    bot.add_handler(start_command)
    bot.add_handler(about_command)
    bot.add_handler(surpriseme_command)
    bot.add_handler(start_game_command)

    bot.run_polling()


if __name__ == "__main__":
    main()
