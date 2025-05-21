from fastapi.testclient import TestClient
from main import app, lifespan
import asyncio

client = TestClient(app)


def test_lifespan_events():
    async def test_lifespan():
        async with lifespan(app):
            # Test tables creation
            response = client.get("/tasks")
            assert response.status_code == 200

    asyncio.run(test_lifespan())


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello FastAPI!"}