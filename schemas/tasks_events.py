from .common import BaseEvent, BaseEventData, EventTypeLiteral


class TaskStatusChangedEventData(BaseEventData):
    public_id: str
    new_status: str
    original_status: str


class TaskStatusChangedEvent(BaseEvent):
    event_name = 'TaskStatusChanged'
    event_type: EventTypeLiteral = 'business'
    version = 1
    data: TaskStatusChangedEventData


class TaskCreatedUpdatedEventData(BaseEventData):
    public_id: str
    reporter: str
    assignee: str
    description: str
    status: str
    title: str
    jira_id: str


class TaskCreatedEvent(BaseEvent):
    event_name = 'TaskCreated'
    event_type: EventTypeLiteral = 'data_stream'
    version = 1
    data: TaskCreatedUpdatedEventData


class TaskUpdatedEvent(BaseEvent):
    event_name = 'TaskUpdated'
    event_type: EventTypeLiteral = 'data_stream'
    version = 1
    data: TaskCreatedUpdatedEventData


class TaskDeletedEventData(BaseEventData):
    public_id: str


class TaskDeletedEvent(BaseEvent):
    event_name = 'TaskDeleted'
    event_type: EventTypeLiteral = 'data_stream'
    version = 1
    data: TaskDeletedEventData
