from enum import Enum
from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional
from math import ceil

from mock_data.generate_todos import mock_todos
from models.todo_models import ToDoModel, ToDoListModelPaginated
from models.user_models import User
from helpers.authentication import get_current_active_user
from helpers.levenshtein import search_by_levenshtein

router = APIRouter()

todos = mock_todos


class SortByFields(Enum):
    id = "id"
    title = "title"
    description = "description"
    due_date = "due_date"


class ToDos:
    @staticmethod
    @router.get("/todos", response_model=ToDoListModelPaginated)
    async def get_all(
        page: int,
        page_size: int,
        title: Optional[str] = None,
        sort_by: Optional[SortByFields] = None,
        current_user: User = Depends(get_current_active_user),
    ):
        """
        ## Get all todos from database, filter and sort results

         * filter on (a part of the) title
         * sort by: id, title, description or due_date
        """

        # Filter results on title by levenshtein distance
        _todos = todos.copy()
        if title is not None:
            _todos = search_by_levenshtein(title, data=_todos, field_name="title")

        # Sort by field name
        if sort_by is not None:
            _todos = sorted(_todos, key=lambda x: getattr(x, sort_by.name))

        # Calculate the offset for pagination
        offset = (page - 1) * page_size
        pages = ceil(len(_todos) / page_size)

        # Create paginated result
        result = ToDoListModelPaginated(
            page_size=page_size,
            page=page,
            pages=pages,
            result=[x for x in _todos[offset : offset + page_size]],
        )
        return result

    @staticmethod
    @router.get("/todos/{_id}", response_model=ToDoModel)
    async def get(
        _id: int,
        current_user: User = Depends(get_current_active_user),
    ):
        """
        ## Get todo from database by id
        """

        for todo in todos:
            if todo.id == _id:
                return todo
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    @staticmethod
    @router.post("/todos", response_model=ToDoModel)
    async def post(
        body: ToDoModel,
        current_user: User = Depends(get_current_active_user),
    ):
        """
        ## Create new todo
        """

        global todos
        if not body:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Task is required"
            )

        # Find the maximum ID in the list of todos and create a new ID
        ids = [x.id for x in todos]
        max_id = max(ids) if ids else 0
        new_id = max_id + 1

        # Get body data and add new ID
        body.id = new_id
        new_todo = ToDoModel(**body.model_dump())

        # Store data
        todos.append(new_todo)
        return new_todo

    @staticmethod
    @router.put("/todos/{_id}", response_model=ToDoModel)
    async def put(
        _id: int,
        body: ToDoModel,
        current_user: User = Depends(get_current_active_user),
    ):
        """
        ## Update todo
        """

        global todos
        for i, todo in enumerate(todos):
            if todo.id == _id:
                body.id = _id
                todos[i] = body
                return body
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    @staticmethod
    @router.delete("/todos/{_id}")
    async def delete(
        _id: int,
        current_user: User = Depends(get_current_active_user),
    ):
        """
        ## Delete todo
        """

        global todos
        todos = [todo for todo in todos if todo.id != _id]
        return {"message": "Todo deleted"}
