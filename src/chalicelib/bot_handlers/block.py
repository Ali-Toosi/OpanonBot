from enum import Enum, auto

from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove

from chalicelib.bot import bot
from chalicelib.chat_codes import drivers
from chalicelib.chat_states.drivers import set_user_state_in_chat
from chalicelib.keyboards import confirmation_keyboard
from chalicelib.messages.en import Messages
from chalicelib.utils import set_user_state


class States(Enum):
    CONFIRM = auto()


@bot.callback_query_handler(
    lambda callback_query: str(callback_query.data).startswith("block_")
)
def block_request(callback_query: CallbackQuery, data):
    vocab: Messages = data["messages"]

    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    sender_user_id = callback_query.data.split("_")[1]

    bot.answer_callback_query(callback_query.id)

    set_user_state_in_chat(chat_id, user_id, States.CONFIRM.name, sender_user_id)
    bot.send_message(
        chat_id, vocab.block_confirmation, reply_markup=confirmation_keyboard(vocab)
    )


@bot.message_handler(func=lambda msg: msg.user_state.state == States.CONFIRM.name)
def block_confirmation(message: Message, data):
    vocab: Messages = data["messages"]

    if message.text == vocab.yes_do_it:
        user_to_block = int(message.user_state.data)
        chat_id = message.chat.id
        set_user_state(message, None)
        drivers.block_user(user_to_block, chat_id)
        bot.reply_to(message, vocab.user_blocked, reply_markup=ReplyKeyboardRemove())
    elif message.text == vocab.no_cancel:
        set_user_state(message, None)
        bot.reply_to(message, vocab.block_cancelled)
    else:
        bot.reply_to(message, vocab.confirmation_keyboard_ignored)
