import json

import sentry_sdk
from chalice import Chalice
from chalice.app import ForbiddenError
from sentry_sdk.integrations.chalice import ChaliceIntegration
from telebot.types import Update

from chalicelib import app_config
from chalicelib.bot import bot
from chalicelib.utils import make_response

"""
Initial configuration
Configure Sentry and initialise the app
"""

sentry_sdk.init(
    dsn=app_config.SENTRY_DSN,
    integrations=[ChaliceIntegration()],
)

app = Chalice(app_name="OpanonBot")


"""
Heartbeat for diagnostics
"""


@app.route("/heartbeat")
def heartbeat():
    return "I'm up."


@app.route("/update/{bot_token}", methods=["POST"])
def bot_webhook(bot_token):
    # Quick authenticity check
    if bot_token == str(app_config.BOT_TOKEN_EN).replace(":", ""):
        bot.lang = "en"
        bot.username = "OpanonBot"
    elif bot_token == str(app_config.BOT_TOKEN_FA).replace(":", ""):
        bot.lang = "fa"
        bot.username = "NashenasBot"
        bot.token = app_config.BOT_TOKEN_FA
    else:
        raise ForbiddenError("Incorrect bot token provided.")

    update = Update.de_json(json.dumps(app.current_request.json_body))

    # Make sure it's a private chat
    if update.message and update.message.chat.type != "private":
        bot.reply_to(update.message, "This bot only works in private chats.")
        return make_response("All done.")

    bot.process_new_updates([update])
