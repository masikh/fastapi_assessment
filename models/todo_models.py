from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class ToDoID(BaseModel):
    """Simple ID model"""

    id: int


class ToDoModel(BaseModel):
    """Simple ToDo Model"""

    id: Optional[int] = None
    title: str
    description: str
    due_date: datetime
    completed: bool = True


class ToDoListModelPaginated(BaseModel):
    """Paginated model"""

    page: int
    page_size: int
    pages: int
    result: List[ToDoModel]
