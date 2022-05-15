from pydantic import BaseModel
from typing import Literal

EventTypeLiteral = Literal["data_stream", "business"]


class BaseEventData(BaseModel):
    pass


class BaseEvent(BaseModel):
    event_name: str
    event_type: EventTypeLiteral
    data: BaseEventData
