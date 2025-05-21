import pytest
from fastapi.testclient import TestClient
from main import app
from database import delete_tables, create_tables

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

@pytest.fixture(autouse=True)
async def cleanup_db():
    await delete_tables()
    await create_tables()
    yield