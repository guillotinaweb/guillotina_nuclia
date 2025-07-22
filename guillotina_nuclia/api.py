from guillotina import configure
from guillotina.api.service import Service
from guillotina.component import query_utility
from guillotina_nuclia.interfaces.chat import IChat
from guillotina_nuclia.utility import INucliaUtility


@configure.service(
    context=IChat,
    method="POST",
    permission="nuclia.Predict",
    name="@predict",
    summary="Get a response",
    responses={"200": {"description": "Get a response", "schema": {"properties": {}}}},
    requestBody={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Question",
                            "required": True,
                        },
                    }
                }
            }
        },
    },
)
class PredictChat(Service):
    async def __call__(self):
        nuclia_utility = query_utility(INucliaUtility)
        payload = await self.request.json()
        return await nuclia_utility.predict(
            question=payload["question"], chat=self.context
        )
