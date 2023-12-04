import typing as t

from .models import ChatStateDR, ChatStateSerializer


def get_user_state_in_chat(
    chat_id: int, user_id: t.Optional[int] = None
) -> ChatStateSerializer:
    """
    :param chat_id: Chat id.
    :param user_id: User id. If None, it means the message is sent in a channel. Each chat_id can have only one empty
        user_id case, which we'll replace with 0.
    :return: The user state (str)
    """
    args = {"chat_id": chat_id}
    if user_id is not None:
        args["user_id"] = user_id

    serialized_obj = ChatStateSerializer(**args)
    try:
        record = ChatStateDR.get(serialized_obj.chat_id, serialized_obj.user_id)
        return ChatStateSerializer.from_record(record)
    except ChatStateDR.DoesNotExist:
        return serialized_obj


def set_user_state_in_chat(
    chat_id: int,
    user_id: t.Optional[int] = None,
    state: t.Optional[str] = None,
    data=None,
):
    args = {"chat_id": chat_id, "state": state, "data": data}
    if user_id is not None:
        args["user_id"] = user_id

    serialized_obj = ChatStateSerializer(**args)
    if serialized_obj.state is None:
        ChatStateDR(serialized_obj.chat_id, serialized_obj.user_id).delete()
    else:
        ChatStateDR(
            serialized_obj.chat_id, serialized_obj.user_id, state=state, data=data
        ).save()
