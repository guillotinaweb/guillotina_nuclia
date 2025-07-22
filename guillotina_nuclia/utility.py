from nuclia import sdk
from nuclia.lib.nua_responses import ChatModel
from guillotina_nuclia.interfaces.chat import IChat
from guillotina.async_util import IAsyncUtility
from guillotina.utils import get_authenticated_user_id
from guillotina.event import notify
from guillotina.events import ObjectModifiedEvent

import logging

logger = logging.getLogger("nuclia_utility")


class INucliaUtility(IAsyncUtility):
    pass


class NucliaUtility:
    def __init__(self, settings=None, loop=None):
        self._settings = settings
        self.loop = loop
        self._nuclia_auth = sdk.AsyncNucliaAuth()
        self._predict = sdk.AsyncNucliaPredict()
        self._upload = sdk.AsyncNucliaUpload()

    async def initialize(self, app):
        try:
            await self.auth()
        except Exception:
            logger.error("Error auth", exc_info=True)

    async def auth(self):
        client_id = await self._nuclia_auth.nua(token=self._settings["nua_key"])
        self._nuclia_auth._config.set_default_nua(client_id)

    async def upload(self, file_path: str):
        await self._upload.file(path=file_path)

    async def predict(self, question: str, chat: IChat):
        try:
            user = get_authenticated_user_id()
        except Exception:
            user = "UNKNOWN"
        generative_model = self._settings.get("generative_model", "chatgpt4o")
        max_tokens = self._settings.get("max_tokens", 4096)
        chat_model = ChatModel(
            question=question,
            query_context=chat.context or [],
            chat_history=chat.history or [],
            user_id=user,
            generative_model=generative_model,
            max_tokens=max_tokens,
        )
        response = await self._predict.generate(text=chat_model)
        chat.history.append(question)
        chat.responses.append(response)
        chat.registry()
        await notify(
            ObjectModifiedEvent(
                chat, payload={"history": chat.history, "responses": chat.responses}
            )
        )
        return response
