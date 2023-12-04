import telebot
from telebot.types import CallbackQuery

from chalicelib.app_config import BOT_TOKEN_EN
from chalicelib.chat_states import drivers as chat_states_drivers
from chalicelib.messages import en, fa

bot = telebot.TeleBot(
    BOT_TOKEN_EN, threaded=False, parse_mode="MARKDOWN", use_class_middlewares=True
)


class AllUpdatesMiddleware(telebot.handler_backends.BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.update_sensitive = False
        self.update_types = ["message", "callback_query"]

    def pre_process(self, message, data):
        if bot.lang == "fa":
            data["messages"] = fa.Messages
        elif bot.lang == "en":
            data["messages"] = en.Messages

    def post_process(self, message, data, exception):
        pass


class MessagesMiddleware(telebot.handler_backends.BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.update_sensitive = True
        self.update_types = ["message"]

    def pre_process_message(self, message: telebot.types.Message, data):
        # Load the user's state in chat
        message.user_state = chat_states_drivers.get_user_state_in_chat(
            message.chat.id, message.from_user.id
        )

    def post_process_message(self, message, data, exception):
        pass


class CallbackMiddleware(telebot.handler_backends.BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.update_sensitive = True
        self.update_types = ["callback_query"]

    def pre_process_callback_query(self, callback_query: CallbackQuery, data):
        # Load the user's state in chat
        callback_query.user_state = chat_states_drivers.get_user_state_in_chat(
            callback_query.message.chat.id, callback_query.from_user.id
        )

    def post_process_callback_query(self, message, data, exception):
        pass


for middleware_class in [AllUpdatesMiddleware, MessagesMiddleware, CallbackMiddleware]:
    bot.setup_middleware(middleware_class())


def avoid_circular_import():
    # This import is necessary so the handlers will be registered
    from chalicelib import bot_handlers as _  # noqa: F401


avoid_circular_import()
