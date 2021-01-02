import pytest


@pytest.fixture
def test_client():
    from src.main import app
    from fastapi.testclient import TestClient
    return TestClient(app)
