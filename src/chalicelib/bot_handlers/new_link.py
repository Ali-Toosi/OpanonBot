from enum import Enum, auto

from telebot.types import Message, ReplyKeyboardRemove

from chalicelib.bot import bot
from chalicelib.chat_codes.drivers import (
    create_new_anonymous_code,
    delete_code_by_chat,
    get_code_by_chat,
)
from chalicelib.keyboards import confirmation_keyboard
from chalicelib.messages.en import Messages
from chalicelib.utils import set_user_state


class States(Enum):
    CONFIRM_REVOKE = auto()


@bot.message_handler(commands=["new_link"])
def new_link(message: Message, data):
    vocab: Messages = data["messages"]

    # We get the chat id, but since the bot only allows private chat, this is the same as user id
    chat_id = message.chat.id
    existing_code = get_code_by_chat(chat_id)
    if existing_code is None:
        set_user_state(message, None)
        new_code = create_new_anonymous_code(chat_id).code
        bot.reply_to(message, vocab.new_link_created)
        bot.send_message(
            message.chat.id,
            f"https://t.me/{bot.username}?start=C{new_code}",
            disable_web_page_preview=True,
        )
    else:
        set_user_state(message, States.CONFIRM_REVOKE.name)
        bot.reply_to(
            message,
            vocab.new_link_confirmation,
            reply_markup=confirmation_keyboard(vocab),
        )


@bot.message_handler(
    func=lambda msg: msg.user_state.state == States.CONFIRM_REVOKE.name
)
def revoke_confirmation_response(message: Message, data):
    vocab: Messages = data["messages"]

    if message.text == vocab.yes_do_it:
        set_user_state(message, None)
        delete_code_by_chat(message.chat.id)
        new_code = create_new_anonymous_code(message.chat.id).code
        bot.reply_to(message, vocab.new_link_created)
        bot.send_message(
            message.chat.id,
            f"https://t.me/{bot.username}?start=C{new_code}",
            disable_web_page_preview=True,
        )
    elif message.text == vocab.no_cancel:
        set_user_state(message, None)
        bot.reply_to(
            message,
            vocab.delete_link_cancelled,
            reply_markup=ReplyKeyboardRemove(selective=True),
        )
    else:
        bot.reply_to(message, vocab.confirmation_keyboard_ignored)
