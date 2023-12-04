import typing as t
from abc import ABC
from enum import Enum

from chalice import Response
from pydantic import BaseModel as PydanticModel
from pynamodb.models import Model as PynamoModel
from telebot.types import Message

from chalicelib import app_config
from chalicelib.chat_states import drivers as chat_states_drivers


class BasePynamoModelMeta:
    region = app_config.THE_AWS_REGION
    host = app_config.DYNAMODB_HOST
    billing_mode = "PAY_PER_REQUEST"


class BaseSerializer(ABC, PydanticModel):
    @classmethod
    def from_record(cls, record: PynamoModel):
        """
        Creates the data model from a given db record. Returns the data object.
        """
        return cls(**record.attribute_values)


class ResponseCodes(Enum):
    """
    The response codes to be used with `make_response`. They can contain custom codes as well.
    """

    SUCCESS = 200, "Success"
    CREATED = 201, "Created"
    BAD_REQUEST = 400, "BadRequest"
    NOT_FOUND = 404, "NotFound"
    INTERNAL_ERROR = 500, "InternalServerError"


def make_response(message, result=None, response_code: ResponseCodes = None):
    """
    The global response format to be used by all APIs
    Pass response_code as None if you want Success code.
    The reason we have a Code and a status code is because Chalice has them and we want the API to
    be consistent.
    """
    if response_code is None:
        response_code = ResponseCodes.SUCCESS
    elif not isinstance(response_code, ResponseCodes):
        raise ValueError

    response = {"Message": message, "Code": response_code.value[1]}
    if result is not None:
        response["Result"] = result

    return Response(
        body=response,
        headers={"Content-Type": "application/json"},
        status_code=response_code.value[0],
    )


def set_user_state(message: Message, state: t.Optional[str], data=None):
    chat_states_drivers.set_user_state_in_chat(
        message.chat.id, message.from_user.id, state, data
    )
