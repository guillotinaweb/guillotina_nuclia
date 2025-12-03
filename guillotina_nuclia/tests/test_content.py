import asyncio
import json
import pytest


pytestmark = pytest.mark.asyncio


async def test_addon(guillotina):
    response, status = await guillotina("POST", "/db/guillotina/@addons", data=json.dumps({"id": "nuclia"}))
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
    response, status = await guillotina("POST", "/db/guillotina/@addons", data=json.dumps({"id": "nuclia"}))
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
        "POST",
        "/db/guillotina/@NucliaAsk",
        data=json.dumps({"question": "Foo question"}),
    )
    assert status == 200
    assert response == "Not enough data to answer this."

    response, status = await guillotina(
        "POST",
        "/db/guillotina/@NucliaPredictStateless",
        data=json.dumps(
            {
                "question": "Foo question",
                "history": [
                    {"author": "USER", "text": "Foo question"},
                    {
                        "author": "NUCLIA",
                        "text": "Not enough data to answer this.",
                    },
                    {"author": "USER", "text": "Foo question 2"},
                    {
                        "author": "NUCLIA",
                        "text": "Not enough data to answer this.",
                    },
                ],
                "context": ["some context"],
            }
        ),
    )
    assert status == 200
    assert response["answer"] == "Not enough data to answer this."
    assert response["history"] == [
        {"author": "USER", "text": "Foo question"},
        {"author": "NUCLIA", "text": "Not enough data to answer this."},
        {"author": "USER", "text": "Foo question 2"},
        {"author": "NUCLIA", "text": "Not enough data to answer this."},
        {"author": "USER", "text": "Foo question"},
        {"author": "NUCLIA", "text": "Not enough data to answer this."},
    ]
    assert response["response"]["answer"] == "Not enough data to answer this."

    response, status = await guillotina(
        "POST",
        "/db/guillotina/@NucliaPredictStatelessStream",
        data=json.dumps(
            {
                "question": "Foo question",
                "history": [
                    {"author": "USER", "text": "Foo question"},
                    {
                        "author": "NUCLIA",
                        "text": "Not enough data to answer this.",
                    },
                    {"author": "USER", "text": "Foo question 2"},
                    {
                        "author": "NUCLIA",
                        "text": "Not enough data to answer this.",
                    },
                ],
                "context": ["some context"],
            }
        ),
    )
    assert status == 200
    assert response.startswith(b"Not enough data to answer this.")
    assert b'"type": "end"' in response

    response, status = await guillotina(
        "POST",
        "/db/guillotina/@NucliaAskStream",
        data=json.dumps({"question": "Foo question"}),
    )
    assert status == 200
    assert response.find(b"Not enough data to answer this.") != -1

    response, status = await guillotina(
        "POST",
        "/db/guillotina/@NucliaSearch",
        data=json.dumps({"question": "Foo question"}),
    )
    assert status == 200
    assert response == []

    response, status = await guillotina(
        "POST",
        "/db/guillotina/@NucliaFind",
        data=json.dumps({"question": "Foo question"}),
    )
    assert status == 200
    assert len(response) == 16
