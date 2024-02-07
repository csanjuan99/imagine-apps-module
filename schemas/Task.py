from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
