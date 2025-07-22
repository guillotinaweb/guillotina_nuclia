from pytest_docker_fixtures import images


pytest_plugins = [
    "pytest_docker_fixtures",
    "guillotina.tests.fixtures",
    "guillotina_nuclia.tests.fixtures",
]
