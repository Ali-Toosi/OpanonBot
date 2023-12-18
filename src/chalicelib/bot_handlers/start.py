from telebot.types import Message, ReplyKeyboardRemove

from chalicelib.bot import bot
from chalicelib.messages.en import Messages
from chalicelib.utils import set_user_state


@bot.message_handler(func=lambda msg: msg.text == "/start")
def start(message: Message, data):
    vocab: Messages = data["messages"]
    set_user_state(message, None)
    bot.reply_to(message, vocab.start_message)


@bot.message_handler(commands=["help"])
def tips(message: Message, data):
    vocab: Messages = data["messages"]
    set_user_state(message, None)
    bot.reply_to(message, vocab.help_message, disable_web_page_preview=True)


@bot.message_handler(commands=["cancel"])
def cancel(message: Message, data):
    vocab: Messages = data["messages"]
    set_user_state(message, None)
    bot.reply_to(message, vocab.all_cancelled, reply_markup=ReplyKeyboardRemove())
