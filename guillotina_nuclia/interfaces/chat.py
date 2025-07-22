from guillotina.interfaces import IFolder
from guillotina.interfaces import IItem
from guillotina import schema


class IChats(IFolder):
    pass


class IChat(IItem):
    history = schema.List(
        title="Chat history",
        value_type=schema.TextLine(),
        required=False,
        default=[],
        missing_value=[],
        defaultFactory=list,
    )

    responses = schema.List(
        title="Responses",
        value_type=schema.TextLine(),
        required=False,
        default=[],
        missing_value=[],
        defaultFactory=list,
    )

    context = schema.List(
        title="Context",
        value_type=schema.TextLine(),
        required=False,
        default=[],
        missing_value=[],
        defaultFactory=list,
    )
