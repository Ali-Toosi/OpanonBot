from telebot.types import Message, ReplyKeyboardRemove

from chalicelib.bot import bot
from chalicelib.messages.en import Messages


@bot.message_handler(
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
        "new_chat_members",
        "left_chat_member",
        "new_chat_title",
        "new_chat_photo",
        "delete_chat_photo",
        "group_chat_created",
        "supergroup_chat_created",
        "channel_chat_created",
        "migrate_to_chat_id",
        "migrate_from_chat_id",
        "pinned_message",
        "invoice",
        "successful_payment",
        "connected_website",
        "poll",
        "passport_data",
        "proximity_alert_triggered",
        "video_chat_scheduled",
        "video_chat_started",
        "video_chat_ended",
        "video_chat_participants_invited",
        "web_app_data",
        "message_auto_delete_timer_changed",
        "forum_topic_created",
        "forum_topic_closed",
        "forum_topic_reopened",
        "forum_topic_edited",
        "general_forum_topic_hidden",
        "general_forum_topic_unhidden",
        "write_access_allowed",
        "user_shared",
        "chat_shared",
        "story",
    ]
)
def catch_all_messages(message: Message, data):
    vocab: Messages = data["messages"]
    bot.reply_to(message, vocab.unknown_message, reply_markup=ReplyKeyboardRemove())
