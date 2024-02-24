from httpx import AsyncClient, Response
from fastapi import status
from unittest.mock import patch
from tests.mock_functions import get_user, mock_todos


async def test_authorization(async_client: AsyncClient) -> None:
    response: Response = await async_client.get("/api/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response: Response = await async_client.get("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response: Response = await async_client.post("/api/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response: Response = await async_client.put("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response: Response = await async_client.delete("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@patch("routes.todos.todos", mock_todos())
@patch("mock_data.mock_user_database.MockUserDatabase.get_user", side_effect=get_user)
async def test_get_all_todos(mock_get_user, async_client: AsyncClient):
    # Get authorization header
    form_data = {
        "username": "mock",
        "password": "mock",
        "grant_type": "password",
        "scope": "",
    }
    response: Response = await async_client.post("/api/token", data=form_data)
    data = response.json()
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    # Call API
    response: Response = await async_client.get(
        "/api/todos?page=1&page_size=2&title=Title&sort_by=id", headers=headers
    )
    data = response.json()

    # Assert results
    expected_result = {
        "page": 1,
        "page_size": 2,
        "pages": 1,
        "result": [
            {
                "id": 1,
                "title": "Title 1",
                "description": "Description 1",
                "due_date": "1970-01-01T00:00:00Z",
                "completed": False,
            },
            {
                "id": 2,
                "title": "Title 2",
                "description": "Description 2",
                "due_date": "1970-01-01T00:00:00Z",
                "completed": True,
            },
        ],
    }

    assert response.status_code == status.HTTP_200_OK
    assert data == expected_result


@patch("routes.todos.todos", mock_todos())
@patch("mock_data.mock_user_database.MockUserDatabase.get_user", side_effect=get_user)
async def test_get_single_todo(mock_get_user, async_client: AsyncClient):
    # Get authorization header
    form_data = {
        "username": "mock",
        "password": "mock",
        "grant_type": "password",
        "scope": "",
    }
    response: Response = await async_client.post("/api/token", data=form_data)
    data = response.json()
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    # Call API
    response: Response = await async_client.get("/api/todos/1", headers=headers)
    data = response.json()

    # Assert results
    expected_result = {
        "id": 1,
        "title": "Title 1",
        "description": "Description 1",
        "due_date": "1970-01-01T00:00:00Z",
        "completed": False,
    }

    assert response.status_code == status.HTTP_200_OK
    assert data == expected_result


@patch("routes.todos.todos", mock_todos())
@patch("mock_data.mock_user_database.MockUserDatabase.get_user", side_effect=get_user)
async def test_post_single_todo(mock_get_user, async_client: AsyncClient):
    # Get authorization header
    form_data = {
        "username": "mock",
        "password": "mock",
        "grant_type": "password",
        "scope": "",
    }
    response: Response = await async_client.post("/api/token", data=form_data)
    data = response.json()
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    # New todo payload
    payload = {
        "title": "New Todo",
        "description": "New Description",
        "due_date": "1970-01-01T00:00:00Z",
        "completed": False,
    }

    # Call API
    response: Response = await async_client.post(
        "/api/todos", json=payload, headers=headers
    )
    data = response.json()

    # Assert results
    expected_result = {
        "completed": False,
        "description": "New Description",
        "due_date": "1970-01-01T00:00:00Z",
        "id": 4,
        "title": "New Todo",
    }

    assert response.status_code == status.HTTP_200_OK
    assert data == expected_result


@patch("routes.todos.todos", mock_todos())
@patch("mock_data.mock_user_database.MockUserDatabase.get_user", side_effect=get_user)
async def test_put_single_todo(mock_get_user, async_client: AsyncClient):
    # Get authorization header
    form_data = {
        "username": "mock",
        "password": "mock",
        "grant_type": "password",
        "scope": "",
    }
    response: Response = await async_client.post("/api/token", data=form_data)
    data = response.json()
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    # New todo payload
    payload = {
        "title": "New title",
        "description": "New Description",
        "due_date": "1970-01-01T00:00:00Z",
        "completed": True,
    }

    # Call API
    response: Response = await async_client.put(
        "/api/todos/1", json=payload, headers=headers
    )
    data = response.json()

    # Assert results
    expected_result = {
        "completed": True,
        "description": "New Description",
        "due_date": "1970-01-01T00:00:00Z",
        "id": 1,
        "title": "New title",
    }

    assert response.status_code == status.HTTP_200_OK
    assert data == expected_result


@patch("routes.todos.todos", mock_todos())
@patch("mock_data.mock_user_database.MockUserDatabase.get_user", side_effect=get_user)
async def test_delete_single_todo(mock_get_user, async_client: AsyncClient):
    # Get authorization header
    form_data = {
        "username": "mock",
        "password": "mock",
        "grant_type": "password",
        "scope": "",
    }
    response: Response = await async_client.post("/api/token", data=form_data)
    data = response.json()
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    # Call API
    response: Response = await async_client.delete("/api/todos/1", headers=headers)
    data = response.json()

    # Assert results
    expected_result = {"message": "Todo deleted"}

    assert response.status_code == status.HTTP_200_OK
    assert data == expected_result

    # Call API
    response: Response = await async_client.get(
        "/api/todos?page=1&page_size=1000", headers=headers
    )
    data = response.json()

    # Assert results
    expected_result = {
        "page": 1,
        "page_size": 1000,
        "pages": 1,
        "result": [
            {
                "id": 3,
                "title": "Mock 3",
                "description": "Description 3",
                "due_date": "1970-01-01T00:00:00Z",
                "completed": False,
            },
            {
                "id": 2,
                "title": "Title 2",
                "description": "Description 2",
                "due_date": "1970-01-01T00:00:00Z",
                "completed": True,
            },
        ],
    }

    assert response.status_code == status.HTTP_200_OK
    assert data == expected_result
