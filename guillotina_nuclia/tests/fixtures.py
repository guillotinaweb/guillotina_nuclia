from guillotina import testing
from guillotina.component import query_utility
from guillotina.tests.fixtures import _update_from_pytest_markers

import json
import os
import pytest


ELASTICSEARCH = os.environ.get("ELASTICSEARCH", "True")

annotations = {"elasticsearch": {"host": "localhost:9200"}}


def base_settings_configurator(settings):
    if "applications" not in settings:
        settings["applications"] = []
    settings["applications"].append("guillotina")
    settings["applications"].append("guillotina_nuclia")


testing.configure_with(base_settings_configurator)


@pytest.fixture(scope="function")
async def guillotina(guillotina):
    response, status = await guillotina(
        "POST", "/db/", data=json.dumps({"@type": "Container", "id": "guillotina"})
    )
    assert status == 200
    yield guillotina
