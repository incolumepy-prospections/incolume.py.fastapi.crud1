import pytest
from typing import Generator
from fastapi.testclient import TestClient
from incolume.py.fastapi.crud1.server import app
 

@pytest.fixture(scope="function")
def client() -> Generator:
    with TestClient(app) as cliente:
        yield cliente
