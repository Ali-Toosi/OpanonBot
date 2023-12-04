from enum import Enum, auto

from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove

from chalicelib.bot import bot
from chalicelib.chat_codes import drivers
from chalicelib.chat_states.drivers import set_user_state_in_chat
from chalicelib.keyboards import anon_message_reply_markup
from chalicelib.messages.en import Messages
from chalicelib.utils import set_user_state


class States(Enum):
    AWAITING_MESSAGE = auto()


@bot.message_handler(func=lambda msg: msg.text.startswith("/start C"))
def start_chat(message: Message, data):
    vocab: Messages = data["messages"]

    user_id = message.from_user.id

    code = message.text[len("/start C") :]  # noqa: E203
    try:
        dst_chat_id = drivers.get_chat_id_from_code(code)

        if drivers.is_user_blocked(user_id, dst_chat_id):
            bot.reply_to(
                message, vocab.send_blocked, reply_markup=ReplyKeyboardRemove()
            )
            set_user_state(message, None)
            return

        if dst_chat_id == message.chat.id:
            bot.reply_to(
                message, vocab.no_self_messaging, reply_markup=ReplyKeyboardRemove()
            )
            set_user_state(message, None)
            return

        set_user_state(
            message, States.AWAITING_MESSAGE.name, {"recipient": dst_chat_id}
        )
        bot.reply_to(
            message, vocab.send_ask_message, reply_markup=ReplyKeyboardRemove()
        )
    except ValueError:
        bot.reply_to(
            message, vocab.send_link_not_found, reply_markup=ReplyKeyboardRemove()
        )
        return


@bot.message_handler(
    func=lambda msg: msg.user_state.state == States.AWAITING_MESSAGE.name,
    content_types=[
        "text",
        "audio",
        "document",
        "animation",
        "game",
        "photo",
        "sticker",
        "video",
        "video_note",
        "voice",
        "location",
        "contact",
        "venue",
        "dice",
        "invoice",
        "poll",
        "passport_data",
        "user_shared",
        "chat_shared",
        "story",
    ],
)
def received_anon_message(message: Message, data):
    vocab: Messages = data["messages"]

    user_id = message.from_user.id
    dst_chat_id = message.user_state.data["recipient"]
    reply_to_message_id = message.user_state.data.get("reply_to")

    try:
        if reply_to_message_id is None:
            reply_to_message_id = bot.send_message(
                dst_chat_id, vocab.new_anonymous_chat
            ).message_id
        bot.copy_message(
            dst_chat_id,
            user_id,
            message.message_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=anon_message_reply_markup(user_id, message.message_id),
        )
        bot.reply_to(message, vocab.send_successful)
    except ApiTelegramException:
        bot.reply_to(message, vocab.send_failed)

    set_user_state(message, None)


@bot.callback_query_handler(
    lambda callback_query: str(callback_query.data).startswith("reply_")
)
def reply_request(callback_query: CallbackQuery, data):
    vocab: Messages = data["messages"]

    user_id = callback_query.from_user.id
    dst_chat_id, message_id = callback_query.data.split("_")[1:]

    bot.answer_callback_query(callback_query.id)

    if drivers.is_user_blocked(user_id, int(dst_chat_id)):
        set_user_state_in_chat(callback_query.message.chat.id, user_id, None)
        bot.send_message(
            user_id, vocab.send_blocked, reply_markup=ReplyKeyboardRemove()
        )
        return

    set_user_state_in_chat(
        callback_query.message.chat.id,
        user_id,
        States.AWAITING_MESSAGE.name,
        {"recipient": dst_chat_id, "reply_to": message_id},
    )
    bot.send_message(
        user_id, vocab.send_ask_message, reply_markup=ReplyKeyboardRemove()
    )
