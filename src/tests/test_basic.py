from chalice.test import Client

from chalicelib import app_config


def test_basic(chalice_client: Client):
    assert app_config.TESTING
    assert chalice_client.http.get("/heartbeat").status_code == 200
