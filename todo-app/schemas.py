from pydantic import BaseModel


class Todo(BaseModel):
    task: str