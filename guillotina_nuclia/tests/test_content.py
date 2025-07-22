import pytest
import json


pytestmark = pytest.mark.asyncio


async def test_addon(guillotina):
    response, status = await guillotina(
        "POST", "/db/guillotina/@addons", data=json.dumps({"id": "nuclia"})
    )
    assert status == 200
    response, status = await guillotina("GET", "/db/guillotina/chats")
    assert status == 200
