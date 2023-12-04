from enum import Enum, auto

from telebot.types import ForceReply, Message, ReplyKeyboardRemove

from chalicelib import app_config, keyboards
from chalicelib.bot import bot
from chalicelib.messages.en import Messages
from chalicelib.utils import set_user_state


class States(Enum):
    ASKED = auto()
    WHY = auto()


@bot.message_handler(commands=["feature"])
def feature_request(message: Message, data):
    vocab: Messages = data["messages"]
    set_user_state(message, States.ASKED.name)
    bot.reply_to(
        message,
        vocab.feature_request,
        reply_markup=ForceReply(selective=True),
    )


@bot.message_handler(func=lambda message: message.user_state.state == States.ASKED.name)
def feature_received(message: Message, data):
    vocab: Messages = data["messages"]
    feature = message.text
    if not feature.strip():
        bot.reply_to(
            message,
            vocab.empty_feature,
            reply_markup=ForceReply(selective=True),
        )
        return

    set_user_state(message, States.WHY.name, feature)
    bot.reply_to(
        message,
        vocab.why_feature,
        reply_markup=keyboards.feature_explanation_given_keyboard(vocab),
    )


@bot.message_handler(func=lambda msg: msg.user_state.state == States.WHY.name)
def explained(message: Message, data):
    vocab: Messages = data["messages"]
    feature = message.user_state.data
    explanation = message.text
    set_user_state(message, None)
    bot.reply_to(
        message, vocab.thank_you, reply_markup=ReplyKeyboardRemove(selective=True)
    )
    bot.send_message(
        app_config.ADMIN_TG_ID, f"*Feature request*\n\n{feature}\n\n{explanation}"
    )
