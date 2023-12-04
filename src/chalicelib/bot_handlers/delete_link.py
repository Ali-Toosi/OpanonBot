from enum import Enum, auto

from telebot.types import Message, ReplyKeyboardRemove

from chalicelib.bot import bot
from chalicelib.chat_codes.drivers import delete_code_by_chat, get_code_by_chat
from chalicelib.keyboards import confirmation_keyboard
from chalicelib.messages.en import Messages
from chalicelib.utils import set_user_state


class States(Enum):
    CONFIRM_DELETE = auto()


@bot.message_handler(commands=["delete_link"])
def delete_link(message: Message, data):
    vocab: Messages = data["messages"]

    code = get_code_by_chat(message.chat.id)
    if code is None:
        set_user_state(message, None)
        bot.reply_to(
            message, vocab.delete_link_no_link, reply_markup=ReplyKeyboardRemove()
        )
    else:
        set_user_state(message, States.CONFIRM_DELETE.name)
        bot.reply_to(
            message,
            vocab.delete_link_confirmation,
            reply_markup=confirmation_keyboard(vocab),
        )


@bot.message_handler(
    func=lambda msg: msg.user_state.state == States.CONFIRM_DELETE.name
)
def confirmation(message: Message, data):
    vocab: Messages = data["messages"]

    if message.text == vocab.yes_do_it:
        set_user_state(message, None)
        delete_code_by_chat(message.chat.id)
        bot.reply_to(message, vocab.delete_link_deleted)
    elif message.text == vocab.no_cancel:
        set_user_state(message, None)
        bot.reply_to(message, vocab.delete_link_cancelled)
    else:
        bot.reply_to(message, vocab.confirmation_keyboard_ignored)
