import pytest


pytestmark = pytest.mark.asyncio


async def test_content(guillotina):
    response, status = await guillotina("GET", "/db/guillotina/chats")
    assert status == 200
