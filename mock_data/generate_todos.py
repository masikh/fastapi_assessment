import lorem
import random
from datetime import datetime, timedelta
from models.todo_models import ToDoModel


def random_date_within_range():
    # Get the current date
    current_date = datetime.now()
    start_date = current_date + timedelta(days=7)
    end_date = current_date + timedelta(days=365)
    random_date = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )
    return random_date


mock_todos = [
    ToDoModel(
        id=x,
        title=lorem.sentence(),
        description=lorem.paragraph(),
        completed=random.choice([True, False]),
        due_date=random_date_within_range(),
    )
    for x in range(1000)
]
