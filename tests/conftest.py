from fastapi.testclient import TestClient
from pytest import fixture

from converter.app import app


@fixture
def client():
    yield TestClient(app)
