from guillotina import configure
from guillotina_nuclia.interfaces.chat import IChat, IChats
from guillotina.content import Item, Folder


@configure.contenttype(
    type_name="Chats",
    schema=IChats,
    behaviors=["guillotina.behaviors.dublincore.IDublinCore"],
    allowed_types=["Chat"],
    globally_addable=False,
)
class Chats(Folder):
    pass


@configure.contenttype(
    type_name="Chat",
    schema=IChat,
    add_permission="guillotina.AddContent",
    behaviors=["guillotina.behaviors.dublincore.IDublinCore"],
    globally_addable=False,
)
class Chat(Item):
    pass
