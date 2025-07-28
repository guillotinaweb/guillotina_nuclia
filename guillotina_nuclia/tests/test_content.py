import asyncio
import json
import pytest


pytestmark = pytest.mark.asyncio


async def test_addon(guillotina):
    response, status = await guillotina(
        "POST", "/db/guillotina/@addons", data=json.dumps({"id": "nuclia"})
    )
    assert status == 200
    response, status = await guillotina("GET", "/db/guillotina/chats")
    assert status == 200

    response, status = await guillotina(
        "POST",
        "/db/guillotina/chats",
        data=json.dumps({"@type": "Chat", "id": "foo_chat"}),
    )
    assert status == 201


# Tetsing needs NUA key
async def test_api(guillotina):
    await asyncio.sleep(5)
    response, status = await guillotina(
        "POST", "/db/guillotina/@addons", data=json.dumps({"id": "nuclia"})
    )
    assert status == 200
    response, status = await guillotina(
        "POST",
        "/db/guillotina/chats",
        data=json.dumps({"@type": "Chat", "id": "foo_chat"}),
    )
    assert status == 201
    response, status = await guillotina(
        "POST",
        "/db/guillotina/chats/foo_chat/@NucliaPredict",
        data=json.dumps({"question": "Foo question"}),
    )
    assert status == 200

    response, status = await guillotina("GET", "/db/guillotina/chats/foo_chat/")
    assert status == 200
    assert response["history"] == [
        {"author": "USER", "text": "Foo question"},
        {"author": "NUCLIA", "text": "Not enough data to answer this."},
    ]
    assert response["responses"] == ["Not enough data to answer this."]

    response, status = await guillotina(
        "POST",
        "/db/guillotina/chats/foo_chat/@NucliaPredict",
        data=json.dumps({"question": "Foo question 2"}),
    )
    assert status == 200
    response, status = await guillotina("GET", "/db/guillotina/chats/foo_chat/")
    assert response["history"] == [
        {"author": "USER", "text": "Foo question"},
        {"author": "NUCLIA", "text": "Not enough data to answer this."},
        {"author": "USER", "text": "Foo question 2"},
        {"author": "NUCLIA", "text": "Not enough data to answer this."},
    ]
    response, status = await guillotina(
        "GET", "/db/guillotina/@NucliaAsk?question=Foo question"
    )
    assert status == 200
    assert response == "Not enough data to answer this."

    response, status = await guillotina(
        "GET", "/db/guillotina/@NucliaAskStream?question=Foo question"
    )
    assert status == 200
    assert response == b"Not enough data to answer this."

    response, status = await guillotina(
        "GET", "/db/guillotina/@NucliaSearch?question=Foo question"
    )
    assert status == 200
    assert response == []

    response, status = await guillotina(
        "GET", "/db/guillotina/@NucliaFind?question=Foo question"
    )
    assert status == 200
    assert len(response) == 15
