from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from chalicelib.messages.en import Messages


def feature_explanation_given_keyboard(vocab: Messages):
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, selective=True
    )
    keyboard.row(KeyboardButton(vocab.feature_reason_explained))
    return keyboard


def confirmation_keyboard(vocab: Messages):
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, selective=True
    )
    keyboard.row(KeyboardButton(vocab.yes_do_it), KeyboardButton(vocab.no_cancel))
    return keyboard


def anon_message_reply_markup(sender_tg_id, message_id):
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Reply", callback_data=f"reply_{sender_tg_id}_{message_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Block", callback_data=f"block_{sender_tg_id}"
                ),
            ]
        ]
    )
