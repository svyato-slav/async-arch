from .common import BaseEvent, BaseEventData, EventTypeLiteral


class AccountRoleChangedEventData(BaseEventData):
    public_id: str
    new_role: str
    original_role: str


class AccountRoleChangedEvent(BaseEvent):
    event_name = 'AccountRoleChanged'
    event_type: EventTypeLiteral = 'business'
    version = 1
    data: AccountRoleChangedEventData


class AccountCreatedUpdatedEventData(BaseEventData):
    public_id: str
    username: str
    email: str
    full_name: str
    role: str


class AccountCreatedEvent(BaseEvent):
    event_name = 'AccountCreated'
    event_type: EventTypeLiteral = 'data_stream'
    version = 1
    data: AccountCreatedUpdatedEventData


class AccountUpdatedEvent(BaseEvent):
    event_name = 'AccountUpdated'
    event_type: EventTypeLiteral = 'data_stream'
    version = 1
    data: AccountCreatedUpdatedEventData


class AccountDeletedEventData(BaseEventData):
    public_id: str


class AccountDeletedEvent(BaseEvent):
    event_name = 'AccountDeleted'
    event_type: EventTypeLiteral = 'data_stream'
    version = 1
    data: AccountDeletedEventData
