import pytest
from challenge import create_app
from challenge.settings import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app
