from telebot.types import Message, ReplyKeyboardRemove

from chalicelib.bot import bot
from chalicelib.chat_codes import drivers
from chalicelib.messages.en import Messages
from chalicelib.utils import set_user_state


@bot.message_handler(commands=["my_link"])
def get_my_link(message: Message, data):
    vocab: Messages = data["messages"]
    set_user_state(message, None)
    chat_id = message.chat.id

    code = drivers.get_code_by_chat(chat_id)
    if code is None:
        code = drivers.create_new_anonymous_code(chat_id).code

    bot.reply_to(
        message, vocab.show_link, reply_markup=ReplyKeyboardRemove(selective=True)
    )
    bot.send_message(
        chat_id,
        f"https://t.me/{bot.username}?start=C{code}",
        disable_web_page_preview=True,
    )
