from passlib.context import CryptContext
from httpx import AsyncClient, Response
from unittest.mock import patch
from models.todo_models import ToDoModel
from datetime import datetime, timezone
from copy import deepcopy


def get_user(*arg, **kwargs):
    """Get user from database by username"""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password = pwd_context.hash("mock")

    return {
        "_id": 0,
        "username": "mock",
        "full_name": "mock",
        "email": "mock@mock.com",
        "hashed_password": password,
        "disabled": False,
        "is_admin": False,
    }


@patch("mock_data.mock_user_database.MockUserDatabase.get_user", side_effect=get_user)
async def get_bearer_token(async_client: AsyncClient):
    # Get authorization header
    form_data = {
        "username": "mock",
        "password": "mock",
        "grant_type": "password",
        "scope": "",
    }
    response: Response = await async_client.post("/api/token", data=form_data)
    return response.json()


todos = [
    ToDoModel(
        id=3,
        title="Mock 3",
        description="Description 3",
        due_date=datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        completed=False,
    ),
    ToDoModel(
        id=2,
        title="Title 2",
        description="Description 2",
        due_date=datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        completed=True,
    ),
    ToDoModel(
        id=1,
        title="Title 1",
        description="Description 1",
        due_date=datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        completed=False,
    ),
]


# Ensure a fresh copy on each unittest
def mock_todos():
    return deepcopy(todos)
