import typing as t

from pynamodb.attributes import JSONAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.models import Model as PynamoModel

from chalicelib import app_config
from chalicelib.utils import BasePynamoModelMeta, BaseSerializer


class ChatStateDR(PynamoModel):
    class Meta(BasePynamoModelMeta):
        table_name = app_config.DYNAMO_TABLES_PREFIX + "ChatStates"

    chat_id = NumberAttribute(hash_key=True)
    user_id = NumberAttribute(range_key=True)
    state = UnicodeAttribute()
    data = JSONAttribute(null=True)


if app_config.STAGE == "local":
    if not ChatStateDR.exists():
        ChatStateDR.create_table()


class ChatStateSerializer(BaseSerializer):
    chat_id: int
    # User id can be null if the message is in a channel. We replace this case with 0 as it should happen at most once
    # per chat_id.
    user_id: int = 0
    state: t.Optional[str] = None
    data: t.Optional[t.Union[int, str, list, dict]] = None
