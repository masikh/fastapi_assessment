import pytest
from httpx import AsyncClient, Response
from fastapi import status


@pytest.mark.asyncio
async def test_root(async_client: AsyncClient):
    response: Response = await async_client.get("/")
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    response: Response = await async_client.get(response.next_request.url.path)
    assert response.status_code == status.HTTP_200_OK
