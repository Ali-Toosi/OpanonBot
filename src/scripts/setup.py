"""
These are any setup functions required to run before the project starts.
These should only run at deployments, not during runtime. That's why it's in scripts, not in the app files.
"""

import os

from telebot import TeleBot
from telebot.types import BotCommand


def setup_bot():
    """
    Setups the bot commands.
    """
    print("Setting up bot commands...")

    class CommandsEn:
        command_start = "See how everything works"
        command_help = "Tips and help for using the bot"
        command_my_link = "Get your chat link for receiving anonymous messages"
        command_new_link = "Delete your old chat link and create a new one"
        command_delete_link = "Delete your chat link and don't create a new one"
        command_cancel = "Cancel whatever is happening"

    class CommandsFa:
        command_start = "شروع و دیدن دستورها"
        command_help = "کمک در استفاده از ربات"
        command_my_link = "دریافت پیام ناشناس"
        command_new_link = "دریافت لینک ناشناس جدید"
        command_delete_link = "حذف لینک ناشناس"
        command_cancel = "هر کار دارم میکنم، کنسلش کن!"

    for token, vocab in [
        (os.environ["BOT_TOKEN_EN"], CommandsEn),
        (os.environ["BOT_TOKEN_FA"], CommandsFa),
    ]:
        commands = [
            BotCommand("start", vocab.command_start),
            BotCommand("help", vocab.command_help),
            BotCommand("my_link", vocab.command_my_link),
            BotCommand("delete_link", vocab.command_delete_link),
            BotCommand("new_link", vocab.command_new_link),
            BotCommand("cancel", vocab.command_cancel),
        ]

        try:
            TeleBot(token).set_my_commands(commands)
        except Exception as e:
            print("Bot setup failed!")
            print(e)
            exit(1)

    print("All bot commands set.")


if __name__ == "__main__":
    setup_bot()
