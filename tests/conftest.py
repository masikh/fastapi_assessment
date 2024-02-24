import pytest_asyncio
from httpx import AsyncClient
from main import init_app

app = init_app()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=f"http://testserver") as client:
        yield client
