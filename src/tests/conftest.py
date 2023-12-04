import pytest
from chalice.test import Client

import app


@pytest.fixture
def chalice_client():
    with Client(app.app) as client:
        yield client
