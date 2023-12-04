from random import choice
from string import ascii_lowercase, digits

from .models import BlockedDR, ChatCodeDR, ChatCodeSerializer


def is_user_blocked(user_id, chat_id):
    """
    Checks if user_id is blocked from sending messages to chat_id
    """
    try:
        BlockedDR.get(chat_id, user_id)
        return True
    except BlockedDR.DoesNotExist:
        return False


def block_user(user_id, chat_id):
    """
    Blocks user_id from sending messages to chat_id
    """
    BlockedDR(chat_id, user_id).save()


def get_chat_id_from_code(code):
    """
    Returns the chat_id related to the given anonymous code
    """
    if not isinstance(code, str) or code == "":
        raise ValueError("Invalid code.")
    try:
        record = ChatCodeDR.get(code)
        return record.chat_id
    except ChatCodeDR.DoesNotExist:
        raise ValueError("Code does not exist.")


def delete_anonymous_code(code):
    ChatCodeDR(code).delete()


def get_code_by_chat(chat_id):
    """
    Returns the current anonymous code for this chat_id - returns None if none exists.
    """
    codes = [x.code for x in ChatCodeDR.by_chat_id_index.query(chat_id)]
    if len(codes) == 0:
        return None
    return codes[0]


def delete_code_by_chat(chat_id):
    code = get_code_by_chat(chat_id)
    if code is not None:
        delete_anonymous_code(code)


def create_new_anonymous_code(chat_id) -> ChatCodeSerializer:
    """
    Creates a new anonymous code for chat_id and deletes any existing ones
    """
    existing_code = get_code_by_chat(chat_id)
    if existing_code is not None:
        delete_anonymous_code(existing_code)

    def new_code():
        return "".join(choice(ascii_lowercase + digits) for _ in range(7))

    code = new_code()
    while True:
        try:
            _ = get_chat_id_from_code(code)
            # Code exists...
            code = new_code()
        except ValueError:
            # Does not exist!
            break

    chat_code = ChatCodeDR(code, chat_id=chat_id)
    chat_code.save()
    return ChatCodeSerializer.from_record(chat_code)


def find_random_receiver():
    pass
