import pytest
import os
import shutil
from src import settings


@pytest.fixture
def test_client():
    from src.main import app
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_code_dir():
    for root, dirs, files in os.walk(settings.CODE_DIR):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
