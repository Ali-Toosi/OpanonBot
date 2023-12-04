from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model as PynamoModel

from chalicelib import app_config
from chalicelib.utils import BasePynamoModelMeta, BaseSerializer


class ChatCodeByChatIdIndex(GlobalSecondaryIndex):
    class Meta(BasePynamoModelMeta):
        index_name = "chat-codes-by-chat-id-index"
        projection = AllProjection()

    chat_id = NumberAttribute(hash_key=True)


class ChatCodeDR(PynamoModel):
    class Meta(BasePynamoModelMeta):
        table_name = app_config.DYNAMO_TABLES_PREFIX + "ChatCodes"

    code = UnicodeAttribute(hash_key=True)
    # The bot doesn't allow adding to groups, but we keep this as chat id just in case we wanna support groups later
    # Doesn't make any extra work anyway
    chat_id = NumberAttribute()

    by_chat_id_index = ChatCodeByChatIdIndex()


if app_config.STAGE == "local":
    if not ChatCodeDR.exists():
        ChatCodeDR.create_table()


class ChatCodeSerializer(BaseSerializer):
    code: str
    chat_id: int


class BlockedDR(PynamoModel):
    class Meta(BasePynamoModelMeta):
        table_name = app_config.DYNAMO_TABLES_PREFIX + "Blocks"

    blocking_chat_id = NumberAttribute(hash_key=True)
    blocked_user_id = NumberAttribute(range_key=True)


if app_config.STAGE == "local":
    if not BlockedDR.exists():
        BlockedDR.create_table()


class BlockedSerializer(BaseSerializer):
    blocking_chat_id: int
    blocked_user_id: int
